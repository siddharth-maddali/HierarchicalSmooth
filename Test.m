%%
% This script displays the comparision between individual 
% grains in their smoothed and unsmoothed forms. 

ngrains = unique( fl(:) );
printf( 'Number of grains in volume = %d', numel( ngrains ) );

GrainToPlot = 271; % set this to one of the integers in 'ngrains'.

trisub = tri( any( fl==GrainToPlot, 2 ), : );

figure; 
1 = subplot( 1, 2, 1 );
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
