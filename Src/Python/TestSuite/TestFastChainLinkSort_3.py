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
