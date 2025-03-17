#!/bin/bash

# python -m site


unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_3.py"
python example_3.py

echo -e "\n CHANGED--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_3.py"
PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_3.py

echo -e "\n RUN TEST--------------------------------------------"
pytest test_example_3.py
