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

#include <iostream>
#include <tuple>
#include <unordered_map>
#include <boost/functional/hash.hpp>	// for std::hash( std::pair )

#include "Eigen/Eigen"
#include "Eigen/Sparse"

#include "Base.h"

typedef std::pair< size_t, size_t > EdgePair;
typedef std::vector< EdgePair > EdgeList;

/*
 * Since EdgePair objects are going to be searched for a lot in the 
 * hierarchical smooth library, the following definition is for a 
 * dictionary that maps EdgePair objects to objects of the user's 
 * choice. This object uses Boost's in-built hash function for 
 * std::pair objects. The target object type is specified through 
 * a template parameter T.
 */
template< typename T >
struct DictBase {
	typedef std::unordered_map< EdgePair, T, boost::hash< EdgePair > > EdgeDict;
};
/*
 * The dictionary initialization happens like this:
 *
 * DictBase< your-type >::EdgeDict my_dict;
 *
 */



typedef Eigen::SparseMatrix<double>	SpMat;
typedef Eigen::Triplet<double>		T;

struct EdgeCount {
	EdgePair orig_pair;
	int ncount;
	EdgeCount( size_t x, size_t y ) {
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
		EdgeList freeBoundary( void );		// in proper winding order!
		std::tuple< EdgeList, EdgeList > differentiateFaces( void );

		private:
		// member objects
		trimesh Mesh, nSubTri;				// the Delaunay triangulation from which everything is derived
		EdgeList edge_list, free_boundary;
		std::vector< size_t > nUnique;
		DictBase< EdgeCount >::EdgeDict MyDict;
		std::vector< double > fDiagCount;

		// member functions
		std::tuple< EdgeList, EdgeList > GetEdges( trimesh& );
		EdgeList FastChainLinkSort( EdgeList& );
		std::tuple< SpMat, std::vector< size_t > > GraphLaplacian( void );

	};
}

#endif
