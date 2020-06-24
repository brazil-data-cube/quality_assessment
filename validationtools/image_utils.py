# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020.

# Python Native
import os
# 3rd party
import geoarray
import numpy
from osgeo import gdal


def stack_virtual_raster(image_list, output=None):
    """
        Creates vrt from image list.

        Parameters:
            image_list ([str]): list of image paths that will be loaded.
            output (str): output directory.
        Returns:
            ds (gdal dataset): vrt of images.
    """
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Create virtual raster
    if output is not None:
        ds = gdal.BuildVRT(output, image_list, options=vrt_options)
    else:
        ds = gdal.BuildVRT('', image_list, options=vrt_options)
    return ds


def warp(ds, gdaloptions=None):
    """
        Warps an image.

        Parameters:
            ds (gdal dataset): dataset to be warped.
            gdaloptions (dict): dictionary of gdal options.
        Returns:
            ds (gdal dataset): warped dataset.
    """
    # if gdaloptions is None:
    #     geotrans, prj = ds.GetGeoTransform(), ds.GetProjection()
    #     gdaloptions = {'format':'VRT', 'srcSRS':prj, 'dstSRS':dst_epsg, 'xRes':geotrans[1], 'yRes':geotrans[5]}
    ds = gdal.Warp('', ds, **gdaloptions)

    return ds


def load_singband_geoarray(ds):
    """
        Load a single band into geoarray.

        Parameters:
            ds (gdal dataset): dataset to be loaded.
        Returns:
            geoArr (GeoArray): Geo Array.
    """
    ### Array, Geotrans and Projections
    array, geotrans, prj = ds.ReadAsArray(), ds.GetGeoTransform(), ds.GetProjection()

    ### Load into GeoArray
    geoArr = geoarray.GeoArray(array, geotrans, prj)

    del ds
    return geoArr


def load_multband_geoarray(ds):
    """
        Load a mult band into geoarray.

        Parameters:
            ds (gdal dataset): dataset to be loaded.
        Returns:
            geoArr (GeoArray): Geo Array.
    """
    ### Array, Geotrans and Projections
    array, geotrans, prj = ds.ReadAsArray(), ds.GetGeoTransform(), ds.GetProjection()

    ### Load into GeoArray
    geoArr = geoarray.GeoArray(numpy.transpose(array, (1,2,0)), geotrans, prj) #transpose due to geoarray using wrong gdal dimensions

    del ds
    return geoArr


def find_images(dir_path, bands):
    """
        Load a mult band into geoarray.

        Parameters:
            dir_path (str): path to directory containing images.
            bands (lst): list of bands.
        Returns:
            band_list (lst): list of paths to images.
    """
    ###Create the empty list
    band_list = list()
    listdir = os.listdir(dir_path)
    for band in bands:
        for filename in listdir:
            if band in filename:
                band_list.append(os.path.join(dir_path,filename))
    return band_list
