# Simple conversion to Cython from Python module, without optimization measures.

import numpy as np
import sys
from scipy.sparse import csc_matrix

# intermediate definitions

def __ismember_rows( Array1, Array2 ):
    l1 = [ list( i ) for i in Array1 ]
    l2 = [ list( i ) for i in Array2 ]
    out1 = [ i in l2 for i in l1 ]
    xloc = list( np.where( out1 )[0] )
    out2 = [ list( np.where( np.array(l2)==l1[i] )[0] )[0] for i in xloc ]
    return out1, out2

def __ismember_list( Array1, Array2 ):
    temp1 = Array1.ravel().reshape( -1, 1 )
    temp2 = Array2.ravel().reshape( -1, 1 )
    sol, idx = __ismember_rows( temp1, temp2 )
    sol = np.array( sol ).reshape( -1, Array1.shape[1] )
    return sol, idx

"""
    ISMEMBER -- mimics the functionality of the ismember function 
    in Matlab, although in a limited manner. Only optional kwarg 
    (for now) is 'rows'.
"""
def ismember( Array1, Array2, comparison_type='list' ):
    if comparison_type=='list': 
        return __ismember_list( Array1, Array2 )
    
    elif comparison_type=='rows':
        return __ismember_rows( Array1, Array2 )
    
    else:
        sys.stderr.write( "'ismember' error: invalid comparison type.\n" );
        return [], []

