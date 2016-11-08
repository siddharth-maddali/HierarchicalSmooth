import numpy as np
import sys

"""
    ISMEMBER -- mimics the functionality of the ismember function 
    in Matlab, although in a limited manner. Only optional kwarg 
    (for now) is 'rows'.
"""
def ismember( Array1, Array2, comparison_type='default' ):
    if comparison_type=='default': 
        myset = set( Array2.ravel() )
        return np.array( [ [ i in set( Array2.ravel() ) for i in j ] for j in Array1 ] )
    
    elif comparison_type=='rows':
        return np.array( [ [ i  in Array2[:,j].ravel() for i in Array1[:,j] ] for j in range( 0, Array1.shape[1] ) ] ).all( axis=0 )
    
    else:
        sys.stderr.write( "'ismember' error: invalid comparison type.\n" );
        return []
