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


def stack_virtual_raster(image_path1, image_path2):
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
    print(li_bands1)
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
        if filename.endswith("B02.jp2"):
            li_bands2.append(os.path.join(filename))

    for filename in os.listdir(image_path2):
        if filename.endswith("B03.jp2"):
            li_bands2.append(os.path.join(filename))
                
    for filename in os.listdir(image_path2):
        if filename.endswith("B04.jp2"):
            li_bands2.append(os.path.join(filename))

    for filename in os.listdir(image_path2):
        if filename.endswith("B08.jp2"):
            li_bands2.append(os.path.join(filename))

    #TODO use the function created for img 1
    #TODO Check if vrt_options is necessary, since it was defined before
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Create virtual raster
    ds2 = gdal.BuildVRT('img2.vrt', li_bands2, options=vrt_options)
    #Set output tif filename
    output_filename2 = image_path2.split("/")[-1] + '_stk.tif'  
    gdal.Translate(output_filename2, ds2, format='Gtiff')
    print(li_bands1)
    print(li_bands2)

if __name__ == '__main__':
    
    if len(sys.argv) <= 2: # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED stack_virtual_raster')
    start = time.time()
    image_path1, image_path2 = sys.argv[1], sys.argv[2]
    stack_virtual_raster(image_path1, image_path2)
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
