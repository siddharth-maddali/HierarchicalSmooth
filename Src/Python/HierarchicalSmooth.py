import numpy as np
from scipy.sparse import diags, csc_matrix  # to create sparse diagonal matrices
from scipy.sparse.linalg import spsolve     # to solve sparse systems of equations

import Base as base                         # custom module containing ismember, etc.
import HierarchicalSmooth_PRIVATE as hspv   # private functions to make this code mode readable
import Triangulation as triang              # bare-bones version of Matlab's triangulation object

import copy                                 # to use deepcopy
import sys                                  # to write to output streams
import time

###################################################################################################


def Laplacian2D( N, type='serial' ):    # ...or type='cyclic'
    M = diags( [ np.ones( N-1 ) ], [ 1 ] ) - diags( [ np.ones( N ) ], [ 0 ] ).tolil()
    M = M.T * M
    if type=='serial':
        M[ -1, -1 ] = 1.
    elif type=='cyclic':
        M[ 0, 0 ] = 2.
        M[ 0, -1 ] = M[ -1, 0 ] = -1.
    else:
        sys.stderr.write( 'HierarchicalSmooth.Laplacian2D: Unrecognized type \'%s\'.\n' % type )
    return M.tocsc()

###################################################################################################

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

###################################################################################################

def Smooth( yInArray, fThreshold, nMaxIterations, L=None, nFixed=None ):

    N = yInArray.shape[0]
    if L==None:
        if nFixed==None or len( nFixed )==0:
            L = Laplacian2D( N )                                # serial with fixed endpoints
            nFixed = [ 0, N-1 ]
        else:
            L = Laplacian2D( N, 'cyclic' )

    nMobile = [ i for i in range( N ) if i not in nFixed ]  # cyclic with specified fixed points
    yIn = csc_matrix( yInArray )

    if len( nMobile ) < 1:
        return yIn.todense(), [], []

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

    fObj1, yOut = hspv._GetObjFn( fEps, fSmallEye, LRedTLRed, yIn, nMobile, LRedConst, D, AyIn )
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
        sys.stderr.write( 'HiererchicalSmooth.Smooth warning: Max. number of iterations reached.\n' )
    return yOut.todense(), IterData, nIterations

###################################################################################################

def DifferentiateFaces( TriangIn ):
    FB = TriangIn.freeBoundary() 
        # No need for chain-link sorting; this was already 
        # done on the creation of the Triangulation object.
    fblist = []
    start = FB[0,0]
    thissec = [ 0 ]
    n = 1
    while n < len( FB ):
        if FB[n,1]==start:  # end of current section
            thissec.append( n )
            fblist.append( thissec )
            thissec = []
        elif thissec==[]:   # start of new section
            start = FB[n,0]
            thissec.append( n )
        n += 1
    return FB, fblist

###################################################################################################

def HierarchicalSmooth( xPoints, tri, nFaceLabels, nNodeType, bPointSmoothed=None, sLogFile=None ):

    xSmoothed = copy.deepcopy( xPoints )

    if bPointSmoothed==None:
        bPointSmoothed = ( nNodeType%10==4 )    # following Dream3d convention.
            # quad points are considered already 'smoothed'
    sOut = sys.stdout
    if sLogFile != None:            # dump status to text file instead of stdout
        sys.stdout = open( sLogFile, 'w' )
   
    print 'Hashing interface elements (this may take some time)...',
    t0 = time.time()
    BoundaryDict = {}
    for i in range( len( nFaceLabels ) ):
        if nFaceLabels[i,0] > nFaceLabels[i,1]:
            nFaceLabels[i,0], nFaceLabels[i,1] = nFaceLabels[i,1], nFaceLabels[i,0]
            tri[i,0], tri[i,1] = tri[i,1], tri[i,0]
        try:
            BoundaryDict[ str( nFaceLabels[i] ) ].append( i )
        except KeyError:
            BoundaryDict[ str( nFaceLabels[i] ) ] = [ i ] # start new dictionary entry
    print '%s seconds. ' % str( time.time() - t0 )
    nUniqFaces = np.vstack( { tuple( row ) for row in nFaceLabels } )
    nCount = 1
    for GB in BoundaryDict.keys():
        print 'Interface %s: %d of %d...' % ( GB, nCount, len( nUniqFaces )  ), 
        t0 = time.time()
        triGB = tri[ BoundaryDict[ GB ], : ]
        pointGB = np.unique( triGB )
        triGB = np.array( base.ismember( triGB, pointGB )[1] ).reshape( -1, 3 )
        thisX = xPoints[ :, pointGB ]
        thisType = nNodeType[ pointGB ]
        thisSmoothed = bPointSmoothed[ pointGB ]
        
        T = triang.Triangulation( triGB, thisX )
        FB, fbList = DifferentiateFaces( T )
        print FB.shape, 
        print len( fbList ), 

        for thisFB in fbList:   # smoothing entire closed loop
            thisRange = FB[ thisFB[0]:thisFB[1]+1, 0 ]
            fixed = list( np.where( thisSmoothed[ thisRange ]==True )[0] )
            xLoop = Smooth( thisX[ :, thisRange ].T, 1.e-4, 2000, nFixed=fixed )[0].T
#            xLoop = Smooth( xLoop.T, 1.e-4, 2000, nFixed=fixed )[0].T
#            xLoop = Smooth( xLoop.T, 1.e-4, 2000, nFixed=fixed )[0].T
#            xLoop = Smooth( xLoop.T, 1.e-4, 2000, nFixed=fixed )[0].T
#            print xLoop
            thisX[ :, thisRange ] = xLoop
            bPointSmoothed[ pointGB ][ thisRange ] = True
        # with this loop, done smoothing all free boundaries in this interface.

        L = GraphLaplacian( triGB )[0]
        fixed = list( np.where( bPointSmoothed[ pointGB ]==True )[0] )
        thisXS = Smooth( thisX.T, 1.e-4, 2000, L, nFixed=fixed )[0].T
#        thisXS = Smooth( thisXS.T, 1.e-4, 2000, L, nFixed=fixed )[0].T
#        thisXS = Smooth( thisXS.T, 1.e-4, 2000, L, nFixed=fixed )[0].T
#        thisXS = Smooth( thisXS.T, 1.e-4, 2000, L, nFixed=fixed )[0].T
        xSmoothed[ :, pointGB ] = thisXS
        bPointSmoothed[ pointGB ] = True
        
        
        print '%s seconds. ' % str( time.time() - t0 ), 
        print np.where( bPointSmoothed==True )[0].size
        nCount += 1

    sys.stdout = sOut     # reset stdout
    return xSmoothed, bPointSmoothed

###################################################################################################
        
