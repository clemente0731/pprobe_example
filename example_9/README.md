# Example 9: Performance Optimization with Python Hooks

This example demonstrates how to use Python hooks via `sitecustomize.py` to optimize NumPy operations by transparently replacing them with JAX implementations.

## Overview

The example shows how to intercept NumPy imports and redirect them to JAX equivalents without modifying application code, providing significant performance improvements for numerical computations.

## Files in this Example

- `example_9.py` - Demonstration script with intensive NumPy computations
- `sitecustomize.py` - Hook implementation that replaces NumPy with JAX.numpy
- `run_example_9.sh` - Shell script to run the example with and without the optimization

## How it Works

When Python starts, `sitecustomize.py` is automatically imported and:

1. Checks if NumPy has already been imported
2. If not, creates a proxy module that redirects NumPy calls to JAX.numpy when possible
3. Falls back to original NumPy for unsupported operations

## Running the Example
