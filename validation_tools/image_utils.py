# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020.

# 3rd party
import geoarray
import numpy
from osgeo import gdal


def stack_virtual_raster(image_list, output=None):
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Create virtual raster
    if output is not None:
        ds = gdal.BuildVRT(output, image_list, options=vrt_options)
    else:
        ds = gdal.BuildVRT('', image_list, options=vrt_options)
    return ds


def warp(ds, gdaloptions):
    # geotrans, prj = ds.GetGeoTransform(), ds.GetProjection()
    # gdaloptions = {'format':'VRT', 'srcSRS':prj, 'dstSRS':dst_epsg, 'xRes':geotrans[1], 'yRes':geotrans[5]}
    ds = gdal.Warp('', ds, **gdaloptions)

    return ds


def load_singband_geoarray(ds):
    ### Array, Geotrans and Projections
    array, geotrans, prj = ds.ReadAsArray(), ds.GetGeoTransform(), ds.GetProjection()

    ### Load into GeoArray
    geoArr = geoarray.GeoArray(array, geotrans, prj)

    del ds
    return geoArr


def load_multband_geoarray(ds):
    ### Array, Geotrans and Projections
    array, geotrans, prj = ds.ReadAsArray(), ds.GetGeoTransform(), ds.GetProjection()

    ### Load into GeoArray
    geoArr = geoarray.GeoArray(numpy.transpose(array, (1,2,0)), geotrans, prj) #transpose due to geoarray using wrong gdal dimensions

    del ds
    return geoArr
