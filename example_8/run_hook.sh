#!/usr/bin/bash

hook_package_demo --list


hook_package_demo --reset
hook_package_demo --enable HOOK_A,HOOK_B,HOOK_C
echo "-------------------------------- python -c hello with HOOK_A,HOOK_B,HOOK_C --------------------------------"
python -c "print('hello, world')"

hook_package_demo --reset
hook_package_demo --enable HOOK_A,HOOK_C
echo "-------------------------------- python -c hello with HOOK_A,HOOK_C --------------------------------"
python -c "print('hello, world')"

hook_package_demo --reset
hook_package_demo --enable HOOK_NUMPY
echo "-------------------------------- python -c numpy --------------------------------"
python -c "import numpy; print(numpy.add(1, 2))"


echo "-------------------------------- subprocess python -c numpy --------------------------------"
python -c "import subprocess; subprocess.run(['python', '-c', 'import numpy; print(numpy.add(1, 2))'], check=True)"