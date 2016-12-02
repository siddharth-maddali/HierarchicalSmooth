#   Copyright (c) 2016, Siddharth Maddali 
#   All rights reserved. 
#   
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met: 
#   
#    * Redistributions of source code must retain the above copyright notice, 
#      this list of conditions and the following disclaimer. 
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in the 
#      documentation and/or other materials provided with the distribution. 
#    * Neither the name of Carnegie Mellon University nor the names of its 
#      contributors may be used to endorse or promote products derived from 
#      this software without specific prior written permission. 
#   
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
#   POSSIBILITY OF SUCH DAMAGE. 
#   
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

def _FastChainLinkSort( fe ):
    TrgDict = {}
    for Edge in fe: # hashing edges...
        try:
            TrgDict[ Edge[0] ].append( Edge[1] )
        except KeyError:
            TrgDict[ Edge[0] ] = [ Edge[1] ] # create new list
    List = np.zeros( ( len( fe ), len( fe[0] ) ), dtype=int )
    Key = TrgDict.keys()[0]
    for i in range( List.shape[0] ):
        List[i,0], List[i,1] = Key, TrgDict[ Key ][-1]
        NewKey = TrgDict[ Key ][-1]
        TrgDict[ Key ].pop()
        if len( TrgDict[ Key ] ) == 0:
            del TrgDict[ Key ]
        if TrgDict.has_key( NewKey ):
            Key = NewKey
        elif len( TrgDict ) > 0:
            Key = TrgDict.keys()[0]

    return List

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
    return np.array( AllEdges ), _FastChainLinkSort( FreeEdges )

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

