function [ triFace ] = ExtractFace( triFull, SeedArray )

    nPrevSize = 0;
    triFace = triFull( sum( ismember( triFull, SeedArray ), 2 ) > 1, : );
    nNextSize = size( triFace, 1 );
    while nNextSize ~= nPrevSize
        nPrevSize = nNextSize;
        SeedArray = unique( triFace );
        triFace = triFull( sum( ismember( triFull, SeedArray ), 2 ) > 1, : );
        nNextSize = size( triFace, 1 );
    end

end