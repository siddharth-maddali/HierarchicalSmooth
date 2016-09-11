% Central routine that does hierarchical smoothing. 
%
% Inputs:
%
% xPoints - a 3xN array of floats, each column of which is a point in 3D
%   space.
%
% tri - a Mx3 array of integers that denote the delaunay triangulation of
%   the surface mesh of xPoints. M = # of mesh elements
% nFaceLabels - a Mx2 array of integers denoting the grain boundary patches
%   with each row specifying the grain IDs on either side of the patch. 
%
% nNodeType - Integer ID denoting type of sample points:
%     2: bulk GB interior
%     3: bulk triple line point
%     4: bulk quad point
%     12: surface GB interior
%     13: surface triple point
%     14: surface quad point
% Note: These designations conform to the DREAM.3D designations.
%
% varargin{5}: array of booleans of the number of columns in xPoints, that
% denotes whether each of the xPoints has already been smoothed or not.
% This is provided as an additional argument in case it is desired to
% resume smoothing from some intermediate point.
%
% varargin{6}: A log file that dumps information to disk. Defaults to
% "Smooth.Default.log". 
% 
% Outputs: 
% 
% xSmoothed - An array of floats, same size as xPoints, containing the corresponsing 
% 	smoothed points. 
% 
% bPointSmoothed - Returns the (new or modified) version of varargin{5}.
%

