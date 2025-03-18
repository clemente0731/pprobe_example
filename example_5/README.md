# NumPy 操作监控与拦截系统
# NumPy Operation Monitoring and Interception System

这个项目展示了如何通过 Python 和 NumPy 的分发机制（dispatch mechanism）实现对所有 NumPy 操作的全范围监控和拦截，而无需修改用户代码。
This project demonstrates how to implement comprehensive monitoring and interception of all NumPy operations through Python and NumPy's dispatch mechanism, without modifying user code.

## 核心理念
## Core Concept

通过利用 Python 的 `site` 模块加载机制和 NumPy 的分发机制，我们可以在不修改现有代码的情况下，实现对所有 NumPy 操作的监控、日志记录和数据导出。
By leveraging Python's `site` module loading mechanism and NumPy's dispatch mechanism, we can monitor, log, and export data for all NumPy operations without modifying existing code.

### 关键组件
### Key Components

1. **site 模块加载机制**：
1. **site Module Loading Mechanism**:
   - `sitecustomize.py`：Python 启动时自动加载的模块，全局生效
   - `sitecustomize.py`: Module automatically loaded when Python starts, globally effective
   - `usercustomize.py`：仅在 PYTHONPATH 中指定时加载，可按需启用
   - `usercustomize.py`: Only loaded when specified in PYTHONPATH, can be enabled as needed

2. **NumPy 分发机制**：
2. **NumPy Dispatch Mechanism**:
   - `np.ufunc` - 处理基础数学运算（如加、减、乘、除等）
   - `np.ufunc` - Handles basic mathematical operations (such as addition, subtraction, multiplication, division, etc.)
   - `np.ndarray.__array_ufunc__` - 处理通用函数操作
   - `np.ndarray.__array_ufunc__` - Handles universal function operations
   - `np.ndarray.__array_function__` - 处理高级数组操作
   - `np.ndarray.__array_function__` - Handles advanced array operations

## 实现方式
## Implementation Method

本系统主要通过以下方式实现全操作范围的控制：
This system implements full-range operation control through the following methods:

1. **装饰器模式**：使用装饰器包装所有 NumPy 的 ufunc 操作
1. **Decorator Pattern**: Using decorators to wrap all NumPy ufunc operations
2. **运行时替换**：通过替换 NumPy 命名空间中的函数实现监控
2. **Runtime Replacement**: Implementing monitoring by replacing functions in the NumPy namespace
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


# NumPy 操作批量监控示例 / NumPy Operations Batch Monitoring Example

本示例展示如何使用 `sitecustomize.py` 批量监控 NumPy 的 Universal Functions (ufuncs) 操作函数调用，记录运行时的输入输出数据并保存，方便后续复现和调试，同时保持原始功能不变。

This example demonstrates how to use `sitecustomize.py` to batch monitor NumPy Universal Functions (ufuncs) operation calls, record runtime input/output data for later reproduction and debugging while preserving the original functionality.

## 示例内容 / Example Content

- `example_5.py`: 包含多种 NumPy 操作的示例代码 / Contains example code with various NumPy operations
- `sitecustomize.py`: 实现对 NumPy ufunc 函数的批量钩子，记录调用信息并保存为 `.npy` 文件 / Implements batch hooks for NumPy ufunc functions, records call information and saves as `.npy` files
- `usercustomize.py`: 用户自定义的 Python 启动脚本 / User-defined Python startup script

## 工作原理 / How It Works

NumPy 提供了两种主要的分发机制，用于自定义类与 NumPy 函数的交互：
NumPy provides two main dispatch mechanisms for custom classes to interact with NumPy functions:

这些接口是稳定的API，不会因NumPy版本更新或操作名称变化而受到影响，确保了hook代码的长期兼容性。

1. `__array_ufunc__` 机制:
1. `__array_ufunc__` mechanism:
   - 专门处理 NumPy 的 universal functions (ufuncs)，如 np.add, np.subtract 等基本数学运算
   - Specifically handles NumPy universal functions (ufuncs), such as np.add, np.subtract and other basic mathematical operations
   - 当对象参与 NumPy ufunc 调用时自动触发
   - Automatically triggered when objects participate in NumPy ufunc calls
   - 主要用于重载基本元素级操作
   - Mainly used for overriding basic element-wise operations

2. `__array_function__` 机制:
2. `__array_function__` mechanism:
   - 处理更高级的 NumPy 函数，如 np.concatenate, np.vstack, np.tensordot 等
   - Handles more advanced NumPy functions, such as np.concatenate, np.vstack, np.tensordot, etc.
   - 当对象作为参数传递给大多数 NumPy 命名空间函数时触发
   - Triggered when objects are passed as arguments to most NumPy namespace functions
   - 用于重载更复杂的数组操作和算法
   - Used for overriding more complex array operations and algorithms

这两种机制共同构成了 NumPy 的完整分发系统，使自定义对象能够无缝地与 NumPy 生态系统集成。本示例主要关注 ufunc 操作的监控。
These two mechanisms together form NumPy's complete dispatch system, allowing custom objects to seamlessly integrate with the NumPy ecosystem. This example primarily focuses on monitoring ufunc operations.

当 `PYTHONPATH` 包含当前目录时，Python 启动会自动加载 `sitecustomize.py`，该脚本使用装饰器模式批量替换 NumPy 的 ufunc 操作函数为包装函数：

When `PYTHONPATH` includes the current directory, Python automatically loads `sitecustomize.py`, which uses decorator pattern to batch replace NumPy ufunc operation functions with wrapper functions:

- 通过遍历 `dir(np)` 找到所有 `np.ufunc` 类型的函数
- 为每个 ufunc 函数创建包装函数，保留原始功能的同时添加监控逻辑
- 包装函数同时处理 `__call__` 和 `reduce` 方法，确保完整功能

在执行原始操作的同时，记录输入参数和结果，并将它们保存到 `np_op_dumps` 目录中，便于后续复现运行时的数据。

While executing the original operations, it records input parameters and results, saving them to the `np_op_dumps` directory for later reproduction of runtime data.

## 技术要点 / Technical Highlights

- 使用装饰器模式批量替换多个 NumPy ufunc 操作函数 / Uses decorator pattern to batch replace multiple NumPy ufunc operation functions
- 统一的数据记录和存储机制，支持各种 ufunc 操作 / Unified data recording and storage mechanism, supporting various ufunc operations
- 保留原始函数功能的同时添加监控逻辑 / Adds monitoring logic while preserving the original function functionality
- 处理 ufunc 的 `__call__` 和 `reduce` 方法，确保完整功能 / Handles both `__call__` and `reduce` methods of ufuncs to ensure complete functionality
- 详细的日志输出，包括彩色终端输出，方便调试和分析 / Detailed log output, including colored terminal output, for easy debugging and analysis
- 自动创建数据转储目录，确保数据保存的可靠性 / Automatically creates data dump directory to ensure reliability of data saving
- 区分并解释了 `__array_ufunc__` 和 `__array_function__` 的不同作用 / Distinguishes and explains the different roles of `__array_ufunc__` and `__array_function__`
