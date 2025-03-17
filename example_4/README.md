# NumPy 操作批量监控示例 / NumPy Operations Batch Monitoring Example

本示例展示如何使用 `sitecustomize.py` 批量监控 NumPy 的多种操作函数调用（包括一元、二元和三元操作），记录运行时的输入输出数据并保存，方便后续复现和调试，同时保持原始功能不变。

This example demonstrates how to use `sitecustomize.py` to batch monitor various NumPy operation function calls (including unary, binary, and ternary operations), record runtime input/output data for later reproduction and debugging while preserving the original functionality.

## 示例内容 / Example Content

- `example_4.py`: 包含多种 NumPy 操作的示例代码 / Contains example code with various NumPy operations
- `sitecustomize.py`: 实现对 NumPy 多种操作函数的批量钩子，记录调用信息并保存为 `.npy` 文件 / Implements batch hooks for various NumPy operation functions, records call information and saves as `.npy` files
- `test_example_4.py`: 使用参数化测试验证所有被监控操作的正确性 / Uses parameterized tests to verify the correctness of all monitored operations
- `run_example_4.sh`: 分别在有无 `sitecustomize.py` 环境下运行示例并执行测试 / Runs the example and executes tests with and without the `sitecustomize.py` environment

## 工作原理 / How It Works

当 `PYTHONPATH` 包含当前目录时，Python 启动会自动加载 `sitecustomize.py`，该脚本批量替换 NumPy 的各种操作函数为包装函数：

When `PYTHONPATH` includes the current directory, Python automatically loads `sitecustomize.py`, which batch replaces various NumPy operation functions with wrapper functions:

- 一元操作 / Unary operations: negative, positive, absolute, sqrt, square
- 二元操作 / Binary operations: add, subtract, multiply, divide, power
- 三元操作 / Ternary operations: where

在执行原始操作的同时，记录输入参数和结果，并将它们保存到 `np_op_dumps` 目录中，便于后续复现运行时的数据。测试代码会自动从这些保存的数据中加载并验证操作的正确性。

While executing the original operations, it records input parameters and results, saving them to the `np_op_dumps` directory for later reproduction of runtime data. The test code automatically loads from these saved data and verifies the correctness of the operations.

## 技术要点 / Technical Highlights

- 使用 monkey patching 技术批量替换多个 NumPy 操作函数 / Uses monkey patching technique to batch replace multiple NumPy operation functions
- 统一的数据记录和存储机制，支持一元、二元和三元操作类型 / Unified data recording and storage mechanism, supporting unary, binary, and ternary operation types
- 保留原始函数功能的同时添加监控逻辑 / Adds monitoring logic while preserving the original function functionality
- 通过环境变量控制功能启用/禁用 / Controls feature enabling/disabling through environment variables
- 使用参数化测试自动验证所有操作的正确性 / Uses parameterized tests to automatically verify the correctness of all operations
- 支持从保存的数据中重新加载并验证，实现运行时数据的完整复现 / Supports reloading and verification from saved data, achieving complete reproduction of runtime data
- 详细的日志输出，包括彩色终端输出，方便调试和分析 / Detailed log output, including colored terminal output, for easy debugging and analysis
