# Python Site-Packages Customization Example / Python站点包自定义示例

这个示例演示了Python的site-packages自定义功能的工作原理。
This example demonstrates how Python's site-packages customization works.

特别展示了如何使用`sitecustomize.py`来修改导入模块的行为。
Specifically, it shows how `sitecustomize.py` can be used to modify the behavior of imported modules.

## 示例内容 / Example Content

这个示例创建了两个NumPy数组，并尝试使用`np.add()`将它们相加。
This example creates two NumPy arrays and attempts to add them together using `np.add()`.

正常运行时，`np.add()`按预期执行加法操作。
When run normally, `np.add()` performs addition as expected.

当在Python路径中包含`sitecustomize.py`运行时，它将`np.add`替换为`np.subtract`。
When run with the `sitecustomize.py` in the Python path, it replaces `np.add` with `np.subtract`.

这展示了如何使用`sitecustomize.py`修改导入模块的行为。
This demonstrates how `sitecustomize.py` can be used to modify the behavior of imported modules.

## 文件说明 / Files Description

- `example_2.py`: 创建数组并执行加法的主脚本。
  The main script that creates arrays and performs addition.

- `sitecustomize.py`: 将`np.add`替换为`np.subtract`的自定义脚本。
  Customization script that replaces `np.add` with `np.subtract`.

- `usercustomize.py`: 一个空的自定义文件（本示例中未使用）。
  An empty customization file (not used in this example).

- `run_example_2.sh`: 用于运行示例的Shell脚本，分别展示有无自定义时的结果。
  Shell script to run the example with and without the customization.

## 运行方法 / How to Run

运行以下命令来执行示例：
Run the following command to execute the example:

```bash
./run_example_2.sh
```

## 代码示例 / Code Example

```python
import numpy as np

# create a 1d array
arr = np.array([1, 2, 3, 4, 5])
print("arr: ", arr)

# create a 1d array
arr2 = np.array([-1, -2, -3, -4, -5])
print("arr2: ", arr2)

# plus
arr3 = np.add(arr, arr2)
print("arr3: ", arr3)
```

## 预期输出 / Expected Output

不使用自定义时的输出：
Output without customization:

```
arr:  [1 2 3 4 5]
arr2:  [-1 -2 -3 -4 -5]
arr3:  [0 0 0 0 0]  # 加法结果 / Addition result
```

在PYTHONPATH中包含sitecustomize.py时的输出：
Output with sitecustomize.py in PYTHONPATH:

```
start ==> example_1/sitecustomize.py
	np.add is now replaced with np.subtract: <ufunc 'subtract'>
	This means all np.add operations will perform subtraction instead
end ==> example_1/sitecustomize.py
arr:  [1 2 3 4 5]
arr2:  [-1 -2 -3 -4 -5]
arr3:  [2 4 6 8 10]  # 减法结果(arr - arr2) / Subtraction result (arr - arr2)
```
