import numpy as np

def FastChainLinkSort( FBIn ):
    FBOut = FBIn
    for i in range( 1, FBOut.shape[0] ):
        f = np.where( np.any( FBOut[i:,:]==FBOut[i-1,1], axis=1 ) )[0]
        FBOut[ [ i, f+i ], : ] = FBOut[ [ f+i, i ], : ]
        if FBOut[ i,1 ] == FBOut[ i-1,1 ]:
            FBOut[ i, [ 0, 1 ] ] = FBOut[ i, [ 1, 0 ] ]
    return FBOut
