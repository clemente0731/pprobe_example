#!/bin/bash

# python -m site


unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_4.py"
python example_4.py

echo -e "\n CHANGED--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_4.py"
PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_4.py

echo -e "\n RUN TEST--------------------------------------------"
pytest -vv -s test_example_4.py
