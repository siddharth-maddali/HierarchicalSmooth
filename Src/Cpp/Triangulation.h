/*
 * Triangulation.h -- contains a simple implementation of the 
 * 'triangulation' object from Matlab. Modeled from the Python 
 * prototype written by Siddharth Maddali. Customized for use 
 * in hierarchical smooth and doesn't have the full range of 
 * applicability as its Matlab counterpart. In particular, 
 * there is no functionality to computer mesh node-related 
 * quantities like local face and node normals. This will be 
 * added later as needed.
 */

#ifndef _HSMOOTH_TRI
#define _HSMOOTH_TRI

#include "Types.h"
#include "Base.h"


struct EdgeCount {
	EdgePair orig_pair;
	int ncount;
	EdgeCount( int x, int y ) {
		orig_pair = std::make_pair( x, y );
		ncount = 1;		// i.e. one edge already found at time of instantiation.
	}
};

namespace HSmoothTri {

	class Triangulation {
		public:
		Triangulation( trimesh& );			// not taking points for now; this will come later.

		trimesh connectivityList( void );
		EdgeList allEdges( void );
		std::tuple< EdgeList, EdgeList > freeBoundary( void );		// in proper winding order!
		std::tuple< SpMat, matindex > GraphLaplacian( void );

		private:
		// member objects
		trimesh Mesh, nSubTri;				// the Delaunay triangulation from which everything is derived
		EdgeList edge_list, free_boundary, free_boundary_segments;
		std::vector< int > nUnique;
		DictBase< EdgeCount >::EdgeDict MyDict;
		std::vector< double > fDiagCount;

		// member functions
		std::tuple< EdgeList, EdgeList > GetEdges( trimesh& );
		EdgeList FastChainLinkSort( EdgeList& );
		void differentiateFaces( void );

	};
}

#endif
