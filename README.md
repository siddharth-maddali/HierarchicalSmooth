# Hierarchical Smoothing
![alt tag](https://github.com/siddharth-mv/HierarchicalSmooth/blob/master/Banner.png?raw=true "Triple line fidelity with hierarchical smoothing")

## Description
This is an implementation of the hierarchical smoothing algorithm applicable to voxelated meshes of interface networks. Primarily directed at users of microstructure analysis software, specifically [DREAM.3D](http://dream3d.bluequartz.net/). 

## Motivation
1. Faithfulness to mesoscopically smooth interfaces
1. Minimum user interference in deciding numerical parameters
1. Automatability over an entire volume
1. Proper treatment of GB interiors, triple lines and quad points

A detailed description of the theory is given [here](http://arxiv.org/abs/1601.04699v4).

## Software requirements
1. Matlab R2013a or higher (extensive use of the `triangulation` object)
1. DREAM.3D v6.2 or higher (to import and export ASCII data)	__OR__
1. [HDFView](https://www.hdfgroup.org/products/java/hdfview/) to export from existing DREAM.3D data file

## Basic tutorial
 This tutorial for the Matlab implementation does not include the import and export of the required microstructure data relative to DREAM.3D. Included is a data set (in the `/examples/ex1` directory) containing the mesh of a 426-grain microstructure volume. The following steps illustrate the form of the input and implementation of the central `HierarchicalSmooth` routine.

* The input array `xDat` contains a set of N points in 3D in the form of a 3xN array. These represent voxelated sample points of the GB network.
```Matlab
xdat = load( 'examples/ex1/SharedVertexList.txt' );
xdat = xdat';
```
* The input array `tri` contains the Delaunay triangulation of the points in `xDat` in the form of an Mx3 integer array. A +1 offset is applied in order to accommodate the difference between DREAM.3D's 0-indexing and Matlab's 1-indexing.
```Matlab
tri = 1 + load( 'examples/ex1/SharedTriList.txt' );
```

* The Quick Surface mesh filter in DREAM.3D assigns a unique integer ID to every grain in the volume. The following input array serves to identify the grain boundary that a particular triangular element of array `tri` belongs to, in the form of an Mx2 integer array. The integers in each row denote the grains on either side of that particular triangular patch of grain boundary. 
```Matlab
fl = load( 'examples/ex1/FaceLabels.txt' );
```

* By default DREAM3D assigns the 'grain ID' of -1 to the top and bottom surfaces of the imaged volumes, and 0 to the sides respectively. These buffer regions are included in the array `fl` as well, for example the row [ 30, -1 ] in `fl` denotes the 'grain boundary' between the grain 30 and the top/bottom surface of the volume. These are unnecessary inputs to the smoothing routine and need to be filtered out to save time.
```Matlab
f = find( any( fl==-1 | fl==0, 2 ) );
fl( f, : ) = [];
tri( f, : ) = [];
```

* The final required input is the classification of the surface mesh nodes as belonging to surface interiors, triple lines or quad points. 
```Matlab
ntype = load( 'examples/ex1/NodeType.txt' );
ntype = ntype';
```

* The next line runs the smoothing routine with these arrays as input. NOTE: This could take time; around 25 minutes for 426 grains. Porting to C++ is under way. The log file generated by default is `Smooth.Default.log` and can be monitored in real time. 
```Matlab
xsmooth = HierarchicalSmooth( xdat, tri, fl, ntype );
```
Optional arguments for `HierarchicalSmooth` are described in the script file. Finally, the script `Test.m` plots a comparison between the smoothed and unsmoothed versions of a grain of the user's choice. 

## Acknowledgements
1. Anthony Rollett (Dept of MSE, CMU)
2. David Menasche (Dept of Physics, CMU)


