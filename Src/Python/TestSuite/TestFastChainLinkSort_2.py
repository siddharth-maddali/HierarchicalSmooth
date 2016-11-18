import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rc
rc( 'text', usetex=True )

from scipy.spatial import Delaunay
import gc

import Triangulation as tr

#nPoints = 1000
nRemovable = 1000
fLeft = -1.
fRight = 1.
fPts = 60
fNoise = 0.25

mx, my = np.meshgrid( 
        np.linspace( fLeft, fRight, fPts ), 
        np.linspace( fLeft, fRight, fPts )
        )
P= np.concatenate( 
        ( mx.reshape( 1, -1 ), my.reshape( 1, -1 ) ), 
        axis=0 )
P = P + ( fNoise * ( fRight-fLeft )/ fPts ) * np.random.rand( P.shape[0], P.shape[1] )

#P = np.random.rand( 2, nPoints )
tri = Delaunay( P.T ).simplices
nRemovedPoints =  np.random.permutation( P.shape[1]  )[ :nRemovable ]
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
        scale=1, units='xy', label='Free boundaries' )

plt.title( r'Test of routine \texttt{Triangulation.\_FastChainLinkSort}' )
plt.axis( 'equal' )
plt.axis( 'tight' )
plt.legend( loc='best' )
plt.grid( which='both' )
plt.show()

gc.collect()
