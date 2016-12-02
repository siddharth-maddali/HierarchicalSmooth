# A set of private functions not meant to be seen outside 
# module HierarchicalSmooth, containing functions for use 
# inside HierarchicalSmooth only. For better readability.

from scipy.sparse.linalg import spsolve
import copy

def _GetObjFn( fMyEps, fEye, LTL, yIn, nMobile, LK, D, AyIn ):
	yTemp = copy.deepcopy( yIn )
	try:
		yOut = spsolve(	( 1. - fMyEps )*fEye + fMyEps*LTL, ( 1. - fMyEps )*yIn[ nMobile, : ] - fMyEps*LK )
	except RuntimeError:
		return 0.0, yTemp	
	yTemp[ nMobile, : ] = yOut
	fObj = D*yTemp + AyIn
	return ( fObj.T *fObj ).diagonal().sum(), yTemp
