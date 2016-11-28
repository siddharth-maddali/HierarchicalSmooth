# A set of private functions not meant to be seen outside 
# module HierarchicalSmooth, containing functions for use 
# inside HierarchicalSmooth only. For better readability.

from scipy.sparse.linalg import spsolve
import copy


def _GetObjFn( fMyEps, fEye, LTL, yIn, nMobile, LK, D, AyIn ):

    yOut = spsolve( 
        ( 1. - fMyEps )*fEye + fMyEps*LTL, 
        ( 1. - fMyEps )*yIn[ nMobile, : ] - fMyEps*LK
    )
    yTemp = copy.deepcopy( yIn )
    yTemp[ nMobile, : ] = yOut
    fObj = D*yTemp + AyIn
    return ( fObj.T *fObj ).diagonal().sum(), yTemp
