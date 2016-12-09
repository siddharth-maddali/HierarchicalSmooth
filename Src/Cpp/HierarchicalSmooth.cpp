/*
 *
 * HierarchicalSmooth.cpp -- implementation of the routines declared in HierarchicalSmooth.h
 *
 */

#include "HierarchicalSmooth.h"


//============================================================================================

SpMat HSmoothMain::Laplacian2D( size_t N, std::string type ) {

	std::vector< T > tripletList;
	tripletList.reserve( 3*N ); // approx. number of nonzero elements
	for( size_t i = 0; i < N; i++ ) {
		tripletList.push_back( T( i, i, -1.0 ) );
		if( i != N-1 )
			tripletList.push_back( T( i, i+1, 1.0 ) );
	}
	SpMat temp( N, N );
	temp.setFromTriplets( tripletList.begin(), tripletList.end() );
	SpMat L = SpMat( temp.transpose() ) * temp;
	if( type=="serial" ){ 
		L.coeffRef( N-1, N-1 ) = 1.0;
	}
	else if( type=="cyclic" ) { 
		L.coeffRef( 0, 0 ) = 2.0;
		L.coeffRef( 0, N-1 ) = L.coeffRef( N-1, 0 ) = -1.0;
	}
	else
		std::cerr << "HSmoothMain::Laplacian2D: Unrecognized type. " << std::endl;

	return L;
}

//============================================================================================

SpMat HSmoothMain::GraphLaplacian( trimesh& tri ) {
	vector< size_t > nUnique;
	for( size_t i = 0; i < tri.rows(); i++ ) {
		for( size_t j = 0; j < tri.cols(); j++ ) {
			nUnique.push_back( tri( i, j );
		}
	}
	std::sort( nUnique.begin(), nUnique.end() );
	nUnique.erase( std::unique( nUnique.begin(), nUnique.end() ), nUnique.end() );

	trimesh nSubTri = HSmoothBase::ismember( tri, nUnique );

	return L;
}
