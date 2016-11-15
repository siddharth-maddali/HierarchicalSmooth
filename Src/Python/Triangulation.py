import numpy as np

def __SortMinMax( arr ):
    return np.concatenate( 
        ( 
            np.min( arr, axis=1 ).reshape( -1, 1 ), 
            np.max( arr, axis=1 ).reshape( -1, 1 )
        ), 
        axis=1 
    )

def __GetEdges( tri ):
    MyEdges = np.concatenate( 
        ( 
            __SortMinMax( tri[:,[ 0, 1 ] ] ), 
            __SortMinMax( tri[:,[ 1, 2 ] ] ), 
            __SortMinMax( tri[:,[ 2, 0 ] ] )
        ), 
        axis=0 
    )
    MyDict = { str( i ).strip( '[]' ):0 for i in MyEdges }
    for i in MyEdges: MyDict[ str( i ).strip( '[]' ) ] += 1
    AllEdges  = np.array( [ [ int( j ) for j in i.split() ] for i in MyDict.keys() ] )
    FreeEdges = np.array( [ [ int( j ) for j in i.split() ] for i in MyDict.keys() if MyDict[i]==1 ] )
    return AllEdges, FreeEdges


class Triangulation:
    def __init__( self, MyTri, X ):
        self.faces = MyTri
        self.vertices = X
        self.edges, self.freeboundary = __GetEdges( MyTri )

    def connectivityList( self ):
        return self.faces

    def freeBoundary( self ):
        return self.freeboundary

    def edges( self ):
        return self.edges

