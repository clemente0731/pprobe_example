import sys
import importlib.abc
import importlib.util
from contextlib import contextmanager

class HookManager(importlib.abc.MetaPathFinder):
    def __init__(self):
        self.hooks = []
        self._processing = set()  # prevent recursive processing

    def add_hook(self, hook, priority=0):
        """ add hook and automatically sort """
        self.hooks.append((priority, hook))
        self.hooks.sort(key=lambda x: -x[0])  # higher priority first

    def find_spec(self, fullname, path, target=None):
        print(f"HookManager ><>>>>>>> [Hook] captured module import: {fullname}, path: {path}, target: {target}")
        if fullname in self._processing:
            return None
            
        self._processing.add(fullname)
        try:
            for _, hook in self.hooks:
                if spec := hook.find_spec(fullname, path, target):
                    return spec
        finally:
            self._processing.remove(fullname)

class BaseHook(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, priority=0):
        self.priority = priority
        self._active = True
        self._finder_index = None  # record hook position

    @contextmanager
    def _disable_hook(self):
        """ context manager to temporarily disable the hook """
        prev_state = self._active
        self._active = False
        try:
            yield
        finally:
            self._active = prev_state

    def find_spec(self, fullname, path, target=None):
        print(f"BaseHook ><>>>>>>> [Hook] captured module import: {fullname}, path: {path}, target: {target}")
        if not self._active:
            print(f"BaseHook ><>>>>>>> [Hook] not processing module import: {fullname}, reason: hook not active")
            return None
        if not self.can_handle(fullname):
            print(f"BaseHook ><>>>>>>> [Hook] not processing module import: {fullname}, reason: module name does not match")
            return None
        
        print(f"BaseHook ><>>>>>>> [Hook] processing module import: {fullname}, reason: module name matches and hook is active")
        return importlib.util.spec_from_loader(fullname, self)

    def can_handle(self, fullname):
        raise NotImplementedError
    
    

class FunctionHook(BaseHook):
    def __init__(self, module_name, func_name, wrapper, priority=0):
        print(f"FunctionHook initializing function hook: {module_name}.{func_name}, wrapper: {wrapper}")
        super().__init__(priority)
        self.module_name = module_name
        self.func_name = func_name
        self.wrapper = wrapper
        self._function_patched = False  # flag indicating if function has been modified
        
    def can_handle(self, fullname):
        """
        check if the specified module import should be handled
        
        this method is called by BaseHook.find_spec to determine if the current hook
        should handle a specific module import. when the Python import system calls
        HookManager.find_spec, the HookManager iterates through all registered hooks
        and calls their find_spec methods. BaseHook.find_spec calls this method to
        decide whether to process the import.
        
        args:
            fullname: the full name of the module to be imported
            
        returns:
            bool: True if the module should be handled, False otherwise
        """
        print(f"FunctionHook can_handle checking module: {fullname} vs {self.module_name}")
        # check if this is the target module or its submodule
        return fullname == self.module_name
    
    def create_module(self, spec):
        print(f"FunctionHook creating module: {spec.name}")
        # if the module is already in sys.modules, return it directly
        # this avoids creating duplicate modules
        if spec.name in sys.modules:
            print(f"module {spec.name} already in sys.modules, returning directly")
            return sys.modules[spec.name]
        
        # if the module is not in sys.modules, return None to let importlib use default creation
        print(f"module {spec.name} not in sys.modules, returning None for importlib to create")
        return None
        
    def exec_module(self, module):
        print(f"FunctionHook executing module: {module.__name__}")
        
        # avoid duplicate modifications
        if self._function_patched:
            print(f"function {self.func_name} already modified, skipping")
            return
        
        # ensure the module is fully initialized
        # sometimes the module might still be in the initialization process, and the function might not exist yet
        if not hasattr(module, self.func_name):
            print(f"function {self.func_name} does not exist in module {module.__name__}, attempting full import")
            # try to fully import the module
            with self._disable_hook():
                try:
                    # use importlib to reload the module, ensuring it's fully loaded
                    importlib.reload(module)
                except Exception as e:
                    print(f"failed to reload module: {e}")
        
        # apply function modification
        with self._disable_hook():
            if hasattr(module, self.func_name):
                original = getattr(module, self.func_name)
                wrapped = self.wrapper(original)
                
                # preserve original function metadata
                if hasattr(original, "__name__"):
                    wrapped.__name__ = original.__name__
                if hasattr(original, "__doc__"):
                    wrapped.__doc__ = original.__doc__
                if hasattr(original, "__module__"):
                    wrapped.__module__ = original.__module__
                
                # apply modification
                setattr(module, self.func_name, wrapped)
                self._function_patched = True
                print(f"successfully modified function: {self.module_name}.{self.func_name}")
            else:
                print(f"warning: function {self.func_name} not found in module {module.__name__}")


# 初始化管理器
manager = HookManager()
# insert the hook manager at the beginning of sys.meta_path
# sys.meta_path is a core component of Python's module import system, a list containing all meta path finders
# this code accomplishes the following:
# 1. registers our HookManager as the first import hook, which can intercept Python module import processes
# 2. when Python executes an "import module_name" statement, the interpreter iterates through each finder in sys.meta_path
# 3. since our manager is inserted at the front of the list (index 0), it will be called first, giving it priority to intercept all module import requests
# 4. this mechanism is based on Python's import protocol, defined in PEP 302 and PEP 451, allowing developers to customize module import behavior
# 
# in Python's import system, an importer is responsible for finding and loading modules, typically consisting of two parts:
# - finder: determines if a module exists and how to load it via the find_spec method, returning a ModuleSpec object
# - loader: creates module objects via the create_module method and executes module code via exec_module method to initialize the module
#
# when our hook intercepts a module import request, it can modify module behavior, replace module content, or even completely take over the module creation and execution process
sys.meta_path.insert(0, manager)


def numpy_func_warpper(original_function):
    # function to replace numpy.add with numpy.sub
    def wrapped_f(a, b):
        # call numpy.sub directly instead of add
        print(f"debug: ><>>>>>>> original function being called: {original_function}")
        c = original_function(a, b)
        print(f"debug: ><>>>>>>> result after function execution: {c}")
        print("debug: ><>>>>>>> function execution completed successfully")
        return c
    return wrapped_f

# add a hook to replace numpy.add with numpy.sub function
manager.add_hook(
    FunctionHook("numpy", "add", numpy_func_warpper),
    priority=50
)
