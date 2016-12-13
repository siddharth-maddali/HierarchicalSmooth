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

namespace VolumeSolver {

	class VolumeSolver {
		public:
		VolumeSolver( 
			trimesh& VolumeMesh, meshnode& SurfaceNodes, 
			facelabel& FLabels, nodetype& NodeType 
		);
		meshnode HierarchicalSmooth( 
			bool logging=false, std::string logfile="Smooth.Default.log"
		);

		private:
		// member objects; all these are instantiated in the constructor
		is_smoothed Status;
		trimesh vsMesh;
		meshnode vsNode;
		facelabel vsLabel;
		nodetype vsType;
		int MaxIterations;
		std::unordered_map< size_t, std::vector< size_t > > vsBoundaryDict;

		// member functions
		std::tuple< trimesh, meshnode, nodetype	> BuildBoundary( std::vector< size_t >& FromThesePatches );
		bool SmoothBoundary( std::tuple< trimesh, meshnode, nodetype > );
		bool Smooth2D( 

	};

}

#endif
