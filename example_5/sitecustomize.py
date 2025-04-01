import os
import threading
print(f"start ==> example_5/sitecustomize.py (pid: {os.getpid()}, thread: {threading.current_thread().ident})")

# hook numpy operations using dispatch mechanism to monitor inputs and outputs
# this code will hook numpy operations to log and save data while preserving original functionality

# hook numpy operations using dispatch mechanism to monitor inputs and outputs
import numpy as np
import os
from functools import wraps
import functools



## hook numpy operations using dispatch mechanism to monitor inputs and outputs
# numpy/core/overrides.py


# create dump directory
dump_dir = "np_op_dumps"
if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)

def dump_numpy_data(inputs, result, op_name, prefix="example_5"):
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



# np.ndarray.__array_ufunc__ 和 np.ndarray.__array_function__ 的区别:
# 
# 1. __array_ufunc__: 
#    - 处理 NumPy 的 universal functions (ufuncs)，如 np.add, np.subtract 等基本数学运算
#    - 当调用 NumPy ufunc 时会触发此方法
#    - 主要用于基本元素级操作的重载
#
# 2. __array_function__:
#    - 处理更高级的 NumPy 函数，如 np.concatenate, np.vstack, np.tensordot 等
#    - 当调用大多数 NumPy 命名空间函数时会触发此方法
#    - 用于重载更复杂的数组操作和算法
#
# 两者共同构成了 NumPy 的分发机制，允许自定义类与 NumPy 函数交互

# 由于 numpy.ndarray 是不可变类型，无法直接修改其 __array_ufunc__ 方法
# 使用装饰器模式来监控 ufunc 操作

# 创建一个装饰器来包装 ufunc 函数
def monitor_ufunc(ufunc_obj):
    # save original __call__ method
    original_call = ufunc_obj.__call__
    original_reduce = ufunc_obj.reduce
    
    @functools.wraps(original_call)
    def wrapped_call(*args, **kwargs):
        # get operation name
        op_name = ufunc_obj.__name__
        print(f"\033[1;34m\t- UFUNC Operation: {op_name}\033[0m")
        
        # print input parameters
        for i, arg in enumerate(args):
            print(f"\033[1;32m\t- UFUNC Input {i+1}: \033[0m", arg)
        
        # call original method
        result = original_call(*args, **kwargs)
        
        # print output result
        print(f"\033[1;32m\t- UFUNC Output: \033[0m", result)
        
        # dump inputs and outputs to npy files
        dump_numpy_data(args, result, f"{op_name}")
        
        # print detailed information about inputs and output
        print_numpy_data(args, result, f"{op_name}")
        
        return result
    
    # create a wrapped reduce method to fix the AttributeError
    @functools.wraps(original_reduce)
    def wrapped_reduce(array, *args, **kwargs):
        print(f"\033[1;34m\t- UFUNC Reduce Operation: {ufunc_obj.__name__}\033[0m")
        try:
            result = original_reduce(array, *args, **kwargs)
            print(f"\033[1;32m\t- UFUNC Reduce Result: \033[0m", result)
            return result
        except Exception as e:
            print(f"\033[1;31m\t- Error in UFUNC Reduce: {e}\033[0m")
            raise
    
    # create a new function that has both __call__ and reduce methods
    wrapped_call.reduce = wrapped_reduce
    
    return wrapped_call

# apply monitoring to common ufunc functions
for ufunc_name in dir(np):
    obj = getattr(np, ufunc_name)
    if isinstance(obj, np.ufunc):
        setattr(np, ufunc_name, monitor_ufunc(obj))

print("\033[1;32m\tAll NumPy operations are now hooked to log inputs and outputs\033[0m")
print("\033[1;33m\tOriginal functionality is preserved but inputs and outputs will be logged and saved as npy files\033[0m")

print(f"end ==> example_5/sitecustomize.py (pid: {os.getpid()}, thread: {threading.current_thread().ident})")
