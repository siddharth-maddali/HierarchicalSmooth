import numpy				as np
import HierarchicalSmooth	as hs

filePrefix = '/home/smaddali/MatlabScripts/HierarchicalSmooth/examples/ex2'

print 'Loading data...'
P		= np.loadtxt( filePrefix + '/SharedVertexList.txt',	dtype=float	).T
tri		= np.loadtxt( filePrefix + '/SharedTriList.txt', 	dtype=int	)
nFaces	= np.loadtxt( filePrefix + '/FaceLabels.txt', 		dtype=int	)
nType	= np.loadtxt( filePrefix + '/NodeType.txt', 		dtype=int	)

print 'Commencing smooth...'
PS, bPS = hs.HierarchicalSmooth( 
	xPoints=P, tri=tri, 
	nFaceLabels=nFaces, 
	nNodeType=nType
	)

