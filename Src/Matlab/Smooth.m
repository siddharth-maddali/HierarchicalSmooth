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
function [ yOut, IterData, fLandscape ] = Smooth( yIn, fThreshold, nMaxIterations, varargin )

    IterData = [];
    if nargin > 3 % nargin = 3 or 5
        L = varargin{1}; 
        nFixed = varargin{2};
    else
        N  = size( yIn, 1 );
        L = Laplacian2D( N );    % assuming points are sequentially connected and endpoints are fixed
        nFixed = [ 1 N ];
    end
	nMobile = (1:size(yIn,1)); nMobile = nMobile( ~ismember( nMobile, nFixed ) );
    if numel( nMobile ) < 1
        yOut = yIn; 
        IterData = [];
        fLandscape = [];
        return;
    end
    LRed = L( :, nMobile );
    LRed = LRed( nMobile', : );

    fConst = L; fConst( :, nMobile ) = 0;
    fConst = fConst * yIn;
    fConst( nFixed', : ) = [];
    
    D = ( L > 0 ) .* L; % diagonal matrix
    A = ( L < 0 ) .* L; % adjacency matrix
    AyIn = A * yIn;
        
    fSmallEye = diag( sparse( ones( numel(nMobile), 1 ) ) );
    yMobile = yIn( nMobile', : );
        
    fEps = 0.5;
    fStep = fEps / 2;
    nIterations = 1;
    
    fEps1 = fEps; fEps2 = fEps+fThreshold;
	yOut1 = ( (1-fEps1)*fSmallEye + fEps1*(LRed'*LRed) ) \ ( (1-fEps1)*yMobile - fEps1*LRed'*fConst );
    yOut2 = ( (1-fEps2)*fSmallEye + fEps2*(LRed'*LRed) ) \ ( (1-fEps2)*yMobile - fEps2*LRed'*fConst );

    yTemp1 = yIn; yTemp1( nMobile', : ) = yOut1;
    yTemp2 = yIn; yTemp2( nMobile', : ) = yOut2;
    
    fObj1 = D*yTemp1 + AyIn; fObj1 = exp( trace( fObj1'*fObj1 ) ); 
    fObj2 = D*yTemp2 + AyIn; fObj2 = exp( trace( fObj2'*fObj2 ) ); 
    fSlope = ( fObj2 - fObj1 ) / fThreshold;
    
    while abs( fSlope ) > fThreshold && nIterations < nMaxIterations
        if fSlope > 0 
            fEps = fEps - fStep;
        else
            fEps = fEps + fStep;
        end
        fStep = fStep / 2;
        fEps1 = fEps; fEps2 = fEps+fThreshold;
    	yOut1 = ( (1-fEps1)*fSmallEye + fEps1*(LRed'*LRed) ) \ ( (1-fEps1)*yMobile - fEps1*LRed'*fConst );
        yOut2 = ( (1-fEps2)*fSmallEye + fEps2*(LRed'*LRed) ) \ ( (1-fEps2)*yMobile - fEps2*LRed'*fConst );

        yTemp1 = yIn; yTemp1( nMobile', : ) = yOut1;
        yTemp2 = yIn; yTemp2( nMobile', : ) = yOut2;

        fObj1 = D*yTemp1 + AyIn; fObj1 = exp( trace( fObj1'*fObj1 ) ); 
        fObj2 = D*yTemp2 + AyIn; fObj2 = exp( trace( fObj2'*fObj2 ) ); 
        fSlope = ( fObj2 - fObj1 ) / fThreshold;
        IterData = [ IterData; ...
            fEps, fObj1 ];
        nIterations = nIterations + 1;
            
    end
    
    yOut = ( yTemp1 + yTemp2 ) / 2;
    
    fEpses = linspace( 0, 1, 1000 )';
    fLandscape = [ fEpses zeros( numel( fEpses ), size( yIn, 2 ) ) ];
	for i = 1:numel( fEpses )
    	fMyEps = fEpses( i );
        yOutThis = ( (1-fMyEps)*fSmallEye + fMyEps*(LRed'*LRed) ) \ ( (1-fMyEps)*yMobile - fMyEps*LRed'*fConst );
        yTemp = yIn; yTemp( nMobile', : ) = yOutThis;
        fObj = D*yTemp + AyIn; [ ~, el ]= eig( fObj'*fObj );
        fLandscape( i, 2:end ) = diag( el )';
	end
    
    
end
