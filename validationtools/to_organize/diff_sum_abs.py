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

def diff_sum_abs(image_path1,image_path2, output_folder):
    '''
    documentar para sair automaticamente
    '''
    # get o stk de bandas .tif
    for filename in os.listdir(image_path1):
        if filename.endswith('.tif'):
            i1 = filename
            ds1 = gdal.Open(os.path.join(image_path1, filename))

    # Set current working dir to second image
    os.chdir(image_path2)

    for filename in os.listdir(image_path2):
        if filename.endswith('.tif'):
            i2 = filename
            ds2 = gdal.Open(os.path.join(image_path2, filename))

     # Create GTIF file
    driver = gdal.GetDriverByName("GTiff")

    #conta numero de bandas
    numbands = ds1.RasterCount
    print(numbands)

    #define nome do output
    # cria o nome do arquivo de saída
    output_file = os.path.basename(i1) + "_DIF_ABS_" + os.path.basename(i2)
    print(output_file)

    #ref t1 banda 1
    xsize = ds1.RasterXSize
    ysize = ds1.RasterYSize

    #cria a imagem de saída
    os.chdir(output_folder)
    dataset = driver.Create(output_file, xsize, ysize, 1, gdal.GDT_Float32)

    # follow code is adding GeoTranform and Projection
    geotrans=ds1.GetGeoTransform()  #get GeoTranform from existed 'data0'
    proj=ds1.GetProjection() #you can get from a exsited tif or import
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)

    #cria lista vazia para receber os dados
    results = []

    os.chdir(output_folder)
    for band in range(numbands):
        #ds1 = gdal.Open(os.path.join(img1, listbands1[band]))
        #ds2 = gdal.Open(os.path.join(img2, listbands2[band]))
        bandtar = ds1.GetRasterBand(band+1).ReadAsArray()
        bandref = ds2.GetRasterBand(band+1).ReadAsArray()
        # transforma para float
        bandtar = bandtar.astype(float)
        bandref = bandref.astype(float)
        #bandtar = np.array(ds1.GetRasterBand(band).ReadAsArray().astype(float))
        #bandref = np.array(ds2.GetRasterBand(band).ReadAsArray().astype(float))
        results.append(np.abs(bandtar - bandref))
        diff_abs_sum = np.sum(results, axis=0)
        dataset.GetRasterBand(1).WriteArray(diff_abs_sum)

if __name__ == '__main__':

    if len(
            sys.argv) <= 3:  # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED diff_sum_abs')
    start = time.time()
    image_path1, image_path2, output_folder = sys.argv[1], sys.argv[2], sys.argv[3]

    diff_sum_abs(image_path1, image_path2, output_folder)

    # limpa as variáveis
    ds1 = None
    ds2 = None
    bandref = None
    bandtar = None
    dataset = None
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end - start))