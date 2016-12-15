/*
 * VolumeSolver.h -- contains the definition of the object that takes the 
 * surface mesh data of the entire volume and returns an array containing 
 * hierarchical-smoothed mesh nodes. This object does all the necessary 
 * bookkeeping with node types, connectivity and smoothed status.
 */

#ifndef _HSMOOTH_VOLSOLVER
#define _HSMOOTH_VOLSOLVER

#include <iostream>
#include <fstream>

#include "Eigen/Eigen"

#include "Types.h"
#include "Base.h"
#include "Triangulation.h"

#include "igl/slice.h"	// for slicing operations on Eigen matrix types

namespace VolumeSolver {

	class VolumeSolver {
	
		public:
		// constructor
		VolumeSolver( trimesh&, meshnode&,facelabel&, nodetype&, size_t=53 );
			// the last integer default is the number of bisections in each call
			// to the core smoothing routine. Obtained from a typical machine 
			// zero value of ~10^16.

		// smoother
		bool HierarchicalSmooth( 
			bool=false, std::string="Smooth.Default.log"
		);

		// writer
		meshnode GetSmoothed( void ) { return vsNodeSmooth };

		private:
		// member objects; all these are instantiated in the constructor
		is_smoothed Status;
		trimesh vsMesh;
		meshnode vsNode, vsNodeSmooth;
		facelabel vsLabel;
		nodetype vsType;
		int MaxIterations;
		std::fstream fout;	// log file handle
		Dictbase< std::vector< size_t > >::EdgeDict vsBoundaryDict;

		// member functions
		trimesh SliceMesh( std::vector< size_t >& );

	};

}

#endif
