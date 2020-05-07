# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020.
# Python Native
import os
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


def find_images(image_path, bands):
    band_list = list()
    listdir = os.listdir(image_path)
    for band in bands:
        for filename in listdir:
            if band in filename:
                band_list.append(filename)
    return band_list


def find_images_band(image_path, band):
    '''This function works with an dir path and a band (.tif) to be returned in that folders and subfolders
    retrieve a list of specific bands.
    img_list retrieve strings band paths
    band = band string that user need retrive. i.e.: red, nir, blue, B02, B01, etc.'''
    ###Create the empty list
    img_list = list()
    ###for in the folders to retrieve specific band in path, subdirs and files - using os.walk
    for path, subdirs, files in os.walk(image_path):
        for name in files:
            if name.endswith(band + '.tif'):
                img_list.append(os.path.join(image_path,name))
    return img_list

