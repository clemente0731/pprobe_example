import os
import threading
print(f"start ==> example_9/sitecustomize.py (pid: {os.getpid()}, thread: {threading.current_thread().ident})")

# replace compatible numpy interfaces with jax.numpy
import sys
import importlib.util

# check if numpy is already imported
if 'numpy' in sys.modules:
    # if numpy is already imported, we can't replace it
    print("warning: numpy already imported, can't replace with jax.numpy")
else:
    # create a proxy numpy module that redirects to jax.numpy when possible
    class NumpyProxy:
        def __init__(self):
            # ensure jax.numpy is imported
            import jax.numpy as jnp
            self.jnp = jnp
            
            # import real numpy for fallback
            import numpy as np_original
            self.np_original = np_original
            
        def __getattr__(self, name):
            # try to get attribute from jax.numpy first
            if hasattr(self.jnp, name):
                return getattr(self.jnp, name)
            # set origin numpy as fallback opt
            # fallback to original numpy for unsupported features
            if hasattr(self.np_original, name):
                return getattr(self.np_original, name)
            raise AttributeError(f"module 'numpy' has no attribute '{name}'")
    
    # create and register the proxy numpy module
    numpy_module = NumpyProxy()
    sys.modules['numpy'] = numpy_module
    print("compatible numpy interfaces replaced with jax.numpy")

print(f"end ==> example_9/sitecustomize.py (pid: {os.getpid()}, thread: {threading.current_thread().ident})")
