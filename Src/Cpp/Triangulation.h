/*
 * Triangulation.h -- contains a simple implementation of the 
 * 'triangulation' object from Matlab. Modeled from the Python 
 * prototype written by Siddharth Maddali. Customized for use 
 * in hierarchical smooth and doesn't have the full range of 
 * applicability as its Matlab counterpart.
 *
 */

#ifndef _HSMOOTH_TRI
#define _HSMOOTH_TRI

#include "Base.h"
#include "Eigen/Eigen"

namespace HSmoothTri {

	typedef Eigen::Array< size_t, Eigen::Dynamic, 2 > edgelist;

	class Triangulation {
		public:
		Triangulation( trimesh& inTri, Eigen::MatrixXd xIn );
		~Triangulation();
		trimesh connectivityList( void );
		edgelist allEdges( void );
		edgelist freeBoundary( void );		// in proper winding order!
		edgelist differentiateFaces( void );

		private:
		trimesh Mesh;		// the Delaunay triangulation
		Eigen::MatrixXd P;	// the mesh nodes
		edgelist edgeList, freeBoundary;

	};
}

#endif
