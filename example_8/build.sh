#!/bin/bash

# 1. build the package
echo "Building package..."
python -m pip uninstall hook_package_demo -y || true
python setup.py bdist_wheel
