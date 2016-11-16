import numpy as np


class _SortObject:
    def __init__( self, MyOrig ):
        self.orig = MyOrig
        self.count = 1

def __SortMinMax( arr ):
    return np.concatenate( 
        ( 
            np.min( arr, axis=1 ).reshape( -1, 1 ), 
            np.max( arr, axis=1 ).reshape( -1, 1 )
        ), 
        axis=1 
    )

def _GetEdges( tri ):
    MyEdges = np.concatenate( ( tri[:,[ 0, 1 ] ], tri[:,[ 1, 2 ] ], tri[:,[ 2, 0 ] ] ), axis=0 )
    MyEdgesSorted = __SortMinMax( MyEdges )
    MyDict = {}
    for i in range( len( MyEdgesSorted ) ):
        MyKey = str( MyEdgesSorted[i] ).strip( '[]' )
        try:
            MyDict[ MyKey ].count += 1
        except KeyError: # if entry not found, create new one.
            MyDict[ MyKey ] = _SortObject( MyEdges[i] )
    AllEdges = []
    FreeEdges = []
    for i in MyDict.keys():
        AllEdges.append( MyDict[i].orig )
        if MyDict[i].count == 1:
            FreeEdges.append( MyDict[i].orig )
    return np.array( AllEdges ), np.array( FreeEdges )

class Triangulation:
    def __init__( self, MyTri, X ):
        self.faces = MyTri
        self.vertices = X
        self.edges, self.freeboundary = _GetEdges( MyTri )

    def connectivityList( self ):
        return self.faces

    def freeBoundary( self ):
        return self.freeboundary

    def edges( self ):
        return self.edges

