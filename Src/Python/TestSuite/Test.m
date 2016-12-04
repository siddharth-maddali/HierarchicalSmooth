%P = load( 'SharedVertexList.txt' )';
%Q = load( 'SmoothVertexList.txt' )';
%
%
%tri = 1 + load( 'SharedTriList.txt' );
%FL = load( 'FaceLabels.txt' );
%T = load( 'NodeType.txt' );

nGrain = [ 198 403 ]
f = find( any( ismember( FL, nGrain ), 2 ) );
triSub = tri( f, : );
U = unique( triSub );
TSub = T( U );
TJ = U( find( rem( TSub, 3 ) == 0 ) );
QJ = U( find( rem( TSub, 4 ) == 0 ) );

subplot( 1, 2, 1 );
trisurf( triSub, P(1,:), P(2,:), P(3,:), 'EdgeColor', 0.5*[ 1 1 1 ], 'FaceColor', 'w' ); 
hold on;
plot3( P(1,TJ), P(2,TJ), P(3,TJ), 'ok', 'LineWidth', 2 );
plot3( P(1,QJ), P(2,QJ), P(3,QJ), 'dc', 'LineWidth', 3 );
axis equal;

subplot( 1, 2, 2 );
trisurf( triSub, Q(1,:), Q(2,:), Q(3,:), 'EdgeColor', 0.5*[ 1 1 1 ], 'FaceColor', 'w');
hold on;
plot3( Q(1,TJ), Q(2,TJ), Q(3,TJ), 'ok', 'LineWidth', 2 );
plot3( Q(1,QJ), Q(2,QJ), Q(3,QJ), 'dc', 'LineWidth', 3 );
axis equal;