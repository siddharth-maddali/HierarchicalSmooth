#   Copyright (c) 2016-2018, Siddharth Maddali 
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

import matplotlib.pyplot as plt
from matplotlib import rc
rc( 'text', usetex=True )

from scipy.spatial import Delaunay
import gc

import Triangulation as tr

nPerimeterPoints = 100
nInteriorPoints = 2000
nRemovable = 100

th = np.linspace( 0., 2.*np.pi, nPerimeterPoints+1 )[:-1]

X = np.concatenate( 
    ( np.cos( th ).reshape( 1, -1 ), np.sin( th ).reshape( 1, -1 ) ), 
    axis=0 )
r = np.sqrt( 2. * np.random.rand( nInteriorPoints ) )
th2 = 2. * np.pi * np.random.rand( nInteriorPoints )
Y = np.concatenate( ( 
    ( r * np.cos( th2 ) ).reshape( 1, -1 ), 
    ( r * np.sin( th2 ) ).reshape( 1, -1 ) ), 
    axis=0 )

P = np.concatenate( ( X, Y ), axis=1 )
P = P[ :, np.random.permutation( P.shape[1] ) ]

tri = Delaunay( P.T ).simplices

#nRemovedPoints =  np.random.permutation( P.shape[1]  )[ :nRemovable ]
nRemovedPoints = np.where( 
    np.logical_or( 
        ( P[0]-0.5 )**2/0.0225 + ( P[1]-0.5 )**2/0.09 < 1., 
        ( P[0]+0.5 )**2/0.09 + ( P[1]+0.5 )**2/0.0225 < 1.
    )
)[0]


tri2 = np.array( [ 
        list( i ) for i in tri if 
        i[0] not in nRemovedPoints and 
        i[1] not in nRemovedPoints and 
        i[2] not in nRemovedPoints
    ] )


### This is the bit of code being tested ######

T = tr.Triangulation( tri2, P )
FB = T.freeBoundary()

###############################################

print 'Free boundary segments = ' + str( len( FB ) )

V = P[ :, FB[:,1] ] - P[ :, FB[:,0] ]

plt.clf()

plt.triplot( P[0], P[1], tri2, label='Surface triangulation' )
plt.quiver( 
        P[ 0, FB[:,0] ], P[ 1, FB[:,0] ], 
        V[0], V[1], 
        units='xy', scale=1., headaxislength=4., width=0.005,
        color='r',
        label='Free boundaries' )

plt.title( r'Test of routine \texttt{Triangulation.\_FastChainLinkSort}' )
plt.axis( 'equal' )
plt.legend( loc='best' )
plt.grid( which='both' )
plt.show()

gc.collect()
