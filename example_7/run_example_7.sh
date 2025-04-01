#!/bin/bash

set -e -o pipefail
# python -m site

rm -rf np_op_dumps || true

unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_7.py --dummy --arch resnet18 --batch-size 1 --print-freq 1"
python example_7.py --dummy --arch resnet18 --batch-size 1 --print-freq 1

echo -e "\n CHANGED 10 STEPS--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_7.py"
time PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_7.py --dummy --arch resnet18 --batch-size 1 --print-freq 1


echo -e "\n CHANGED 0 STEPS DRYRUN --------------------------------------------"
echo -e "\n set PYTHONPATH and dryrun MAX_TRAINING_STEPS=0 python example_7.py"
time PYTHONPATH="${PYTHONPATH}:$(pwd)" MAX_TRAINING_STEPS=0 python example_7.py --dummy --arch resnet18 --batch-size 1 --print-freq 1


# echo -e "\n RUN TEST--------------------------------------------"
# pytest -vv -s test_example_6.py
