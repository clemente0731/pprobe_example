# Example 1: Python Site Customization Demo

## 简介 (Introduction)

这个示例演示了Python的站点自定义功能，通过`sitecustomize.py`和`usercustomize.py`模块在Python启动时自动执行代码。

This example demonstrates Python's site customization feature, which allows automatic code execution during Python startup through the `sitecustomize.py` and `usercustomize.py` modules.

## 文件结构 (File Structure)

- `run_example_1.sh`: 运行示例的Shell脚本
- `sitecustomize.py`: 站点自定义模块，Python启动时自动导入
- `usercustomize.py`: 用户自定义模块，Python启动时自动导入（在sitecustomize之后）

## 工作原理 (How It Works)

当Python解释器启动时，它会自动查找并导入`sitecustomize`和`usercustomize`模块。这些模块可以用于设置环境、修改Python路径或执行任何需要在程序开始前运行的代码。

When the Python interpreter starts, it automatically looks for and imports the `sitecustomize` and `usercustomize` modules. These modules can be used to set up environments, modify Python paths, or execute any code that needs to run before your program begins.

导入顺序：
1. 首先导入`sitecustomize.py`
2. 然后导入`usercustomize.py`

Import order:
1. First, `sitecustomize.py` is imported
2. Then, `usercustomize.py` is imported

## 本示例内容 (This Example)

在本示例中，我们有两个简单的Python模块：
- `sitecustomize.py` 只是打印一条消息 `==> example_1/sitecustomize.py`
- `usercustomize.py` 只是打印一条消息 `==> example_1/usercustomize.py`

In this example, we have two simple Python modules:
- `sitecustomize.py` simply prints a message `==> example_1/sitecustomize.py`
- `usercustomize.py` simply prints a message `==> example_1/usercustomize.py`

我们的Shell脚本 `run_example_1.sh` 设置了 `PYTHONPATH` 环境变量，以确保Python能够找到这些模块，然后运行了一个简单的Python命令。

Our shell script `run_example_1.sh` sets the `PYTHONPATH` environment variable to ensure Python can find these modules, then runs a simple Python command.

## 运行示例 (Running the Example)

执行以下命令运行示例：

```bash
./run_example_1.sh
```

你将看到以下输出：

```
==> example_1/sitecustomize.py
==> example_1/usercustomize.py
Hello example1
```

这表明：
1. Python在启动时先导入并执行了`sitecustomize.py`
2. 然后导入并执行了`usercustomize.py`
3. 最后才执行了指定的Python代码 `print('Hello example1')`

This indicates that:
1. Python first imported and executed `sitecustomize.py` at startup
2. Then imported and executed `usercustomize.py`
3. Finally executed the specified Python code `print('Hello example1')`

## 用途 (Use Cases)

这种自动导入机制对以下场景非常有用：
- 设置环境变量
- 配置日志系统
- 添加自定义导入钩子
- 修改Python路径
- 在所有Python程序启动时执行通用初始化代码

This automatic import mechanism is particularly useful for:
- Setting environment variables
- Configuring logging systems
- Adding custom import hooks
- Modifying Python paths
- Executing common initialization code for all Python programs

## 注意事项 (Notes)

- 这些模块必须位于Python的导入路径中才能被自动导入
- 在本示例中，我们通过设置`PYTHONPATH`环境变量确保模块可以被找到
- 使用这些模块时要小心，因为它们会影响所有Python程序的启动过程
- 在生产环境中使用前，请确保了解其潜在影响

These modules must be in Python's import path to be automatically imported. In this example, we ensure the modules can be found by setting the `PYTHONPATH` environment variable. Be careful when using these modules as they affect the startup process of all Python programs. Make sure you understand their potential impact before using them in a production environment.
