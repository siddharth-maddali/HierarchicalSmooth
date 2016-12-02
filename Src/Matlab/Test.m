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
%%
% This script displays the comparision between individual 
% grains in their smoothed and unsmoothed forms. 

ngrains = unique( fl(:) );
printf( 'Number of grains in volume = %d', numel( ngrains ) );

GrainToPlot = 271; % set this to one of the integers in 'ngrains'.

trisub = tri( any( fl==GrainToPlot, 2 ), : );

figure; 
s1 = subplot( 1, 2, 1 );
trisurf( trisub, xdat(1,:), xdat(2,:), xdat(3,:) );
axis equal; axis off; 

s2 = subplot( 1, 2, 2 );
trisurf( trisub, xsmooth(1,:), xsmooth(2,:), xsmooth(3,:) );
axis equal; axis off;

linkprop( [ s1 s2 ], { ...
	'CameraPosition', ...
	'CameraTarget', ...
	'CameraUpVector', ...
	'CameraViewAngle' } );

% This last statement links the axis properties of the two subplots, 
% so that the two figures can be rotated and zoomed simultaneously.
