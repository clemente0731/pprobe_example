
# Hook Package Demo

## Introduction

This example demonstrates how to implement and manage toggleable hooks. Hooks are a technique for inserting custom code during program execution, allowing for extension or modification of program behavior without changing the original code.

1. **Hook Mechanism Design**
   - Demonstrates how to design a simple hook system

2. **Configuration Management**
   - Controls the activation status of different hooks through the `hook.toggle.default` file

3. **Modular Hooks**
   - Each hook as an independent module for easier maintenance and extension

4. **Dynamic Loading**
   - Dynamically loads and executes hooks based on configuration

## Hook Types

This example contains several hook types:

1. **Basic Hooks**: a_hook, b_hook, c_hook
   - Demonstrates basic hook implementation

2. **Functional Hooks**: numpy_hook
   - Shows how to integrate third-party library functionality


# Running Examples

The following demonstrates the basic usage and examples of the hook_package_demo tool, showing how to manage and test different hooks.

## Basic Commands

### List All Available Hooks

View all available hooks in the system:

```bash
hook_package_demo --list
```

### Reset and Enable Hooks

Reset all hook states, then enable specified hooks:

```bash
# Reset all hook states
hook_package_demo --reset

# Enable specific hooks
hook_package_demo --enable HOOK_NAME1,HOOK_NAME2
```

## Usage Examples

### Example 1: Enable Multiple Basic Hooks

```bash
# Reset all hooks
hook_package_demo --reset

# Enable HOOK_A, HOOK_B, and HOOK_C
hook_package_demo --enable HOOK_A,HOOK_B,HOOK_C

# Test hook effects
echo "-------------------------------- python -c hello with HOOK_A,HOOK_B,HOOK_C --------------------------------"
python -c "print('hello, world')"
```

### Example 2: Selectively Enable Hooks

```bash
# Reset all hooks
hook_package_demo --reset

# Enable only HOOK_A and HOOK_C
hook_package_demo --enable HOOK_A,HOOK_C

# Test hook effects
echo "-------------------------------- python -c hello with HOOK_A,HOOK_C --------------------------------"
python -c "print('hello, world')"
```

### Example 3: Enable NumPy Related Hooks

```bash
# Reset all hooks
hook_package_demo --reset

# Enable NumPy related hooks
hook_package_demo --enable HOOK_NUMPY

# Test NumPy operations
echo "-------------------------------- python -c numpy --------------------------------"
python -c "import numpy; print(numpy.add(1, 2))"
```

### Example 4: Hook Effects in Subprocesses

Test hook behavior in subprocesses:

```bash
echo "-------------------------------- subprocess python -c numpy --------------------------------"
python -c "import subprocess; subprocess.run(['python', '-c', 'import numpy; print(numpy.add(1, 2))'], check=True)"
```

## Notes

- Use the `--reset` command to ensure a clean hook state before each test
- Separate multiple hook names with commas and no spaces
- Make sure the hook_package_demo package is properly installed before testing
