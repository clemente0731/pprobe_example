print("start ==> example_4/sitecustomize.py")

# hook numpy operations using dispatch mechanism to monitor inputs and outputs
# this code will hook numpy operations to log and save data while preserving original functionality

import numpy as np
import os
from functools import wraps

# create dump directory
dump_dir = "np_op_dumps"
if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)

def dump_numpy_data(inputs, result, op_name, prefix="example_4"):
    """dump inputs and outputs to npy files"""
    # save inputs and output to npy files
    for i, inp in enumerate(inputs):
        np.save(f"{dump_dir}/op_{op_name}_input{i+1}_{prefix}.npy", inp)
    
    np.save(f"{dump_dir}/op_{op_name}_output_{prefix}.npy", result)
    print(f"\033[1;32m\t- Dumped {op_name} inputs and output to {dump_dir}/ directory\033[0m")

def print_numpy_data(inputs, result, op_name):
    """print inputs and output to console"""
    print(f"\033[1;34m\t- Operation: {op_name}\033[0m")
    for i, inp in enumerate(inputs):
        print(f"\033[1;32m\t- Input {i+1}: \033[0m", inp)
    print(f"\033[1;32m\t- Output: \033[0m", result)

def hook_numpy_op(original_func):
    """hook a numpy operation to log inputs and outputs"""
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        # get operation name
        op_name = original_func.__name__
        
        # filter out non-array arguments
        inputs = [arg for arg in args if isinstance(arg, np.ndarray)]
        
        # call original function
        result = original_func(*args, **kwargs)
        
        # print data to console
        print_numpy_data(inputs, result, op_name)
        
        # dump data to files
        dump_numpy_data(inputs, result, op_name, "example_4")
        
        return result
    
    return wrapper

# hook unary operations
unary_ops = [np.negative, np.positive, np.absolute, np.sqrt, np.square]
for op in unary_ops:
    setattr(np, op.__name__, hook_numpy_op(op))

# hook binary operations
binary_ops = [np.add, np.subtract, np.multiply, np.divide, np.power]
for op in binary_ops:
    setattr(np, op.__name__, hook_numpy_op(op))

# hook ternary operations
ternary_ops = [np.where]
for op in ternary_ops:
    setattr(np, op.__name__, hook_numpy_op(op))

print("\033[1;32m\tNumPy operations are now hooked to log inputs and outputs\033[0m")
print("\033[1;33m\tOriginal functionality is preserved but inputs and outputs will be logged and saved as npy files\033[0m")

print("end ==> example_4/sitecustomize.py")