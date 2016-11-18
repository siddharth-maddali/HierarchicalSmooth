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

def _FastChainLinkSort( fe, tri ):
    MyDict = {}
    for Edge in fe:
        EdgeS = str( Edge[0] )
        while MyDict.has_key( EdgeS ):
            EdgeS += '.'
        MyDict[ EdgeS ] = Edge[1]
    MyList = []
    Key = MyDict.keys()[0]
    MyList.append( [ int( Key.strip( '.' ) ), MyDict[ Key ] ] )
    OldKey = Key
    Key = str( MyDict[ Key ] )
    del MyDict[ OldKey ]
    while len( MyDict ) > 0:
        Duplicates = [ i for i in MyDict.keys() if i.strip( '.' )==Key ]
        n = 0 
        if len( Duplicates ) > 1:
            TriangleWithThisEdge = set( [ list( i ) for i in tri if 
                int( OldKey.strip('.') ) in i and 
                int( Key ) in i 
            ][0] )
            while n < len( Duplicates ):
                TriangleWithNextEdge = set( [ list( i ) for i in tri if 
                    int( Duplicates[n].strip('.') ) in i and
                    MyDict[ Duplicates[n] ] in i
                ][0] )
                if len( TriangleWithThisEdge.intersection( TriangleWithNextEdge ) )==1:
                    break
                n += 1
        try:
            Key = Duplicates[n]
        except IndexError:
            Key = MyDict.keys()[0]
        MyList.append( [ int( Key.strip( '.' ) ), MyDict[ Key ] ] )
        OldKey = Key
        try:
            Key = str( MyDict[ Key ] )
        except KeyError:
            Key = MyDict.keys()[0]
        del MyDict[ OldKey ]
    return np.array( MyList )

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
    return np.array( AllEdges ), _FastChainLinkSort( FreeEdges, tri )

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

