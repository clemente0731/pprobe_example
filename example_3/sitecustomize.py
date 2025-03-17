print("start ==> example_3/sitecustomize.py")


# hook numpy.add function to monitor inputs and outputs
# this code will monkey patch numpy.add to log and save data while preserving original functionality

import numpy as np
original_add = np.add

def dump_numpy_data(x1, x2, result, prefix="example_3"):
    # dump inputs and outputs to npy files
    import os
    dump_dir = "np_add_dumps"
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    
    # save inputs and output to npy files
    np.save(f"{dump_dir}/input1_{prefix}.npy", x1)
    np.save(f"{dump_dir}/input2_{prefix}.npy", x2)
    np.save(f"{dump_dir}/output_{prefix}.npy", result)
    print(f"\033[1;32m\t- Dumped inputs and output to {dump_dir}/ directory\033[0m")

def print_numpy_data(x1, x2, result, prefix="example_3"):
    print(f"\033[1;32m\t- Input 1: \033[0m", x1)
    print(f"\033[1;32m\t- Input 2: \033[0m", x2)
    print(f"\033[1;32m\t- Output: \033[0m", result)

def add_hook(x1, x2, *args, **kwargs):
    result = original_add(x1, x2, *args, **kwargs)

    # print data to console
    print_numpy_data(x1, x2, result, "example_3")

    # dump data to files
    dump_numpy_data(x1, x2, result, "example_3")

    return result

np.add = add_hook
print("\033[1;32m\tnp.add is now hooked to log inputs and outputs \033[0m")
print("\033[1;33m\tOriginal functionality is preserved but inputs and outputs will be logged and saved as npy files\033[0m")


print("end ==> example_3/sitecustomize.py")