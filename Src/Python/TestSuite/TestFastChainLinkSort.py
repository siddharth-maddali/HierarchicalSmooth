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

import matplotlib.pyplot as plt
from matplotlib import rc
rc( 'text', usetex=True )

from scipy.spatial import Delaunay
import gc

import Triangulation as tr

nInside = 20
nOutside = 40
nBetween = 250

th1 = np.linspace( 0, 2.*np.pi, nInside+1 )[:-1]
th2 = np.linspace( 0, 2.*np.pi, nOutside+1 )[:-1]
th = 2. * np.pi * np.random.rand( nBetween )
r = 1. + np.random.rand( nBetween )

X = np.concatenate( ( np.cos( th1 ).reshape( 1, -1 ), np.sin( th1 ).reshape( 1, -1 ) ), axis=0 )
Y = 2. * np.concatenate( ( np.cos( th2 ).reshape( 1, -1 ), np.sin( th2 ).reshape( 1, -1 ) ), axis=0 )
Z = np.concatenate( ( ( r*np.cos( th ) ).reshape( 1, -1 ), ( r*np.sin( th ) ).reshape( 1, -1 ) ), axis=0 )

P = np.concatenate( ( X, Y, Z ), axis=1 )
tri = Delaunay( P.T ).simplices

trilist = [ list( i ) for i in tri ]
tri2 = np.array( 
    [ i for i in trilist if 
        i[0] >= nInside or i[1] >= nInside or i[2] >= nInside ]
)

### This is the bit of code being tested ######

T = tr.Triangulation( tri2, P )
FB = T.freeBoundary()

###############################################

V = P[ :, FB[:,1] ] - P[ :, FB[:,0] ]

plt.clf()

plt.triplot( P[0], P[1], tri2, label='Complete triangulation' )
plt.quiver( 
    P[ 0, FB[:,0] ], P[ 1, FB[:,0] ], 
    V[0], V[1],
    units='xy',
    label='Free boundaries' )

plt.title( r'Test of routine \texttt{Triangulation.\_FastChainLinkSort}' )
plt.axis( 'equal' )
plt.legend( loc='best' )
plt.grid( which='both' )
plt.show()

gc.collect()
