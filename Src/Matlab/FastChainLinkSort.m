function [ FBOut ] = FastChainLinkSort( FBIn )
    
    FBOut = FBIn;
    for i = 2:size( FBOut,1)
        f = find( any( FBOut(i:end,:)==FBOut(i-1,2), 2 ) );
        FBOut( [i;f+i-1], : ) = FBOut( [f+i-1;i], : );
        if FBOut(i,2)== FBOut(i-1,2)
            FBOut( i, [ 1 2 ] ) = FBOut( i, [ 2 1 ] );
        end
    end
    
end