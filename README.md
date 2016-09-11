# Hierarchical Smoothing

## Description
This is an implementation of the hierarchical smoothing algorithm applicable to voxelated meshes of interface networks. This primarily directed at users of microstructure analysis software, specifically [DREAM.3D](link-dream3d). 

## Motivation
	- Faithfulness to mesoscopically smooth interfaces
	- Minimum user interference in deciding numerical parameters
	- Automatability over an entire volume
	- Proper treatment of GB interiors, triple lines and quad points

## Software requirements
	- Matlab R2013a or higher (extensive use of the `triangulation` object)
	- DREAM.3D v6.2 or higher (to import and export ASCII data)	__OR__
	- [HDFView](link-hdfview) to export from existing DREAM.3D data file

## Basic tutorial
 This tutorial for the Matlab implementation does not include the import and export of the required input data, which are in ASCII form for now. 

 [link-dream3d]:http://dream3d.bluequartz.net/
 [link-hdfview]:https://www.hdfgroup.org/products/java/hdfview/
