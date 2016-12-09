/*
 *
 * Base.cpp -- implementation of routines in Base.h
 *
 */

#include "Base.h"

// size_t is the same as unsigned long

//============================================================================================

trimesh HSmoothBase::ismember( trimesh& Array1, std::vector<size_t>& Array2 ) {
	
	std::unordered_map< size_t, size_t > MyDict; // dictionary lookup for faster access
	for( size_t i = 0; i < Array2.size(); i++ ) 
		MyDict.insert( { Array2[i], i } );
	trimesh NewTri = trimesh::Zero( Array1.rows(), Array1.cols() );
	// running through Array1 in column-major order, Eigen's default
	for( size_t col = 0; col < Array1.cols(); col++ ) {
		for( size_t row = 0; row < Array1.rows(); row++ ) {
			std::unordered_map<size_t,size_t>::const_iterator got = MyDict.find( Array1( row, col ) );
			NewTri( row, col ) = got->second;
		}
	}
	return NewTri;
}

//============================================================================================
