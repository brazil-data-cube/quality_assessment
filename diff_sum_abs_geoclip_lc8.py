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
#
def diff_sum_abs(image_path1,image_path2, output_folder):

    li_bands1 = list()
    li_bands2 = list()

    for filename in os.listdir(image_path1):
        if filename.endswith(("_B2.TIF", "_B3.TIF", "_B4.TIF", "_B5.TIF", "_B6.TIF", "_B7.TIF")):
            li_bands1.append(os.path.join(filename))

    for filename in os.listdir(image_path2):
        if filename.endswith(("_B2.TIF", "_B3.TIF", "_B4.TIF", "_B5.TIF", "_B6.TIF", "_B7.TIF")):
            li_bands2.append(os.path.join(filename))
    print(li_bands1)
    print(li_bands2)
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
    print(xsize , ysize)
    # follow code is adding GeoTranform and Projection
    geotrans = ref.GetGeoTransform()  # get GeoTranform from existed 'data0'
    proj = ref.GetProjection()  # you can get from a exsited tif or import
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)

    #create stk bands img
    os.chdir(output_folder)

    dataset = driver.Create(output_file, xsize, ysize, 1, gdal.GDT_Float32)

    for band in range(len(li_bands1)):
        ds1 = gdal.Open(os.path.join(image_path1, li_bands1[band]))
        ds2 = gdal.Open(os.path.join(image_path2, li_bands2[band]))
        # IN ORDER TO CLIP BY EXTENT EVERY IMAGE
        gt1 = ds1.GetGeoTransform()
        gt2 = ds2.GetGeoTransform()

        if gt1[0] < gt2[0]:  # CONDITIONAL TO SELECT THE CORRECT ORIGIN
            gt3 = gt2[0]
        else:
            gt3 = gt1[0]
        if gt1[3] < gt2[3]:
            gt4 = gt1[3]
        else:
            gt4 = gt2[3]
        xOrigin = gt3
        yOrigin = gt4

        pixelWidth = gt1[1]
        pixelHeight = gt1[5]
        r1 = [gt1[0], gt1[3], gt1[0] + (gt1[1] * ds1.RasterXSize), gt1[3] + (gt1[5] * ds1.RasterYSize)]
        r2 = [gt2[0], gt2[3], gt2[0] + (gt2[1] * ds2.RasterXSize), gt2[3] + (gt2[5] * ds2.RasterYSize)]
        intersection = [max(r1[0], r2[0]), min(r1[1], r2[1]), min(r1[2], r2[2]), max(r1[3], r2[3])]
        print(intersection)
        xmin = intersection[0]
        xmax = intersection[2]
        ymin = intersection[3]
        ymax = intersection[1]
        print(xmin, xmax, ymin, ymax)

        # Specify offset and rows and columns to read
        xoff = int((xmin - xOrigin) / pixelWidth)
        yoff = int((yOrigin - ymax) / pixelWidth)
        xcount = int((xmax - xmin) / pixelWidth)
        ycount = int((ymax - ymin) / pixelWidth)
        print(xoff, yoff, xcount, ycount)
        bandtar = np.array(ds1.GetRasterBand(1).ReadAsArray(xoff, yoff, xcount, ycount).astype(float))
        bandref = np.array(ds2.GetRasterBand(1).ReadAsArray(xoff, yoff, xcount, ycount).astype(float))
        results.append(np.abs(bandtar - bandref))
        diff_abs_sum = np.sum(results, axis=0)
        # cria a imagem de saída
        os.chdir(output_folder)

        dataset.GetRasterBand(1).WriteArray(diff_abs_sum)
        print("proxima banda")



if __name__ == '__main__':

    if len(
            sys.argv) <= 3:  # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED diff_sum_abs_lc8')
    start = time.time()
    image_path1, image_path2, output_folder = sys.argv[1], sys.argv[2], sys.argv[3]

    diff_sum_abs(image_path1, image_path2, output_folder)

    # limpa as variáveis
    ds1 = None
    ds2 = None
    bandref = None
    bandtar = None
    ref = None
    dataset = None
    diff_abs_sum = None
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end - start))
