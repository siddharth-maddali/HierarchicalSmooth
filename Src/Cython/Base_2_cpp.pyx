# Adding basic static typing to core Python routines. 
from __future__ import division

import numpy as np
import sys
from scipy.sparse import csc_matrix

# compile time information 
cimport numpy as np
#cimport sys
#from scipy.sparse cimport csc_matrix

# intermediate definitions
DTYPE = np.float
ctypedef np.float_t DTYPE_t

def __ismember_rows( np.ndarray Array1, np.ndarray Array2 ):
    cdef list l1 = [ list( i ) for i in Array1 ]
    cdef list l2 = [ list( i ) for i in Array2 ]
    cdef list out1 = [ i in l2 for i in l1 ]
    cdef list xloc = list( np.where( out1 )[0] )
    cdef list out2 = [ list( np.where( np.array(l2)==l1[i] )[0] )[0] for i in xloc ]
    return out1, out2

def __ismember_list( np.ndarray Array1, np.ndarray Array2 ):
    cdef np.ndarray temp1 = Array1.ravel().reshape( -1, 1 )
    cdef np.ndarray temp2 = Array2.ravel().reshape( -1, 1 )
#    cdef list idx
#    cdef list sol
#    sol, idx = __ismember_rows( temp1, temp2 )
    return __ismember_rows( temp1, temp2 )

"""
    ISMEMBER -- mimics the functionality of the ismember function 
    in Matlab, although in a limited manner. Only optional kwarg 
    (for now) is 'rows'.
"""
def ismember( np.ndarray Array1, np.ndarray Array2, str comparison_type='list' ):
    if comparison_type=='list': 
        print 'Chosen list.'
        return __ismember_list( Array1, Array2 )
    
    elif comparison_type=='rows':
        print 'Chosen rows.'
        return __ismember_rows( Array1, Array2 )
    
    else:
        sys.stderr.write( "'ismember' error: invalid comparison type.\n" );
        return [], []

