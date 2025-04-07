#!/bin/bash
# clean python build artifacts using setup.py

# check if setup.py exists
echo "Cleaning build artifacts using setup.py..."
python setup.py clean --all || true

# clean build directory
if [ -d "build" ]; then
    echo "Removing build directory..."
    find build -type f -delete
    find build -type d -empty -delete
fi

# clean dist directory
if [ -d "dist" ]; then
    echo "Removing dist directory..."
    find dist -type f -delete
    find dist -type d -empty -delete
fi

rm -rf hook_package_demo.egg-info || true

# clean __pycache__ directories
find . -type d -name "__pycache__" | while read dir; do
    echo "Cleaning $dir..."
    find "$dir" -type f -delete
    find "$dir" -type d -empty -delete
done

# clean .pyc files
find . -name "*.pyc" -delete

echo "Clean completed successfully"