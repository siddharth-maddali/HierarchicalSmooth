/*
 *
 * HierarchicalSmooth.h -- Contains main and auxiliary routine prototypes 
 * for smoothing according to the hierarchical filter method.
 *
 */

#ifndef _HSMOOTH_HSMOOTH
#define _HSMOOTH_HSMOOTH

#include <cmath>

#include "Types.h"
#include "Base.h"

namespace HSmoothMain{ 

	SpMat Laplacian2D( int N, std::string type="serial" );	// the options are 'serial' and 'cyclic'.
	std::tuple< SpMat, std::vector< int> > GraphLaplacian( trimesh& tri );	// multiple returns

	meshnode Smooth( meshnode&, std::string="serial", double=0.001, int=53 );
	meshnode Smooth( meshnode&, matindex&, SpMat&, double=0.001, int=53 );

	std::tuple< SpMat, SpMat > GetDirichletBVP( SpMat&, SpMat&, matindex&, matindex& );
	std::tuple< SpMat, SpMat > AnalyzeLaplacian( SpMat& );

	double GetObjFn( Smoother&, double, SpMat&, SpMat&, SpMat&, SpMat&, matindex&, SpMat&, SpMat&, SpMat&, SpMat& );

}

#endif



