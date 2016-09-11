function [ MLap, nUniq ] = GraphLaplacian( nTriangulation ) 

    nUniq = unique( nTriangulation(:) );
    nIdx = (1:numel(nUniq));
    [ ~, nSubTri ] = ismember( nTriangulation, nUniq );
    MLap = diag( sparse( zeros( numel( nUniq ), 1 ) ) );
    
    for i = 1:numel( nUniq ) 
       nThis = nIdx( i );
       nIndexes = unique( nSubTri( ...
           sum( nSubTri == nThis, 2 ) > 0, ...
           : ) )';
       nIndexes( nIndexes == nThis ) = [];
       MLap( nThis, nThis ) = numel( nIndexes );
       MLap( nThis, nIndexes ) = -ones( size( nIndexes ) );
              
    end
    
end
