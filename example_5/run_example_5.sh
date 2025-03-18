#!/bin/bash

# python -m site


unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_5.py"
python example_5.py

echo -e "\n CHANGED--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_5.py"
PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_5.py

echo -e "\n RUN TEST--------------------------------------------"
pytest -vv -s test_example_5.py
