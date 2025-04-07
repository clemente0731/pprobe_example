import numpy as np
import time
import os

def compute_intensive_operation():
    """
    perform a computationally intensive numpy operation
    """
    print("Starting intensive numpy computation...")
    start_time = time.time()
    
    # create large matrices
    size = 2000
    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)
    
    # perform multiple matrix operations
    for i in range(50):
        # matrix multiplication
        result = np.matmul(matrix_a, matrix_b)
        
        # additional operations
        result = np.sin(result) + np.cos(result)
        result = np.exp(np.clip(result, -10, 10) * 0.01)
        
        # update matrix_a for next iteration
        matrix_a = result / np.linalg.norm(result)
    
    elapsed_time = time.time() - start_time
    print(f"Computation completed in {elapsed_time:.2f} seconds")
    print(f"Result shape: {result.shape}, Mean value: {np.mean(result):.6f}")
    
    return result

if __name__ == "__main__":
    compute_intensive_operation()