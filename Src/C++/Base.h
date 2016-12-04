/* 
 * Base.h -- Contains basic function definitions 
 */

#ifndef _HSMOOTH_BASE
#define _HSMOOTH_BASE

#include <iostream>

#include "Eigen/Eigen"

/*  -- output type for the ismember function */
typedef std::tuple< Eigen::Array<bool,Dynamic,2> Array1, std::vector<unsigned> > baseOut;

namespace HSmooth_base{ 

	baseOut ismsmber( 

}



#endif


