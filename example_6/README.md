# NumPy Operation Monitoring and Automatic Test Generation System

This project demonstrates how to implement monitoring and interception of NumPy operations through Python and NumPy's dispatch mechanism, and automatically generate test cases when errors occur, reducing debugging costs for end-to-end testing.

## Core Concept

By leveraging Python's `site` module loading mechanism and NumPy's dispatch mechanism, we can monitor NumPy operations without modifying existing code, and capture critical states when errors occur to automatically generate reproducible unit tests.

### Key Components

1. **site Module Loading Mechanism**:
   - `sitecustomize.py`: Module automatically loaded when Python starts, globally effective
   - Control whether to enable the monitoring system through the `PYTHONPATH` environment variable

2. **NumPy Dispatch Mechanism**:
   - `np.ufunc` - Handles basic mathematical operations (such as addition, subtraction, multiplication, division, etc.)
   - Implement monitoring and error capturing by replacing these functions

## Implementation Method

This system implements error capturing and test generation through the following methods:

1. **Decorator Pattern**: Using wrapt decorators to wrap all NumPy ufunc operations
2. **Error Simulation and Capture**: Simulate errors for specific functions (such as power) and capture states
3. **Automatic Test Generation**: Automatically generate pytest test cases based on captured input data

## Benefits for End-to-End Testing

When end-to-end tests encounter errors, this system:

1. **Captures Input State**: Records the exact input data that caused the error
2. **Generates Statistical Profiles**: Analyzes input data patterns and statistical properties
3. **Creates Reproducible Tests**: Automatically writes pytest files that reproduce the error
4. **Reduces Debug Time**: Eliminates the need to recreate complex test environments
5. **Preserves Context**: Maintains information about the error context for easier debugging

## Example Usage

The example demonstrates a simulated error in NumPy's power function:

1. The system intercepts the error during normal execution
2. It analyzes the input data that caused the failure
3. It automatically generates a test file (`test_gen_from_bug.py`)
4. The generated test contains:
   - Statistically similar test data
   - Expected behavior assertions
   - Proper test structure for pytest

This approach significantly reduces the time needed to debug complex end-to-end tests by providing isolated, reproducible test cases that focus specifically on the failing component.
