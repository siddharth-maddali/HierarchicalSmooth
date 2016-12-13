/*
 *
 * HierarchicalSmooth.h -- Contains main and auxiliary routine prototypes 
 * for smoothing according to the hierarchical filter method.
 *
 */

#ifndef _HSMOOTH_HSMOOTH
#define _HSMOOTH_HSMOOTH

#include "Types.h"
#include "Base.h"

namespace HSmoothMain{ 

	SpMat Laplacian2D( size_t N, std::string type="serial" );	// the options are 'serial' and 'cyclic'.
	std::tuple< SpMat, std::vector< size_t> > GraphLaplacian( trimesh& tri );	// multiple returns

}

#endif



