import numpy as np
import math
a = np.array([[3, 3, 3],[2,2,2],[1,1,1]])
b = np.array([1, 1, 1])
matres = (a - b)**2
a = np.concatenate(a,b)
print a