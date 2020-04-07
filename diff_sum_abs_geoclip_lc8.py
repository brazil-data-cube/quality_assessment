#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import os
import time
import sys
# 3rdparty
import gdal
import numpy as np
#
def list_bands(image_path, patterns):
    # Creates an empty list
    li_bands = list()
    # Search Sentinel-2 blue, green, red, nir and insert to the list
    for filename in os.listdir(image_path):
        if filename.endswith((patterns)):
            li_bands.append(os.path.join(filename))
    return li_bands


def diff_sum_abs(image_path1,image_path2, output_folder):

    li_bands1 = list_bands(image_path1, patterns)
    li_bands2 = list_bands(image_path2, patterns)

    results = []
    # Create GTIF file
    driver = gdal.GetDriverByName("GTiff")

    # define nome do output
    output_file = li_bands1[0][:40] + "__DIF.tif"
    print(output_file)

    # ref t1 banda 1
    ref = gdal.Open(os.path.join(image_path1, li_bands1[1]))

    # usa a referencia para obter xsize e ysize
    xsize = ref.RasterXSize
    ysize = ref.RasterYSize

    # cria a imagem de saída
    os.chdir(output_folder)
    dataset = driver.Create(output_file, xsize, ysize, 1, gdal.GDT_Float32)

    # follow code is adding GeoTranform and Projection
    geotrans = ref.GetGeoTransform()  # get GeoTranform from existed 'data0'
    proj = ref.GetProjection()  # you can get from a exsited tif or import
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)

    for band in range(len(li_bands1)):
        ds1 = gdal.Open(os.path.join(image_path1, li_bands1[band]))
        ds2 = gdal.Open(os.path.join(image_path2, li_bands2[band]))
        projection = ds1.GetProjectionRef()
        geoTransform = ds1.GetGeoTransform()
        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1] * ds1.RasterXSize
        miny = maxy + geoTransform[5] * ds1.RasterYSize
        output = 'masked' + str(band) + '_output.tif'  # output file
        ds2c = gdal.Translate(output, ds2, format='MEM', projWin=[minx, maxy, maxx, miny], outputSRS=projection)
        bandtar = np.array(ds1.GetRasterBand(1).ReadAsArray().astype(float))
        bandref = np.array(ds2c.GetRasterBand(1).ReadAsArray().astype(float))
        results.append(np.abs(bandtar - bandref))
        diff_abs_sum = np.sum(results, axis=0)
        dataset.GetRasterBand(1).WriteArray(diff_abs_sum)
        print("proxima banda")

    ds1 = None
    ds2 = None
    ds2c = None
    bandref = None
    bandtar = None
    ref = None
    dataset = None

if __name__ == '__main__':
    if len(
            sys.argv) <= 3:  # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED diff_sum_abs_lc8')
    start = time.time()
    image_path1, image_path2, output_folder = sys.argv[1], sys.argv[2], sys.argv[3]
    patterns_lc8 = ("_B2.TIF", "_B3.TIF", "_B4.TIF", "_B5.TIF", "_B6.TIF", "_B7.TIF")
    patterns = patterns_lc8
    diff_sum_abs(image_path1, image_path2, output_folder)
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end - start))
