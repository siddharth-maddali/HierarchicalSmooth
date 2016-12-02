function [M] = Laplacian2D ( N )
	M = diag( sparse( ones( N-1, 1 ) ), 1 ) - diag( sparse( ones( N, 1 ) ) );
	M = M'*M;
	M( end, end ) = 1;
end
