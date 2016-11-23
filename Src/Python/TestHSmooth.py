import numpy as np
import Triangulation as tr
import HierarchicalSmooth as hs
import Base as base

from scipy.sparse import csc_matrix

P = csc_matrix( np.loadtxt( '../../examples/ex0/SharedVertexList.txt' ).T )
tri = np.loadtxt( '../../examples/ex0/SharedTriList.txt', dtype=int )
nFaceLabels = np.loadtxt( '../../examples/ex0/FaceLabels.txt', dtype=int )
nType = np.loadtxt( '../../examples/ex0/NodeType.txt', dtype=int )
nUniqFaces = np.vstack( { tuple( row ) for row in nFaceLabels} )

print 'Number of grain boundaries = %d' % len( nUniqFaces )

nGB = 5

triGB = tri[ np.where( base.ismember( nFaceLabels, nUniqFaces[nGB].reshape( 1, -1 ), 'rows' )[0] )[0], : ]
pointGB = np.unique( triGB )
triGB = np.array( base.ismember( triGB, pointGB )[1] ).reshape( -1, 3 )
xGB = P[ :, pointGB ]
typeGB = nType[ pointGB ]

FB, FBsec = hs.DifferentiateFaces( tr.Triangulation( triGB, xGB ) )

#print FB

xGBS = hs.HierarchicalSmooth( xGB, triGB, nUniqFaces[ nGB ].reshape( 1, -1 ).repeat( triGB.shape[0] ) )

