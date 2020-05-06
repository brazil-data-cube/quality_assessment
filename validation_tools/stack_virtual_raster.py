#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import logging
import os
import time
import sys
# 3rdparty
import gdal
import rasterio

def output(image_path, li_bands):
    # Set current working dir to first image
    os.chdir(image_path)
    logging.info('{}'.format(li_bands))
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Set output tif filename
    output_filename = image_path.split("\\")[-3] + '_stk.tif'
    # Create virtual raster
    ds = gdal.BuildVRT('img{}.vrt'.format(output_filename), li_bands, options=vrt_options)
    #Create output tif
    gdal.Translate(output_filename, ds, format='GTiff')


def list_bands(image_path, patterns):
    # Creates an empty list
    li_bands = list()
    # Search Sentinel-2 blue, green, red, nir and insert to the list
    for filename in os.listdir(image_path):
        if filename.endswith((patterns)):
            li_bands.append(os.path.join(filename))
    return li_bands

def stack_virtual_raster(image_path1, image_path2):
    #Creates an empty list
    #Search Sentinel-2 blue, green, red, nir and insert to the list
    li_bands1 = list_bands(image_path1, patterns)
    li_bands2 = list_bands(image_path2, patterns)

    output(image_path1, li_bands1)
    output(image_path2, li_bands2)

    print(li_bands1)
    print(li_bands2)

if __name__ == '__main__':
    
    if len(sys.argv) <= 2: # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED stack_virtual_raster')
    start = time.time()
    patterns_s2 = ("B02_10m.jp2", "B03_10m.jp2", "_B04_10m.jp2", "_B08_10m.jp2")
    patterns_lc8 = ("_B2.TIF", "_B3.TIF", "_B4.TIF", "_B5.TIF", "_B6.TIF", "_B7.TIF")
    patterns = patterns_lc8
    image_path1, image_path2 = sys.argv[1], sys.argv[2]
    stack_virtual_raster(image_path1, image_path2)
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
