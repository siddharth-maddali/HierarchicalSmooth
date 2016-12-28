/*
 * VolumcSolver.cpp:
 * Defines classes and routines declared in VolumeSolver.h
 */

#include "VolumeSolver.h"


//=======================================================================================

VolumeSolver::VolumeSolver::VolumeSolver( 
	trimesh& VolumeMesh, meshnode& SurfaceNodes, 
	facelabel& FLabels, nodetype& NodeType, 
	int nIterations ) {

	// loading primary data into solver
	vsMesh = VolumeMesh;
	vsNode = SurfaceNodes;
	vsLabel = FLabels;
	vsType = NodeType;
	MaxIterations = nIterations;

	Status = is_smoothed( vsType.size() );
	for( int i = 0; i < vsType.size(); i++ )
		Status( i ) = ( vsType(i) % 4 == 0 );	// smoothed is quad jn

	std::vector< int > vtemp{ 0, 1, 2 };
	std::vector< int > vtemp2{ 0 };

	one = base::getindex( vtemp2 );
	three = base::getindex( vtemp );

	vsNodeSmooth = meshnode::Zero( 3, vsNode.cols() );

	// Filling in boundary dictionary
	for( int i = 0; i <  vsLabel.rows(); i++ ) {
		EdgePair this_pair = std::make_pair(  
			std::min( vsLabel( i, 0 ), vsLabel( i, 1 ) ), 
			std::max( vsLabel( i, 0 ), vsLabel( i, 1 ) )
		);
		DictBase< std::vector< int > >::EdgeDict::iterator got = vsBoundaryDict.find( this_pair );
		if( got == vsBoundaryDict.end() ) {		// new boundary, new dictionary entry
			std::vector< int > v;
			v.push_back( i );
			vsBoundaryDict.insert( { this_pair, v } );
		}
		else {									// this patch belongs to an already found boundary
			std::vector< int >& myref = got->second;
			myref.push_back( i );
		}
	}
}

//=======================================================================================

meshnode VolumeSolver::VolumeSolver::HierarchicalSmooth( bool logging, std::string logfile ) {
	fout.open( logfile.c_str() );
	std::ostream& outfile = ( logging ? fout : std::cout );

	for( 
		DictBase< std::vector< int > >::EdgeDict::iterator it = vsBoundaryDict.begin(); 
		it != vsBoundaryDict.end(); 
		++it 
	) {
		trimesh triSub = SliceMesh( it->second );
		tri::Triangulation T( triSub );
		
		std::tuple< SpMat, matindex > Topology = T.GraphLaplacian();
	 	SpMat GL = std::get<0>( Topology );
		matindex nUniq = std::get<1>( Topology );
		meshnode BoundaryNode;
		igl::slice( vsNode, three, nUniq, BoundaryNode );

		std::tuple< EdgeList, EdgeList > FreeBndData = T.freeBoundary();
		EdgeList FB = std::get<0>( FreeBndData );
		EdgeList fbsec = std::get<1>( FreeBndData );

		for( int i = 0; i < fbsec.size(); i++ ) {	// smooth each free boundary first
			int start, stop, count;
			start = std::get<0>( fbsec[i] );
			stop = std::get<1>( fbsec[i] );
			count = start;
			while( count <= stop && Status( nUniq( std::get<0>( FB[ count ] ) ) ) == false )
				count++;
			if( count > stop ) {	// no quad jns in this free boundary. smooth without constraints and get out.
				meshnode BoundaryNodeSmooth = smooth::Smooth( BoundaryNode, std::string( "cyclic" ) );
				for( int i = 0; i < nUniq.size(); i++ )
					vsNodeSmooth.col( nUniq( i ) ) << BoundaryNodeSmooth.col( i );
				MarkSectionAsComplete( nUniq );
			}
			else {					// triple line sections found; smooth separately.
				std::vector< int > vtemp;
				vtemp.push_back( count );
				int thissize = 1 + ( stop - start );
				for( int j = count+1; j < count + thissize; j++ ) {
					int effective_j = j % thissize;
					vtemp.push_back( effective_j );
					if( vsType( nUniq( std::get<0>( FB[ effective_j ] ) ) ) % 4 == 0 ) {	// reached terminal quad point
						matindex thisTripleLineIndex = base::getindex( vtemp );
						
						matindex temp1;
						is_smoothed temp2;
						igl::slice( nUniq, thisTripleLineIndex, one, temp1 );
						igl::slice( Status, temp1, one, temp2 );

						if( !temp2.all() ) {
							meshnode thisTripleLine, thisTripleLineSmoothed; 
							igl::slice( BoundaryNode, three, thisTripleLineIndex, thisTripleLine );
							thisTripleLineSmoothed = smooth::Smooth( thisTripleLine );
							MarkSectionAsComplete( temp1 );
						}
						vtemp.clear();
						vtemp.push_back( effective_j );
					}
				}
			}
		}
	}

	outfile << "Done smoothing volume. " << '\n';
	fout.close();
	return vsNodeSmooth;
}

//=======================================================================================

trimesh VolumeSolver::VolumeSolver::SliceMesh( std::vector< int >& FromThesePatches ) {
	trimesh triSub;
	igl::slice( vsMesh, base::getindex( FromThesePatches ), three, triSub );
	return triSub;
}

//=======================================================================================

void VolumeSolver::VolumeSolver::MarkSectionAsComplete( matindex& idx ) {
	for( int i = 0; i < idx.size(); i++ )
		Status( idx( i ) ) = true;
	return;
}

//=======================================================================================















