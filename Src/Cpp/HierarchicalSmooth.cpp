/*
 *
 * HierarchicalSmooth.cpp -- implementation of the routines declared in HierarchicalSmooth.h
 *
 */

#include "Base.h"
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

	L.makeCompressed();
	return L;
}

//============================================================================================

SpMat HSmoothMain::GraphLaplacian( trimesh& tri ) { 

	std::vector< size_t > nUnique;
	for( size_t i = 0; i < tri.rows(); i++ ) 
		for( size_t j = 0; j < tri.cols(); j++ ) 
			nUnique.push_back( tri( i, j ) );
	std::sort( nUnique.begin(), nUnique.end() );
	nUnique.erase( std::unique( nUnique.begin(), nUnique.end() ), nUnique.end() );
	size_t MaxIdx = 1 + nUnique.back();

	std::vector< T > tripletList;
	tripletList.reserve( nUnique.size() + tri.rows()*tri.cols()*2 );

	std::vector< double > fDiagCount( nUnique.size(), 0.0 );

	trimesh nSubTri = HSmoothBase::ismember( tri, nUnique );

	std::unordered_map< size_t, size_t > MyDict;
	for( size_t i = 0; i < nSubTri.rows(); i++ ) {
		for( size_t j = 0; j < 3; j++ ) {
			size_t l = ( j + 3 ) % 3;
			size_t m = ( j + 4 ) % 3;
			size_t this_row = nSubTri(i,l); 
			size_t this_col = nSubTri(i,m);
			size_t this_hash = std::min(this_row,this_col) + MaxIdx * std::max(this_row,this_col); 
			std::unordered_map< size_t, size_t  >::const_iterator got = MyDict.find( this_hash );
			if( got == MyDict.end() ) {				// not found yet...
				MyDict.insert( { this_hash, i } );	// i.e. the edge, and the triangle it belongs to.
				tripletList.push_back( T( this_row, this_col, -1.0 ) );
				tripletList.push_back( T( this_col, this_row, -1.0 ) );
				fDiagCount[ this_row ] += 1.0;
				fDiagCount[ this_col ] += 1.0;
			}

		}
	}

	for( size_t i = 0; i < fDiagCount.size(); i++ )
		tripletList.push_back( T( i, i, fDiagCount[i] ) );

	SpMat MLap( nUnique.size(), nUnique.size() );
	MLap.setFromTriplets( tripletList.begin(), tripletList.end() );
	MLap.makeCompressed();
	return MLap;
}

//============================================================================================
