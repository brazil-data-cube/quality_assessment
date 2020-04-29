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

def output_s2(image_path, li_bands):
    # Set current working dir to SENTINEL-2X image DIR
    os.chdir(image_path)
    logging.info('{}'.format(li_bands))
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Set output tif filename
    output_filename = image_path.split("/")[-2] + '_stk.tif'
    # Create virtual raster
    ds = gdal.BuildVRT('img{}.vrt'.format(output_filename), li_bands, options=vrt_options)
    #Create output tif
    gdal.Translate(output_filename, ds, format='GTiff')

def output_lc8(image_path, li_bands):
    # Set current working dir to LANDSAT-8 image DIR
    os.chdir(image_path)
    logging.info('{}'.format(li_bands))
    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Set output tif filename
    output_filename = image_path.split("/")[-1] + '_stk.tif'
    # Create virtual raster
    ds = gdal.BuildVRT('img{}.vrt'.format(output_filename), li_bands, options=vrt_options)
    #Create output tif
    gdal.Translate(output_filename, ds, format='GTiff')

def list_bands(image_path, patterns):
    # Creates an empty list
    li_bands = []
    # Search Sentinel-2 blue, green, red, nir and insert to the list
    for filename in os.listdir(image_path):
        if filename.endswith((patterns)):
            li_bands.append(filename)
    li_bands.sort()
    return li_bands

def stack_virtual_raster(image_path1, image_path2):
    #seleciona qual pattern para construir o stk TODO aprimorar para o pacote
    li_bands1 = list_bands(image_path1, bands_s2_sr)
    [x for _, x in sorted(zip(bands_s2_sr, li_bands1))]
    li_bands2 = list_bands(image_path2, bands_s2_sr)
    [x for _, x in sorted(zip(bands_s2_sr, li_bands2))]
    output_s2(image_path1, li_bands1)
    output_lc8(image_path2, li_bands2)
    print(li_bands1)
    print(li_bands2)

if __name__ == '__main__':
    
    if len(sys.argv) <= 2: # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED stack_virtual_raster')
    start = time.time()

    #bands_lc8_toa = ('_B1.TIF', '_B2.TIF', '_B3.TIF', '_B4.TIF', '_B5.TIF', '_B6.TIF', '_B7.TIF', '_B9.TIF')  # Landsat 8 comparable spectral bands
    #bands_s2_toa = ('_B01.jp2', '_B02.jp2', '_B03.jp2', '_B04.jp2', '_B8A.jp2', '_B11.jp2', '_B12.jp2', '_B10.jp2')  # Sentinel 2 comparable spectral bands

    #bands_s2_sr = ("B02_10m.jp2", "B03_10m.jp2", "_B04_10m.jp2", "_B08_10m.jp2")

    #bands_lc8_sr = ("_B2.TIF", "_B3.TIF", "_B4.TIF", "_B5.TIF", "_B6.TIF", "_B7.TIF")

    image_path1, image_path2 = sys.argv[1], sys.argv[2]

    stack_virtual_raster(image_path1, image_path2)

    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
