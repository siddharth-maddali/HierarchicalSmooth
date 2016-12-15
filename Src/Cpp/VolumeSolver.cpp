/*
 * VolumcSolver.cpp:
 * Defines classes and routines declared in VolumeSolver.h
 */



//=======================================================================================

VolumeSolver::VolumeSolver::VolumeSolver( 
	trimesh& VolumeMesh, meshnode& SurfaceNodes, 
	facelabel& FLabels, nodetype& NodeType, 
	size_t nIterations ) {

	// loading primary data into solver
	vsMesh = VolumeMesh;
	vsNode = SurfaceNodes;
	vsLabel = FLabels;
	vsType = NodeType;
	MaxIterations = nIterations;

	vsNodeSmooth = meshnode( vsNode.cols() );

	// Filling in boundary dictionary
	for( size_t i = 0; i <  vsLabel.rows(); i++ ) {
		EdgePair this_pair = std::make_pair(  
			std::min( vsLabel( i, 0 ), vsLabel( i, 1 ) ), 
			std::max( vsLabel( i, 0 ), vsLabel( i, 1 ) )
		);
		DictBase< std::vector< size_t > >::EdgeDict::iterator got = vsBoundaryDict.find( this_pair );
		if( got == vsBoundaryDict.end() ) {		// new boundary, new dictionary entry
			std::vector< size_t > v;
			v.push_back( i );
			vsBoundaryDict.insert( { this_pair, v } );
		}
		else {									// this patch belongs to an already found boundary
			std::vector< size_t >& myref = got->second;
			myref.push_back( i );
		}
	}
}

//=======================================================================================

meshnode VolumeSolver::VolumeSolver::HierarchicalSmooth( bool logging, std::string logfile ) {
	fout.open( logfile.c_str(), std::ios::out );
	std::ofstream& outfile = ( logging ? fout : std::cout );

	for( 
		DictBase< std::vector< size_t > >::EdgeDict::iterator it = vsBoundaryDict.begin(); 
		it != vsBoundaryDict.end(); 
		++it 
	) {
		trimesh triSub = SliceMesh( it->second );
		HSmoothTri::Triangulation T( triSub );
		
		std::tuple< SpMat, matindex > Topology = T.GraphLaplacian();
	 	SpMat GL = std::get<0>( Topology );
		matindex nUniq = std::get<1>( Topology );
		
		std::tuple< EdgeList, EdgeList > FreeBndData = T.freeBoundary();
		EdgeList FB = std::get<0>( FreeBndData );
		EdgeList fbsec = std::get<1>( FreeBndData );

		
		
	}

	outfile << "Done smoothing volume" << '\n';
	outfile.close();		// what happens when this is std::cout?
	return vsNodeSmooth;
}

//=======================================================================================

trimesh VolumeSolver::VolumeSolver::SliceMesh( std::vector< size_t >& FromThesePatches ) {
	trimesh triSub;
	igl::slice( 
		vsMesh, 
		HSmoothBase::getindex( FromThesePatches ), 
		HSmoothBase::getindex( std::vector< size_t >{ 0, 1, 2 } ),
		triSub 
	);
	return triSub;
}

//=======================================================================================

















