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