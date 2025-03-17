print("start ==> example_2/sitecustomize.py")


# replace numpy.add with numpy.subtract in sitecustomize.py

import numpy as np
np.add = np.subtract
print("\033[1;32m\tnp.add is now replaced with np.subtract: \033[0m", np.add)
print("\033[1;33m\tThis means all np.add operations will perform subtraction instead\033[0m")


print("end ==> example_2/sitecustomize.py")