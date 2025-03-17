import numpy as np

# create a 1d array
arr = np.array([1, 2, 3, 4, 5])
print("arr: ", arr)

# create a 1d array
arr2 = np.array([-1, -2, -3, -4, -5])
print("arr2: ", arr2)

# plus
arr3 = np.add(arr, arr2)
print("arr3: ", arr3)

# subtract
arr4 = np.subtract(arr, arr2)
print("arr4: ", arr4)

# multiply
arr5 = np.multiply(arr, arr2)
print("arr5: ", arr5)

# divide
arr6 = np.divide(arr, arr2)
print("arr6: ", arr6)

# power
arr7 = np.power(arr, arr)
print("arr7: ", arr7)

# negative
arr8 = np.negative(arr)
print("arr8: ", arr8)

# positive
arr9 = np.positive(arr)
print("arr9: ", arr9)

# absolute
arr10 = np.absolute(arr2)
print("arr10: ", arr10)

# sqrt
arr11 = np.sqrt(arr)
print("arr11: ", arr11)

# square
arr12 = np.square(arr)
print("arr12: ", arr12)

# where
arr13 = np.where(arr > 3, arr, arr2)
print("arr13: ", arr13)