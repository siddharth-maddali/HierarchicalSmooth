/* Triangulation.cpp -- implementation of routines declared in Triangulation.h */

#include "Triangulation.h"

//===================================================================================

HSmoothTri::Triangulation::Triangulation( trimesh& inTri ) {

	Mesh = inTri;
	std::tuple< EdgeList, EdgeList > GetAllEdges = GetEdges( Mesh );
	edge_list = std::get<0>( GetAllEdges );
	free_boundary = std::get<1>( GetAllEdges );
	differentiateFaces();

}

//===================================================================================

trimesh HSmoothTri::Triangulation::connectivityList( void ) {
	return Mesh;
}

//===================================================================================

EdgeList HSmoothTri::Triangulation::allEdges( void ) {
	return edge_list;
} 

//===================================================================================

std::tuple< EdgeList, EdgeList > HSmoothTri::Triangulation::freeBoundary( void ) {
	return std::make_tuple( free_boundary, free_boundary_segments );
}

//===================================================================================
void HSmoothTri::Triangulation::differentiateFaces( void ) {
	size_t start = std::get<0>( free_boundary[0] );
	std::vector< size_t > thissec{ 0 };
	size_t n = 1;
	while( n < free_boundary.size() ) {
		if( std::get<1>( free_boundary[n] ) == start ) {
			thissec.push_back( n );
			free_boundary_segments.push_back( std::make_pair( thissec[0], thissec[1] ) );
			thissec.clear();
		}
		else if( thissec.size() == 0 ) { 
			start = std::get<0>( free_boundary[n] );
			thissec.push_back( n );
		}
		n++;
	}
	return;
}

//===================================================================================

/*
 * NOTE: 
 * The GetEdges method defined here contains code that is extraneous to its 
 * primary function, in order to lay the groundwork for a much faster method 
 * that computes the graph Laplacian, than the standalone function defined in 
 * HierarchicalSmooth.cpp. This method, internal to the Triangulation object 
 * is implemented in the hierarchical smooth algorithm while the standalone 
 * is provided for choice.
 */

std::tuple< EdgeList, EdgeList > HSmoothTri::Triangulation::GetEdges( trimesh& inTri ) {

	for( size_t i = 0; i < inTri.rows(); i++ ) 
		for( size_t j = 0; j < inTri.cols(); j++ ) 
		nUnique.push_back( inTri( i, j ) );
	std::sort( nUnique.begin(), nUnique.end() );
	nUnique.erase( std::unique( nUnique.begin(), nUnique.end() ), nUnique.end() );

	fDiagCount = std::vector< double >( nUnique.size(), 0.0 );
	nSubTri = HSmoothBase::ismember( inTri, nUnique );

	for( size_t i = 0; i < nSubTri.rows(); i++ )  {
		for( size_t j = 0; j < 3; j++ ) {
			size_t l = ( j+3 ) % 3;
			size_t m = ( j+4 ) % 3;
			size_t this_row = nSubTri( i, l );
			size_t this_col = nSubTri( i, m );
			EdgePair EP = std::make_pair( std::min( this_row, this_col ), std::max( this_row, this_col ) );
			DictBase< EdgeCount >::EdgeDict::iterator got = MyDict.find( EP );
			if( got == MyDict.end() ) {	// not found yet; this is a new edge.
				EdgeCount EC( nUnique[ this_row ], nUnique[ this_col ] );
				MyDict.insert( { EP, EC } );
				fDiagCount[ this_row ] += 1.0;
				fDiagCount[ this_col ] += 1.0;

			}
			else { 						// this is definitely an interior edge.
				EdgeCount& ec = got->second;
				(ec.ncount)++;
			}
		}
	}

	for( DictBase< EdgeCount >::EdgeDict::iterator it = MyDict.begin(); it != MyDict.end(); ++it ) {
		edge_list.push_back( ( it->second ).orig_pair );
		if( ( it->second ).ncount == 1 )
			free_boundary.push_back( ( it->second ).orig_pair );
	}
	return std::make_tuple( edge_list, FastChainLinkSort( free_boundary ) );
}

//===================================================================================

EdgeList HSmoothTri::Triangulation::FastChainLinkSort( EdgeList& inList ) {
	std::unordered_map< size_t, std::vector< size_t > > WindingDict;
	for( size_t i = 0; i < inList.size(); i++ ) {
		size_t ltemp = std::get<0>( inList[i] );
		size_t rtemp = std::get<1>( inList[i] );
		std::unordered_map< size_t, std::vector< size_t > >::iterator got = WindingDict.find( ltemp );
		if( got == WindingDict.end() ) {
			std::vector< size_t > v{ rtemp };	// yet another way to initialize a vector!
			WindingDict.insert( { ltemp, v } );
		}
		else {
			std::vector< size_t >& vtemp = got->second;
			vtemp.push_back( rtemp );
		}
	}
	EdgeList outList;
	std::unordered_map< size_t, std::vector< size_t > >::iterator it = WindingDict.begin();
	while( WindingDict.size() > 0 ) {			// decimate the dictionary as chain-linked list is generated.
		size_t next = ( it->second ).back();	// pop backwards; as good a way to fill as any!
		EdgePair ptemp = std::make_pair( it->first, next );
		outList.push_back( ptemp );
		( it->second ).pop_back();
		if( ( it->second ).size() == 0 ) WindingDict.erase( it );
		it = WindingDict.find( next );
		if( it == WindingDict.end() ) it = WindingDict.begin();
	}
	return outList;
}

//===================================================================================
