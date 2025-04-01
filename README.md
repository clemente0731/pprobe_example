# NumPy 操作监控与拦截系统

这个项目展示了如何通过 Python 和 NumPy 的分发机制（dispatch mechanism）实现对所有 NumPy 操作的全范围监控和拦截，而无需修改用户代码。

## 核心理念

通过利用 Python 的 `site` 模块加载机制和 NumPy 的分发机制，我们可以在不修改现有代码的情况下，实现对所有 NumPy 操作的监控、日志记录和数据导出。

### 关键组件

1. **site 模块加载机制**：
   - `sitecustomize.py`：Python 启动时自动加载的模块，全局生效
   - `usercustomize.py`：仅在 PYTHONPATH 中指定时加载，可按需启用

2. **NumPy 分发机制**：
   - `np.ufunc` - 处理基础数学运算（如加、减、乘、除等）
   - `np.ndarray.__array_ufunc__` - 处理通用函数操作
   - `np.ndarray.__array_function__` - 处理高级数组操作

## 实现方式

本系统主要通过以下方式实现全操作范围的控制：

1. **装饰器模式**：使用装饰器包装所有 NumPy 的 ufunc 操作
2. **运行时替换**：通过替换 NumPy 命名空间中的函数实现监控
3. **环境变量控制**：通过 PYTHONPATH 环境变量控制是否启用监控系统

```python
# 核心实现原理
def monitor_ufunc(ufunc_obj):
    original_call = ufunc_obj.__call__
    
    @functools.wraps(original_call)
    def wrapped_call(*args, **kwargs):
        # 前置处理：记录输入
        result = original_call(*args, **kwargs)  # 调用原始函数
        # 后置处理：记录输出
        return result
    
    return wrapped_call

# 应用到所有 ufunc 函数
for ufunc_name in dir(np):
    obj = getattr(np, ufunc_name)
    if isinstance(obj, np.ufunc):
        setattr(np, ufunc_name, monitor_ufunc(obj))
```

## 使用方法

1. 全局启用监控（适用于所有 Python 脚本）：
   - 将 `sitecustomize.py` 放到 Python 的 site-packages 目录中

2. 按需启用监控（仅针对特定运行）：
   - 设置 PYTHONPATH 环境变量指向包含 `usercustomize.py` 的目录
   - 示例：`PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_5.py`

3. 运行示例脚本：
   ```bash
   ./run_example_5.sh
   ```

## 数据导出

所有被监控的 NumPy 操作的输入和输出将被自动保存：

- 保存位置：`np_op_dumps/` 目录
- 文件格式：`.npy` 文件（NumPy 原生格式）
- 命名规则：`op_{操作名}_input{序号}_{前缀}.npy` 和 `op_{操作名}_output_{前缀}.npy`

## 应用场景

1. **深度学习调试**：跟踪模型内部的数值变化和梯度流动
2. **性能分析**：识别高频使用的 NumPy 操作进行优化
3. **数据流分析**：了解复杂计算中的数据处理路径
4. **单元测试**：自动保存中间结果用于回归测试
5. **教学工具**：可视化 NumPy 操作的实际效果

## 优势

- **非侵入式**：不需要修改现有代码
- **全覆盖**：捕获所有 NumPy 操作
- **灵活控制**：可以通过环境变量启用或禁用
- **选择性监控**：可以扩展为仅监控特定操作
- **原始功能保留**：在监控的同时保持原有功能不变

## 扩展方向

可以类似地扩展到其他库的操作监控：
- PyTorch 张量操作
- TensorFlow 计算图操作
- Pandas 数据操作
- 其他科学计算库 