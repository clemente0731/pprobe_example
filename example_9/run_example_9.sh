#!/bin/bash

set -e -o pipefail
# python -m site

rm -rf np_op_dumps || true

unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_9.py "
python example_9.py

echo -e "\n install jax jaxlib --------------------------------------------"
pip install jax jaxlib -q > /dev/null 2>&1 || true

echo -e "\n CHANGED--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_9.py"
PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_9.py
