import os
import numpy as np
import pytest
from pathlib import Path

# Constants
DUMP_DIR = "np_op_dumps"
RTOL = 1e-5
ATOL = 1e-5

class TestNumpyOperations:
    """Test suite for NumPy operations using golden reference values."""
    
    @staticmethod
    def get_operation_files():
        """Get all operation files from dump directory and group them by operation."""
        if not os.path.exists(DUMP_DIR):
            pytest.skip(f"Dump directory {DUMP_DIR} does not exist")
        
        # Dictionary to store operation files
        op_files = {}
        
        # Get all files in dump directory
        files = list(Path(DUMP_DIR).glob("*.npy"))
        
        # Group files by operation
        for file_path in files:
            file_name = file_path.name
            parts = file_name.split("_")
            if len(parts) >= 2:
                op_name = parts[1]
                if op_name not in op_files:
                    op_files[op_name] = []
                op_files[op_name].append(file_path)
        
        return op_files
    
    @staticmethod
    def get_operation_data(op_name, op_files):
        """Get input and output data for a specific operation."""
        # Filter files for this operation
        files = [f for f in op_files if f.name.startswith(f"op_{op_name}_")]
        
        # Separate input and output files
        input_files = sorted([f for f in files if "input" in f.name], 
                             key=lambda x: int(x.name.split("input")[1].split("_")[0]))
        output_files = [f for f in files if "output" in f.name]
        
        if not input_files or not output_files:
            return None, None
        
        # Load input data
        inputs = [np.load(str(f)) for f in input_files]
        
        # Load output data (golden reference)
        output = np.load(str(output_files[0]))
        
        return inputs, output
    
    @pytest.fixture(scope="class")
    def operation_files(self):
        """Fixture to provide operation files."""
        return self.get_operation_files()
    
    @pytest.fixture(scope="class")
    def operations(self, operation_files):
        """Fixture to provide operation names."""
        return list(operation_files.keys())
    
    @pytest.mark.parametrize("op_name", [
        "add", "subtract", "multiply", "divide", "power",
        "negative", "positive", "absolute", "sqrt", "square", "where"
    ])
    def test_numpy_operation(self, op_name, operation_files):
        """Test NumPy operations against golden reference values."""
        # Skip if operation not found in dump files
        if op_name not in operation_files:
            pytest.skip(f"Operation {op_name} not found in dump files")
        
        # Get input and output data for this operation
        inputs, expected_output = self.get_operation_data(op_name, operation_files[op_name])
        
        if inputs is None or expected_output is None:
            pytest.skip(f"No data found for operation {op_name}")
        
        # Get the NumPy function for this operation
        np_func = getattr(np, op_name)
        
        # Call the function with inputs
        actual_output = np_func(*inputs)
        
        # Compare actual output with expected output
        np.testing.assert_allclose(
            actual_output, expected_output, 
            rtol=RTOL, atol=ATOL,
            err_msg=f"Output mismatch for operation {op_name}"
        )
        
        # print detailed information about input files, output file and comparison
        print(f"\033[1;32m✓ Test passed for NumPy operation: \033[1;36m{op_name}\033[0m")
        print(f"  - Input files: {[f.name for f in operation_files[op_name] if 'input' in f.name]}")
        print(f"  - Golden reference file: {[f.name for f in operation_files[op_name] if 'output' in f.name][0]}")
        print(f"\033[1;33m   - Expected output: {expected_output} \033[0m")
        print(f"\033[1;33m   - Actual output: {actual_output} \033[0m")
        print(f"- Comparison result: Actual output matches expected golden reference")