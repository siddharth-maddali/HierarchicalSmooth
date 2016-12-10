/*
 *
 * HierarchicalSmooth.h -- Contains main and auxiliary routine prototypes 
 * for smoothing according to the hierarchical filter method.
 *
 */

#ifndef _HSMOOTH_HSMOOTH
#define _HSMOOTH_HSMOOTH

#include <iostream>
#include <vector>
#include <unordered_map>

#include <boost/functional/hash.hpp>	// for hash( std::pair )

#include "Eigen/Eigen"
#include "Eigen/Sparse"

#include "Base.h"

typedef Eigen::SparseMatrix<double>	SpMat;
typedef Eigen::Triplet<double>		T;
typedef std::pair< size_t, size_t >	EdgePair;

//typedef template< typename T > std::unordered_map< EdgePair, T, boost::hash< EdgePair > > EdgeDict;
	/* 
	 * The above line will not work because 
	 * templated typedefs are not legal in C++. 
	 * Instead, do the following...
	 */
template< typename T >
struct DictBase {
	typedef std::unordered_map< EdgePair, T, boost::hash< EdgePair > > EdgeDict;
};
	/*
	 * ...and then do this:
	 *
	 * DictBase< your-type >::EdgeDict my_dict;
	 *
	 * ...to declare an unordered map from a 
	 * pair of integers to objects of type 'your-type'.
	 */

namespace HSmoothMain{ 

	SpMat Laplacian2D( size_t N, std::string type="serial" );	// the options are 'serial' and 'cyclic'.
	SpMat GraphLaplacian( trimesh& tri );

}




#endif



