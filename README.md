python runtime hook presentation


# 在讲述如何实现hook这套方案之间, 我想先描述一下遇到的问题 或者说 钉子

# 一行不改 -> 兼容 compatibility
# 批量捕获 -> 减少后处理 reduce post-processing

# before i present how hook did 

# non-intrusive modification and compatibility in the open-source cuda-like community.
torch.device("cuda")    --> torch.device("asic_device")
torch.device("cuda:2")  --> torch.device("asic_deivce:2")

最坏的情况你需要对所有的开源库做一遍适配

# Examine the level of the accuracy generalization ability of this software stack via the modelzoo which is cuda-like.
# 1700-1800 models from torchvision,transformers,pytorch-image-models,diffusers,mmcv in limited resources

source_a_model_a -> different optimizers + different steps -> training_res_output
source_a_model_b -> different optimizers + different steps -> training_res_output
source_b_model_a -> different optimizers + different steps -> training_res_output
...
source_n_model_n -> different optimizers + different steps -> training_res_output

最坏的情况你需要对1800个模型单独做后处理

# 模型优化 或者 某些功能fallback
用户本地代码+python third_lib + python buildin-lib 有一些高度封装的库, 我们在使用的时候不确定他做了什么或者没做什么, 如果需要做图的优化或者某个layer的修改
可能是 用户本地代码 需要修改
可能是 python third_lib 需要修改
可能是 用户本地代码 + third_lib 需要修改
可能是 用户本地代码 + third_lib_a + third_lib_b + ... + third_lib_n 需要修改

最坏的情况你需要对用 户本地代码 + third_lib_a + third_lib_b + ... + third_lib_n 前处理

# WORKAROUND
1. 第三方库产生的非客户或者交付产品的问题
2. 第三方库导致的性能或者写法问题 numpy -> jax.numpy

# 钉子有了 我们来定义一下钉子的正确定义
# 需要有一种机制能够实现 python运行时的对某些函数的替换/修改/输入输出和函数内变量的导出

# 那么现在我们去造锤子
# 实现hook可以分成两部分
1. 控制权 -> 如何接管程序执行流程 -> 提供 运行时 全局作用域 能够替换 的能力
2. patch/replace   -> 在 进程生命周期内 保证 函数的替换/修改/输入输出和函数内变量 
   1. -> Monkeypatch -> 在 Python 中，类、函数、方法等都是对象，变量只是对这些对象的引用
      1. Monkeypatch 就是通过重新赋值这些变量，将原来的对象替换为新的对象。# pprobe_example
