import numpy as np
import wrapt


@wrapt.decorator
def ufunc_debug_wrapper(wrapped, instance, args, kwargs):
    # print function name
    print(f"[DEBUG] Ufunc call | Function: {wrapped.__name__}")
    
    # print input shapes if they are arrays
    for i, arg in enumerate(args):
        if isinstance(arg, np.ndarray):
            print(f"Input {i} shape: {arg.shape}")
        else:
            print(f"Input {i}: {arg} (not an array)")
    
    # print keyword arguments
    if kwargs:
        print(f"Keyword arguments: {kwargs}")
    
    # call the original function with arguments
    result = wrapped(*args, **kwargs)
    
    # print result information
    if isinstance(result, np.ndarray):
        print(f"\033[1;32mResult shape: {result.shape}\033[0m")
    else:
        print(f"\033[1;33mResult: {result} (scalar)\033[0m")
        
    return result

# simulate power function error
def buggy_power(*args, **kwargs):
    print(f"\033[1;31m[ERROR] Power function failed with args: {args}\033[0m")
    
    # auto-generate pytest file when error occurs
    import os
    import numpy as np
    
    # get current timestamp
    test_file_name = f"test_gen_from_bug.py"
    
    # analyze input data
    input_data = []
    for arg in args:
        if isinstance(arg, np.ndarray):
            input_data.append(arg)
    
    # generate test data code
    generate_data_code = ""
    for i, data in enumerate(input_data):
        if isinstance(data, np.ndarray) and data.size > 0:
            # calculate statistical properties
            mean = np.mean(data)
            std = np.std(data)
            shape = data.shape
            
            # calculate growth rate and trend information
            trend_info = []
            if data.size > 1:
                # calculate overall growth rate
                flattened = data.flatten()
                overall_growth = (flattened[-1] - flattened[0]) / (data.size - 1)
                trend_info.append(overall_growth)
            
            # generate code for random data
            generate_data_code += f"""
    # generate data with similar statistical properties to input {i}
    mean_{i} = {mean}
    std_{i} = {std}
    shape_{i} = {shape}
    
    # use normal distribution to generate random data
    np.random.seed({i + 42})  # use different seeds for reproducibility
    input_{i} = np.random.normal(mean_{i}, std_{i}, shape_{i})
    
    # if original data has specific growth trend, apply similar trend
    if {len(trend_info) > 0}:
        # apply similar overall growth trend
        growth_factor_{i} = {overall_growth if trend_info else 0}
        flattened_{i} = input_{i}.flatten()
        for j in range(1, len(flattened_{i})):
            flattened_{i}[j] = flattened_{i}[j-1] + growth_factor_{i} + np.random.normal(0, std_{i}/10)
        input_{i} = flattened_{i}.reshape(shape_{i})
    
    # ensure generated data has similar statistical properties
    input_{i} = (input_{i} - np.mean(input_{i})) / np.std(input_{i}) * std_{i} + mean_{i}
"""
    
    # generate test file content
    test_content = f"""
import pytest
import numpy as np

def test_power_function_bug():
    \"\"\"Test case generated automatically when power function failed\"\"\"
    # generate test data with similar statistical properties to the original input
{generate_data_code}
    
    # expected behavior should be
    # np.power requires 2 arguments: x1 and x2 (base and exponent)
    # adding a default exponent of 2 for the test case
    result = np.power(input_0, 2)
    
    # verify basic properties
    assert result is not None, "Result should not be None"
    assert isinstance(result, np.ndarray), "Result should be a numpy array"
    
    # verify result statistical properties are similar to input
    for i, input_array in enumerate([{', '.join([f'input_{i}' for i in range(len(input_data))])}]):
        # mean comparison not applicable for power function
        # instead check that values are properly squared
        assert np.allclose(result, input_array**2), "Power function did not correctly square the input"
        # additional verifications can be added as needed
"""
    # write test file
    with open(test_file_name, 'w') as f:
        f.write(test_content)
    
    print(f"\033[1;34m[INFO] Generated test file: {test_file_name}\033[0m")
    
    # raise original error
    raise ValueError("Simulated error in power function")

# dynamically replace numpy module ufuncs
for name in dir(np):
    obj = getattr(np, name)
    if isinstance(obj, np.ufunc):
        if name == "power":
            print(f"[DEBUG] Replacing ==>>>> ufunc: {name} with buggy version")
            setattr(np, name, buggy_power)
        else:
            print(f"[DEBUG] Replacing ==>>>> ufunc: {name}")
            setattr(np, name, ufunc_debug_wrapper(obj))
