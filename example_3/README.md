# NumPy 函数监控示例 / NumPy Function Monitoring Example

本示例展示如何使用 `sitecustomize.py` 监控 NumPy 的 `add` 函数调用，记录输入输出并保存数据，同时保持原始功能不变。
This example demonstrates how to use `sitecustomize.py` to monitor NumPy's `add` function calls, log inputs/outputs and save data while preserving the original functionality.

## 示例内容 / Example Content

- `example_3.py`: 简单的 NumPy 数组加法示例
- `sitecustomize.py`: 实现 `np.add` 函数钩子，记录调用信息并保存为 `.npy` 文件
- `test_example_3.py`: 验证钩子函数正确性的测试代码
- `run_example_3.sh`: 分别在有无 `sitecustomize.py` 环境下运行示例并执行测试

## 工作原理 / How It Works

当 `PYTHONPATH` 包含当前目录时，Python 启动会自动加载 `sitecustomize.py`，该脚本替换 `np.add` 为包装函数，在执行原始加法操作的同时，记录输入参数和结果，并将它们保存到 `np_add_dumps` 目录中。

## 技术要点 / Technical Highlights

- 使用 monkey patching 技术替换库函数
- 保留原始函数功能的同时添加监控逻辑
- 通过环境变量控制功能启用/禁用
