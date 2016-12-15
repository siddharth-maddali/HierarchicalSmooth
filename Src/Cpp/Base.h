/* 
 *
 * Base.h -- Contains basic function definitions 
 *
 */

#ifndef _HSMOOTH_BASE
#define _HSMOOTH_BASE

#include "Types.h"

namespace HSmoothBase{ 

/* ismember:
 * Mimics the basic functionality of Matlab's 'ismember' function, currently only for 
 * integer arrays with 3 columns because it is used on triangulations.
 */
	trimesh ismember( trimesh& Array1, std::vector<size_t>& Array2 );
	matindex getindex( std::vector< size_t >& );

}
#endif