function [ xSmoothed ] = HeirarchicalSmooth( xPoints, tri, nFaceLabels, nNodeType, varargin )

    warning( 'off', 'MATLAB:triangulation:PtsNotInTriWarnId' );

	if nargin == 5
		bPointSmoothed = varargin{1};
	else
	   bPointSmoothed = false( 1, size( xPoints, 2 ) );
	end
    xSmoothed = xPoints;
    
    nFaceLabels = [ min(nFaceLabels,[],2) max(nFaceLabels,[],2) ];
    nUniqueFaceLabels = unique( nFaceLabels, 'rows' );

    if nargin == 6
        fid = fopen( varargin{6}, 'a' );
    else
        fid = fopen( 'Smooth.Default.log', 'a' );
    end

    % first smooth triple lines AND DO NOT TOUCH AGAIN!
    tic; 
    for i = 1:size( nUniqueFaceLabels, 1 )
        
        triThisBoundary0 = tri( ismember( nFaceLabels, nUniqueFaceLabels(i,:), 'rows' ), : );

		% Debug messages
		fprintf( fid, 'Perimeter smooth: FaceLabels (%d, %d)\n', nUniqueFaceLabels(i,:) );

        TRoot = triangulation( triThisBoundary0, xPoints' );
        [ FL, ~ ] = DifferentiateFaces( TRoot );
		tmp = 1;
		while tmp <= numel( FL )
			if numel( FL{tmp} ) == 0
				FL(tmp) = [];
			else
				tmp = tmp + 1;
			end
		end

%		FL

        for k = 1:numel( FL )
            triThisBoundary = FL{k};
            if numel( triThisBoundary ) == 0
                continue;
            end
            nUniq = unique( triThisBoundary );
            nUniq = [ (1:numel(nUniq))' nUniq ];
            [ ~, triThisBoundary ] = ismember( triThisBoundary, nUniq(:,2) ); % convert back to original indexes later
            xDeezPoints = xSmoothed( :, nUniq(:,2)' );
            nDeezTypes = nNodeType( nUniq(:,2)' );
    
            T = triangulation( triThisBoundary, xDeezPoints' );
            FB = FastChainLinkSort( T.freeBoundary );
    
            PPerimeter = xDeezPoints( :, FB(:,1)' );    % already sorted in winding order!!!
            nTypePerimeter = nDeezTypes( FB(:,1) );
    
            nTripleJnRanges = find( nTypePerimeter == 4 | nTypePerimeter == 14 );
            if size( nTripleJnRanges, 1 ) == 1 &&size( nTripleJnRanges, 2 ) > 1
                nTripleJnRanges = nTripleJnRanges';
            end
        	nTripleJnRanges = [ nTripleJnRanges  circshift( nTripleJnRanges, [ -1, 0 ] ) ];

			if numel( nTripleJnRanges ) == 0
				continue;
			end

%			nTripleJnRanges

            for j = 1:size( nTripleJnRanges, 1) - 1
                InternalRange = nTripleJnRanges(j,1):nTripleJnRanges(j,2);
                TheRangeICareAbout = nUniq( FB( InternalRange', 1 ), 2 )';
                if all( bPointSmoothed( TheRangeICareAbout ) ) == true
                    continue; 
                end
                PThis = PPerimeter( :, InternalRange );
    
                if diff( nTripleJnRanges( j, : ) ) == 1
                    bPointSmoothed( TheRangeICareAbout ) = true; 
                    continue;
                end
                PThis = Smooth( PThis', 1e-7, 1000 )';
                PThis = Smooth( PThis', 1e-7, 1000 )';
                PThis = Smooth( PThis', 1e-7, 1000 )';
                xSmoothed( :, TheRangeICareAbout ) = PThis;
                bPointSmoothed( TheRangeICareAbout ) = true;
    
            end

%			nTripleJnRanges
%			size( PPerimeter )

        	nLastRange = nTripleJnRanges( end, : );
        	nLastRange = [ nLastRange(1):size(PPerimeter,2) 1:nLastRange(2) ]';
            TheRangeICareAbout = nUniq( FB( nLastRange, 1 ), 2 )';
            if all( bPointSmoothed( TheRangeICareAbout ) ) == true
                continue; 
            end
            PThis = PPerimeter( :, nLastRange );
            if range( nLastRange ) == size( PThis, 2 ) - 1
            	bPointSmoothed( TheRangeICareAbout ) = true; 
                continue;
            end
            PThis = Smooth( PThis', 1e-7, 1000 )';
            PThis = Smooth( PThis', 1e-7, 1000 )';
            PThis = Smooth( PThis', 1e-7, 1000 )';
            xSmoothed( :, TheRangeICareAbout ) = PThis;
            bPointSmoothed( TheRangeICareAbout ) = true;
        end
                
    end
    t = toc; 
    fprintf( fid, 'Done smoothing triple lines. Time taken = %d minutes %f seconds\n', floor( t/60 ), rem( t, 60 ) );
    
    % NOW, smooth boundary interiors...
    tic; 
	for i = 1:size( nUniqueFaceLabels, 1 )
        triThisBoundary0 = tri( ismember( nFaceLabels, nUniqueFaceLabels(i,:), 'rows' ), : );

		% Debug messages
		fprintf( fid, 'Boundary smooth: FaceLabels (%d, %d)\n', nUniqueFaceLabels(i,:) );


        TRoot = triangulation( triThisBoundary0, xPoints' );
        FL = DifferentiateFaces( TRoot );
        for k = 1:numel( FL )
            triThisBoundary = FL{k};
            nUniq = unique( triThisBoundary );
            if all( bPointSmoothed( nUniq ) ) == true
                continue;
            end
            nUniq = [ (1:numel(nUniq))' nUniq ];
            [ ~, triThisBoundary ] = ismember( triThisBoundary, nUniq(:,2) ); % convert back to original indexes later
            xDeezPoints = xSmoothed( :, nUniq(:,2)' ); % points belonging to this grain boundary
            nDeezTypes = nNodeType( nUniq(:,2)' );
    
    
    
            L = GraphLaplacian( triThisBoundary );
            f = find( ~( nDeezTypes == 2 | nDeezTypes == 12 ) )';
            xDeezSmoothed = Smooth( xDeezPoints', 1e-7, 1000, L, f )';
            xDeezSmoothed = Smooth( xDeezSmoothed', 1e-7, 1000, L, f )';
            xDeezSmoothed = Smooth( xDeezSmoothed', 1e-7, 1000, L, f )';
    %         xDeezSmoothed = Smooth( xDeezSmoothed', 1e-7, 1000, L, f )';
    %         xDeezSmoothed = Smooth( xDeezSmoothed', 1e-7, 1000, L, f )';
    
    
            xSmoothed( :, nUniq(:,2)' ) = xDeezSmoothed;
        end
    end
        
    t = toc; 
    fprintf( fid, 'Done smoothing interiors. Time taken = %d minutes %f seconds\n', floor( t/60 ), rem( t, 60 ) );
    % ...phew!
	fclose( fid );
    warning( 'on', 'MATLAB:triangulation:PtsNotInTriWarnId' );
    
end
