import inspect
import time

def example_func(a, b, c=10):
    time.sleep(0.001)
    return a + b + c*c*c*c*c

########################################################
# method 1: modify default parameters (Monkey Patching)
start_time = time.time()
for _i in range(10000):
    example_func.__defaults__ = (20,)
end_time = time.time()
monkey_patch_duration = end_time - start_time
print("Monkey Patching Time:", end_time - start_time)

########################################################
# method 2: modify signature using inspect
def modify_function(func, new_defaults):
    sig = inspect.signature(func)
    new_params = []
    for name, param in sig.parameters.items():
        if name in new_defaults:
            new_param = param.replace(default=new_defaults[name])
        else:
            new_param = param
        new_params.append(new_param)
    new_sig = sig.replace(parameters=new_params)
    def new_func(*args, **kwargs):
        bound_args = new_sig.bind(*args, **kwargs)
        return func(*bound_args.args, **bound_args.kwargs)
    new_func.__signature__ = new_sig
    return new_func

start_time = time.time()
for _i in range(10000):
    modified_func = modify_function(example_func, {'c': 20})
end_time = time.time()
inspect_modify_duration = end_time - start_time
print("Inspect Modify Time:", end_time - start_time)
print(f"Inspect Modify Time / Monkey Patching Time = {inspect_modify_duration/monkey_patch_duration}")

########################################################
# method 3: use audit
# sys.addaudithook Added in version 3.8.1
# sys.audit Added in version 3.11
import sys
def audit_hook(event, args):
    # intercept function calls and modify the arguments for example_func
    if event == "call" and args[0] == example_func:
        # args[1] is the positional arguments tuple
        # args[2] is the keyword arguments dictionary
        if len(args) >= 3 and isinstance(args[2], dict):
            # modify the 'c' parameter to 20 if not explicitly provided
            if 'c' not in args[2] and len(args[1]) < 3:
                args[2]['c'] = 20


start_time = time.time()
for _i in range(10000):
    # register the audit hook
    sys.addaudithook(audit_hook)
end_time = time.time()
audit_duration = end_time - start_time
print("Audit Time:", end_time - start_time)
print(f"Audit Time / Monkey Patching Time = {audit_duration/monkey_patch_duration}")
