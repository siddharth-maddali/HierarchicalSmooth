/* 
 *
 * Base.h -- Contains basic function definitions 
 *
 */

#ifndef _HSMOOTH_BASE
#define _HSMOOTH_BASE

#include "igl/slice.h"

#include "Types.h"


namespace HSmoothBase{ 

/* ismember:
 * Mimics the basic functionality of Matlab's 'ismember' function, currently only for 
 * integer arrays with 3 columns because it is used on triangulations.
 */
	trimesh ismember( trimesh& Array1, std::vector<int>& Array2 );

/* getindex:
 * Returns a matindex object (defined in Types.h) of integers given an 
 * STL std::vector< int > object;
 */
	matindex getindex( std::vector< int >& );

/* getcomplement:
 * Given a matindex M and an integer N > max( M ), returns a matindex containing 
 * { integer i | i < N and i not in M }. Used to find indices of mobile nodes 
 * given the foxed ones and vice versa.
 */
	matindex getcomplement( matindex&, int );

/* matunion:
 * Returns the set union of the indexes in the two imput matindexes, 
 * sorted in ascending order.
 */
	matindex matunion( matindex&, matindex& );


/* merge:
 * Copies row data from source array into target array at the locations specified 
 * by the input matindex. NOTE: Source array should have same number of rows 
 * as elements in the matindex. Two versions are provided, for sparse and dense.
 */
	void merge( meshnode&, meshnode&, matindex& );
	void merge( SpMat&, SpMat&, matindex& );
}



#endif


