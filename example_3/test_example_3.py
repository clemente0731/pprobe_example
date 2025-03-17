import os
import numpy as np
import pytest


def get_dump_files():
    """get the dump files from np_add_dumps directory with fixed filenames"""
    if not os.path.exists("np_add_dumps"):
        pytest.skip("np_add_dumps directory does not exist")
    
    # use fixed filenames as shown in the directory listing
    input1_file = "np_add_dumps/input1_example_3.npy"
    input2_file = "np_add_dumps/input2_example_3.npy"
    output_file = "np_add_dumps/output_example_3.npy"
    
    # check if all files exist
    if not os.path.exists(input1_file) or not os.path.exists(input2_file) or not os.path.exists(output_file):
        pytest.skip("one or more required dump files not found in np_add_dumps directory")
    
    return {
        "input1": input1_file,
        "input2": input2_file,
        "output": output_file
    }


def test_numpy_add_hook():
    """test that numpy add hook works correctly"""
    # get the dump files
    files = get_dump_files()
    
    # load the arrays
    input1 = np.load(files["input1"])
    input2 = np.load(files["input2"])
    expected_output = np.load(files["output"])
    
    # compute the actual output using numpy add
    actual_output = np.add(input1, input2)
    
    # check if the outputs are equal
    np.testing.assert_array_equal(actual_output, expected_output)
    
    print(f"Test passed! Verified files:")
    print(f"  - Input 1: {files['input1']}")
    print(f"  - Input 2: {files['input2']}")
    print(f"  - Output: {files['output']}")