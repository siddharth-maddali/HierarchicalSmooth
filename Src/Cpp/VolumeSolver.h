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
#include "HierarchicalSmooth.h"

#include "igl/slice.h"	// for slicing operations on Eigen matrix types

namespace base 		= HSmoothBase;
namespace smooth	= HSmoothMain;
namespace tri		= HSmoothTri;

namespace VolumeSolver {

	class VolumeSolver {
	
		public:
		// constructor
		VolumeSolver( trimesh&, meshnode&, facelabel&, nodetype&, int=53 );
			// the last integer default is the number of bisections in each call
			// to the core smoothing routine. Obtained from a typical machine 
			// zero value of ~10^16. 
			// TODO: Generalize this to work for machine zero of the specific 
			// machine in use.

		// smoother
		meshnode HierarchicalSmooth( bool=false, std::string="Smooth.Default.log" );

		// writer
		meshnode GetSmoothed( void ) { return vsNodeSmooth; }

		private:
		// member objects; all these are instantiated in the constructor
		is_smoothed Status;
		trimesh vsMesh;
		meshnode vsNode, vsNodeSmooth;
		facelabel vsLabel;
		nodetype vsType;
		int MaxIterations;
		double fError, fErrorThreshold;
		std::ofstream fout;	// log file handle
		DictBase< std::vector< int > >::EdgeDict vsBoundaryDict;


		// member functions
		trimesh SliceMesh( std::vector< int >& );
		void MarkSectionAsComplete( matindex& );

		//scratch
		matindex one, three;

	};

}

#endif
