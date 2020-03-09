#
# This file is part of Brazil Data Cube Validationo Tools.
# Copyright (C) 2020 INPE.
#

# Python Native
import logging
import os
import time
# 3rdparty
import gdal
import rasterio


def stack_virtual_raster(image_path1, image_path2, output_folder):
    #Set current working dir to first image
    os.chdir(image_path1)

    #Creates an empty list
    li_bands1 = list()
    #Search Sentinel-2 blue, green, red, nir and insert to the list
    #TODO do a function that given a path and a pattern (or set of patterns) return your images
    for filename in os.listdir(image_path1):
        if filename.endswith("_B02_10m.jp2"):
            li_bands1.append(os.path.join(filename))

    for filename in os.listdir(image_path1):
        if filename.endswith("_B03_10m.jp2"):
            li_bands1.append(os.path.join(filename))
                
    for filename in os.listdir(image_path1):
        if filename.endswith("_B04_10m.jp2"):
            li_bands1.append(os.path.join(filename))

    for filename in os.listdir(image_path1):
        if filename.endswith("_B08_10m.jp2"):
            li_bands1.append(os.path.join(filename))

    #TODO do a function that creates the output
    logging.info('{}'.format(li_bands1))
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Create virtual raster
    ds1 = gdal.BuildVRT('img1.vrt', li_bands1, options=vrt_options)
    #Set output tif filename
    output_filename1 = image_path1.split("/")[-3] + '_stk.tif'  
    #Create output tif
    gdal.Translate(output_filename1, ds1, format='GTiff')

    #Set current working dir to second image
    os.chdir(image_path2)

    #Creates an empty list
    li_bands2 = list()
    #Search Sentinel-2 blue, green, red, nir and insert to the list
    #TODO use de function created for img1
    for filename in os.listdir(image_path2):
        if filename.endswith("_B02_10m.jp2"):
            li_bands2.append(os.path.join(filename))

    for filename in os.listdir(image_path2):
        if filename.endswith("_B03_10m.jp2"):
            li_bands2.append(os.path.join(filename))
                
    for filename in os.listdir(image_path2):
        if filename.endswith("_B04_10m.jp2"):
            li_bands2.append(os.path.join(filename))

    for filename in os.listdir(image_path2):
        if filename.endswith("_B08_10m.jp2"):
            li_bands2.append(os.path.join(filename))

    #TODO use the function created for img 1
    #TODO Check if crt_options is necessary, since it was defined before
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Create virtual raster
    ds2 = gdal.BuildVRT('img2.vrt', li_bands2, options=vrt_options)
    #Set output tif filename
    output_filename2 = image_path2.split("/")[-3] + '_stk.tif'  
    #Create output tif
    #os.chdir(output_folder)
    gdal.Translate(output_filename2, ds2, format='Gtiff')


def main():
    #image paths
    #TODO use lib sys to obtain parameters from command line
    image_path1 = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/S2A_MSIL2A_20180110T132221_N0206_R038_T23LLF_20191216T040849_255.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
    image_path2 = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/S2A_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200206T173655_280.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
    output_folder = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/diff'

    print('STARTED stack_virtual_raster')
    start = time.time()

    stack_virtual_raster(image_path1, image_path2, output_folder)

    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
