%   Copyright (c) 2016, Siddharth Maddali 
%   All rights reserved. 
%   
%   Redistribution and use in source and binary forms, with or without 
%   modification, are permitted provided that the following conditions are met: 
%   
%    * Redistributions of source code must retain the above copyright notice, 
%      this list of conditions and the following disclaimer. 
%    * Redistributions in binary form must reproduce the above copyright 
%      notice, this list of conditions and the following disclaimer in the 
%      documentation and/or other materials provided with the distribution. 
%    * Neither the name of Carnegie Mellon University nor the names of its 
%      contributors may be used to endorse or promote products derived from 
%      this software without specific prior written permission. 
%   
%   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
%   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
%   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
%   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
%   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
%   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
%   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
%   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
%   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
%   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
%   POSSIBILITY OF SUCH DAMAGE. 
%   
function [ FacesList, FBSections ] = DifferentiateFaces( TriangIn )

    triThis = TriangIn.ConnectivityList;
    FB = FastChainLinkSort( TriangIn.freeBoundary );
    nStart = 1;
    nStop = find( FB(:,2)==FB(nStart,1) );
    nStop = nStop( nStop > nStart );
    nStop = nStop(1);
    FBSections = [];
    while nStop ~= size( FB, 1 )
        FBSections = [ FBSections ; nStart nStop ];
        nStart = nStop + 1;
        nStop = find( FB(:,2)==FB(nStart,1) );
        nStop = nStop( nStop > nStart );
        nStop = nStop( 1 );
    end
    FBSections = [ FBSections ; nStart nStop ];
    N = size( FBSections, 1 );
    FacesList = cell( N, 1 );
    if N == 1 % single point of contact
        FacesList{1} = triThis;
    else
        triRest = [];
        for i = 1:N-1
            triTemp = ExtractFace( triThis, FB( FBSections(i,1):FBSections(i,2), 1 ) );
            triRest = [ triRest ; triTemp ];
            FacesList{i} = triTemp;
        end
        FacesList{N} = triThis( ~ismember( triThis, triRest, 'rows' ), : );
    end

end
