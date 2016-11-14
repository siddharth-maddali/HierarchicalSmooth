import numpy as np
from scipy.sparse import diags, csc_matrix  # to create sparse diagonal matrices
from scipy.sparse.linalg import spsolve     # to solve sparse systems of equations

import Base as base                         # custom module containing ismember, etc.
import HierarchicalSmooth_PRIVATE as hspv   # private functions to make this code mode readable

import copy                                 # to use deepcopy
import sys                                  # to write to output streams

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
    return M.tocsc()

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
    return MLap.tocsc(), nUniq
    
def Smooth( yInArray, fThreshold, nMaxIterations, L=None, nFixed=None ):

    if L==None and nFixed==None:
        N = yInArray.shape[0]
        L = Laplacian2D( N )
        nFixed = [ 0, N-1 ]

    nMobile = [ i for i in range( N ) if i not in nFixed ]
    yIn = csc_matrix( yInArray )

    if len( nMobile ) < 1:
        return yIn, []

    IterData = []
    LRed = L[ :, nMobile ][ nMobile, : ]
    fConst = copy.deepcopy( L )
    fConst[ :, nMobile ] = 0
    fConst = ( fConst * yIn )[ nMobile, : ]
    D = L.multiply( L > 0. ) # diagonal matrix
    A = L.multiply( L < 0. ) # adjacency matrix
    AyIn = A * yIn
    fSmallEye = diags( [ np.ones( len( nMobile ) ) ], [ 0 ] )
    yMobile = yIn[ nMobile, : ]

    fEps = 0.5
    fStep = fEps/2.
    nIterations = 1
    LRedTLRed = LRed.T * LRed
    LRedConst = LRed.T * fConst

    fObj1 = hspv._GetObjFn( fEps, fSmallEye, LRedTLRed, yIn, nMobile, LRedConst, D, AyIn )[0]
    fObj2 = hspv._GetObjFn( fEps+fThreshold, fSmallEye, LRedTLRed, yIn, nMobile, LRedConst, D, AyIn )[0]
    IterData.append( [ fEps, fObj1 ] )

    fSlope = ( fObj2 - fObj1 ) / fThreshold
    while abs( fSlope ) > fThreshold and nIterations < nMaxIterations:
        if fSlope > 0.:
            fEps -= fStep
        else:
            fEps += fStep

        fStep /= 2.
        fObj1, yOut = hspv._GetObjFn( fEps, fSmallEye, LRedTLRed, yIn, nMobile, LRedConst, D, AyIn )
        fObj2 = hspv._GetObjFn( fEps+fThreshold, fSmallEye, LRedTLRed, yIn, nMobile, LRedConst, D, AyIn )[0]

        fSlope = ( fObj2 - fObj1 ) / fThreshold
        IterData.append( [ fEps, fObj1 ] )
        nIterations += 1

    if nIterations == nMaxIterations:
        sys.stderr.write( 'Smooth warning: Max. number of iterations reached.\n' )
    return yOut, IterData, nIterations

def ExtractFace( triFull, SeedArray ):
    nPrevSize = 0
    triFace = triFull[ np.where( np.sum( base.ismember( triFull, SeedArray )[0], axis=1 ) > 1. )[0] , : ]
    nNextSize = triFace.shape[0]
    while nNextSize != nPrevSize:
        nPrevSize = nNextSize
        SeedArray = np.unique( triFace )
        triFace = triFull[ np.where( np.sum( base.ismember( triFull, SeedArray )[0], axis=1 ) > 1. )[0] , : ]
        nNextSize = triFace.shape[0]

    return triFace




        









