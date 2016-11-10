import numpy as np
from scipy.sparse import diags
import Base as base

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

def GraphLaplacian( tri ):
    nUniq = np.unique( tri )
    nIdx = range( nUniq.size )
    nSubTri = np.array( base.ismember( tri, nUniq )[1] ).reshape( -1, tri.shape[1] )
    MLap = diags( [ np.zeros( nUniq.size ) ], [ 0 ] ).tolil()    # linked list sparse matrix
    for i in range( nSubTri.shape[0] ):
        for j in range( 3 ):
            l = ( j + 3 ) % 3
            m = ( j + 4 ) % 3 
            n = ( j + 5 ) % 3
            MLap[ nSubTri[i,l], nSubTri[i,m] ] = -1
            MLap[ nSubTri[i,l], nSubTri[i,n] ] = -1
    for i in range( MLap.shape[0] ):
        MLap[ i, i ] = -MLap[i,:].sum()
    return MLap, nUniq
    
#    def Smooth( yIn, fThreshold, nMaxIterations, L=None, nFixed=None ):
        









