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

#include "Eigen/Eigen"
#include "Eigen/Sparse"

#include "Base.h"

typedef Eigen::SparseMatrix<double> SpMat;
typedef Eigen::Triplet<double>	T;

namespace HSmoothMain{ 

	SpMat Laplacian2D( size_t N, std::string type="serial" );	// the options are 'serial' and 'cyclic'.
	SpMat GraphLaplacian( trimesh& tri );

}




#endif



