import numpy as np
from functools import wraps

class DebugArray(np.ndarray):
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        print(f"[DEBUG] Ufunc调用状态 | 函数: {ufunc.__name__}, 方法类型: {method}")
        print(f"输入参数: {inputs}")
        print(f"关键字参数: {kwargs}")
        
        # 调用原始实现
        result = super().__array_ufunc__(ufunc, method, *inputs, **kwargs)
        
        print(f"返回结果形状: {result.shape if hasattr(result, 'shape') else '标量'}")
        return result

def ufunc_debug_wrapper(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        # 将输入数组转换为调试子类
        debug_args = [np.asarray(a).view(DebugArray) if isinstance(a, np.ndarray) else a 
                     for a in args]
        return func(*debug_args, **kwargs)
    return wrapped

# 动态替换np模块中的ufunc
import inspect

for name in dir(np):
    obj = getattr(np, name)
    if isinstance(obj, np.ufunc):
        setattr(np, name, ufunc_debug_wrapper(obj))

# 现在所有np.ufunc调用都会打印日志
np.add(np.array([1,2]), np.array([3,4]))
