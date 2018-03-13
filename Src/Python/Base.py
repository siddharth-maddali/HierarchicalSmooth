#   COpyright (c) 2016-2018, Siddharth Maddali 
#   All rights reserved. 
#   
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met: 
#   
#    * Redistributions of source code must retain the above copyright notice, 
#      this list of conditions and the following disclaimer. 
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in the 
#      documentation and/or other materials provided with the distribution. 
#    * Neither the name of Carnegie Mellon University nor the names of its 
#      contributors may be used to endorse or promote products derived from 
#      this software without specific prior written permission. 
#   
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
#   POSSIBILITY OF SUCH DAMAGE. 
#   
import numpy as np
import sys
from scipy.sparse import csc_matrix

# intermediate definitions

def __ismember_rows( Array1, Array2 ):
    l1 = [ list( i ) for i in Array1 ]
    l2 = [ list( i ) for i in Array2 ]
    out1 = [ i in l2 for i in l1 ]
    xloc = list( np.where( out1 )[0] )
    out2 = [ list( np.where( np.array(l2)==l1[i] )[0] )[0] for i in xloc ]
    return out1, out2

def __ismember_list( Array1, Array2 ):
    temp1 = Array1.ravel().reshape( -1, 1 )
    temp2 = Array2.ravel().reshape( -1, 1 )
    sol, idx = __ismember_rows( temp1, temp2 )
    sol = np.array( sol ).reshape( -1, Array1.shape[1] )
    return sol, idx

"""
    ISMEMBER -- mimics the functionality of the ismember function 
    in Matlab, although in a limited manner. Only optional kwarg 
    (for now) is 'rows'.
"""
def ismember( Array1, Array2, comparison_type='list' ):
    if comparison_type=='list': 
        return __ismember_list( Array1, Array2 )
    
    elif comparison_type=='rows':
        return __ismember_rows( Array1, Array2 )
    
    else:
        sys.stderr.write( "'ismember' error: invalid comparison type.\n" );
        return [], []

