#!/bin/bash

set -e -o pipefail
# python -m site

rm -rf np_op_dumps || true

unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_6.py"
python example_6.py

echo -e "\n CHANGED--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_6.py"
PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_6.py

# since the error above has already exited, the following needs to be executed manually
# echo -e "\n RUN TEST--------------------------------------------"
# PYTHONPATH="${PYTHONPATH}:$(pwd)" pytest -vv -s test_gen_from_bug.py