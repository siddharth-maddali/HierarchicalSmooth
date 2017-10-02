// Most preprocessor directives stolen from code on Shawn Lankton's website:
//
// http://www.shawnlankton.com/2008/03/getting-started-with-mex-a-short-tutorial/
//
// ...Thanks, Shawn Lankton.


//	#include <matrix.h>		// uncomment this file for matlab, leave commented for octave.
	#include <mex.h>   

	#include <iostream>
	
	#include "VolumeSolver.h"
	
	
	/* Definitions to keep compatibility with earlier versions of ML */
	#ifndef MWSIZE_MAX
	typedef int mwSize;
	typedef int mwIndex;
	typedef int mwSignedIndex;
		#if (defined(_LP64) || defined(_WIN64)) && !defined(MX_COMPAT_32)
		/* Currently 2^48 based on hardware limitations */
			# define MWSIZE_MAX    281474976710655UL
			# define MWINDEX_MAX   281474976710655UL
			# define MWSINDEX_MAX  281474976710655L
			# define MWSINDEX_MIN -281474976710655L
		#else
			# define MWSIZE_MAX    2147483647UL
			# define MWINDEX_MAX   2147483647UL
			# define MWSINDEX_MAX  2147483647L
			# define MWSINDEX_MIN -2147483647L
		#endif
		#define MWSIZE_MIN    0UL
		#define MWINDEX_MIN   0UL
	#endif

	void mexFunction( int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[] ) {

	/* 	Setting up wrapper variables: START */

		// declare variables
		const mwSize *dims_VolumeMesh, *dims_SurfaceNodes, *dims_FLabels, *dims_NodeType;
		double *VolumeMesh, *SurfaceNodes, *FLabels, *NodeType, *SmoothNodes;
		int	VolumeMesh_dimx, VolumeMesh_dimy, 
			SurfaceNodes_dimx, SurfaceNodes_dimy, 
			FLabels_dimx, FLabels_dimy, 
			NodeType_dimx, NodeType_dimy;
	
		// figure out dimensions
		dims_VolumeMesh = mxGetDimensions( prhs[0] );
		VolumeMesh_dimx = ( int )dims_VolumeMesh[0]; VolumeMesh_dimy = ( int )dims_VolumeMesh[1];

		dims_SurfaceNodes = mxGetDimensions( prhs[1] );
		SurfaceNodes_dimx = ( int )dims_SurfaceNodes[0]; SurfaceNodes_dimy = ( int )dims_SurfaceNodes[1];

		dims_FLabels = mxGetDimensions( prhs[2] );
		FLabels_dimx = ( int )dims_FLabels[0]; FLabels_dimy = ( int )dims_FLabels[1];

		dims_NodeType = mxGetDimensions( prhs[3] );
		NodeType_dimx = ( int )dims_NodeType[0]; NodeType_dimy = ( int )dims_NodeType[1];


		// associate outputs
		plhs[0] = mxCreateDoubleMatrix( SurfaceNodes_dimx, SurfaceNodes_dimy, mxREAL );
			// i.e. output array same size as input array.

		// associate pointers
		VolumeMesh		= mxGetPr( prhs[0] );
		SurfaceNodes	= mxGetPr( prhs[1] );
		FLabels			= mxGetPr( prhs[2] );
		NodeType		= mxGetPr( prhs[3] );

		SmoothNodes 	= mxGetPr( plhs[0] );

	/* Setting up wrapper variables: END */		
			


	/* C++ operations take place here. */
		trimesh tri; 
		meshnode P;
		facelabel FL; 
		nodetype NT;

		tri	= -1 + Eigen::Map< Eigen::MatrixXd >  ( VolumeMesh, VolumeMesh_dimx, VolumeMesh_dimy ).cast<int>().array();
		P	= Eigen::Map< meshnode > ( SurfaceNodes, SurfaceNodes_dimx, SurfaceNodes_dimy );
		FL	= Eigen::Map< Eigen::MatrixXd >( FLabels, FLabels_dimx, FLabels_dimy ).cast<int>().array();
		NT	= Eigen::Map< Eigen::MatrixXd > ( NodeType, NodeType_dimx, NodeType_dimy ).cast<int>().array();

		VolumeSolver::VolumeSolver V( tri, P, FL, NT );
		V.HierarchicalSmooth();
		meshnode PSmooth = V.GetSmoothed();
	
	/* Map back to Matlab/Octave variables. */
		Eigen::Map< meshnode >( SmoothNodes, SurfaceNodes_dimx, SurfaceNodes_dimy ) = PSmooth;
	
	/* Done. Get out. */
		return;
	}
