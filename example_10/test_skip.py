###
import numpy as np

# Usage:
# 1. Run tests normally first:
#    pytest -vv test_skip.py
#
# 2. Skip previously passed tests by setting environment variable:
#    PYTEST_SKIP_PREVIOUSLY_PASSED="test_skip.py::test_power" PYTHONPATH="${PYTHONPATH}:$(pwd)" pytest -vv -s test_skip.py

def test_add():
    """test numpy add operation"""
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    result = np.add(a, b)
    print("add result:", result)


def test_subtract():
    """test numpy subtract operation"""
    a = np.array([10, 20, 30])
    b = np.array([5, 10, 15])
    result = np.subtract(a, b)
    print("subtract result:", result)


def test_multiply():
    """test numpy multiply operation"""
    a = np.array([2, 3, 4])
    b = np.array([5, 6, 7])
    result = np.multiply(a, b)
    print("multiply result:", result)


def test_divide():
    """test numpy divide operation"""
    a = np.array([10, 20, 30])
    b = np.array([2, 5, 10])
    result = np.divide(a, b)
    print("divide result:", result)


def test_power():
    """test numpy power operation"""
    a = np.array([2, 3, 4])
    b = np.array([2, 2, 2])
    result = np.power(a, b)
    print("power result:", result)


def test_sin():
    """test numpy sin operation"""
    angles = np.array([0, np.pi/2, np.pi])
    result = np.sin(angles)
    print("sin result:", result)


def test_cos():
    """test numpy cos operation"""
    angles = np.array([0, np.pi/2, np.pi])
    result = np.cos(angles)
    print("cos result:", result)


def test_exp():
    """test numpy exp operation"""
    a = np.array([0, 1, 2])
    result = np.exp(a)
    print("exp result:", result)


def test_log():
    """test numpy log operation"""
    a = np.array([1, 10, 100])
    result = np.log(a)
    print("log result:", result)


def test_matmul():
    """test numpy matrix multiplication"""
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    result = np.matmul(a, b)
    print("matmul result:", result)


if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
    test_power()
    test_sin()
    test_cos()
    test_exp()
    test_log()
    test_matmul()
