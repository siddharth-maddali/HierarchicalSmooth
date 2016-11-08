import numpy as np
from scipy.sparse import diags

def FastChainLinkSort( FBIn ):
    FBOut = FBIn
    for i in range( 1, FBOut.shape[0] ):
        f = np.where( np.any( FBOut[i:,:]==FBOut[i-1,1], axis=1 ) )[0]
        FBOut[ [ i, f+i ], : ] = FBOut[ [ f+i, i ], : ]
        if FBOut[ i,1 ] == FBOut[ i-1,1 ]:
            FBOut[ i, [ 0, 1 ] ] = FBOut[ i, [ 1, 0 ] ]
    return FBOut

def Laplacian2D( N ):
    M = diags( [ np.ones( N-1 ) ], [ 1 ] ) - diags( [ np.ones( N ) ], [ 0 ] )
    M = M.T * M
    M[ -1, -1 ] = 1.
    return M
