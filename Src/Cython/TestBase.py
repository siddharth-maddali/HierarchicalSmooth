import numpy as np

arr  = np.random.permutation( 100000 )[ :10000 ].reshape( -1, 2 )
arr2 = np.random.permutation( 100000 )[ :5000  ].reshape( -1, 1 )

print arr.shape
print arr2.shape

import Base as b0
import Base_1_c as b1c
import Base_1_cpp as b1cpp

%timeit x, y = b0.ismember( arr, arr2 )
%timeit x, y = b1c.ismember( arr, arr2 )
%timeit x, y = b1cpp.ismember( arr, arr2 )
