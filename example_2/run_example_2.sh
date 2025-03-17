#!/bin/bash

# python -m site


unset PYTHONPATH
echo -e "\n ORIGIN --------------------------------------------"
echo -e "\n unset PYTHONPATH and run python example_2.py"
python example_2.py

echo -e "\n CHANGED--------------------------------------------"
echo -e "\n set PYTHONPATH and run python example_2.py"
PYTHONPATH="${PYTHONPATH}:$(pwd)" python example_2.py