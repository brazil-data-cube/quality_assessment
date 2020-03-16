#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import os
import time
# 3rdparty
import gdal
import numpy as np
import matplotlib.pyplot as plt

def diff_bands_stk(image_path1, image_path2, output_folder):
    #Set current working dir to first image
    os.chdir(image_path1)

    #get o stk de bandas .tif
    for filename in os.listdir(image_path1):
        if filename.endswith('.tif'):
            i1 = filename
            ds1 = gdal.Open(os.path.join(image_path1, filename))
    #Set current working dir to second image
    os.chdir(image_path2)

    for filename in os.listdir(image_path2):
        if filename.endswith('.tif'):
            i2 = filename
            ds2 = gdal.Open(os.path.join(image_path2, filename))

    #define o range de bandas da comparação
    numbands = ds1.RasterCount
    
    #define o driver
    driver = gdal.GetDriverByName("GTiff")

    #cria o nome do arquivo de saída
    output_file = os.path.basename(i1) + "_DIF_" + os.path.basename(i2)
    print(output_file)
    os.chdir(output_folder)
    print("CURRENTDIR:" + os.getcwd())

    #dimensoes do raster
    xsize = ds1.RasterXSize
    ysize = ds1.RasterYSize

    #cria o dataset vazio com as bandas da diferença
    dataset = driver.Create(output_file, xsize, ysize, numbands, gdal.GDT_Float32)

    # follow code is adding GeoTranform and Projection
    geotrans=ds1.GetGeoTransform()  #get GeoTranform from existed 'data0'
    proj=ds1.GetProjection() #you can get from a exsited tif or import 
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)

    #setting nodata value
    dataset.GetRasterBand(1).SetNoDataValue(-9999)

    #loop da diferença para gerar as bandas
    for b in range(numbands):
        #variáveis para gerar as estatísticas de ds1 e ds2
        band_ax = ds1.GetRasterBand(b+1)
        band_bx = ds2.GetRasterBand(b+1)
        #constroi o numpy array para fazer a diferença nas bandas
        band_a = ds1.GetRasterBand(b+1).ReadAsArray()
        band_b = ds2.GetRasterBand(b+1).ReadAsArray()
        #transforma para float
        band_a = band_a.astype(float)
        band_b = band_b.astype(float)
        #define -9999 para nan 
        band_a[band_a== -9999]=np.nan
        band_b[band_b== -9999]=np.nan
        #calcula a diferença para a banda
        band_diff = band_a - band_b
        #escreve a diferença no array
        dataset.GetRasterBand(b+1).WriteArray(band_diff)
        #obtem as estatísticas do dataset1 e dataset2
        stats_a = band_ax.GetStatistics(True, True)
        stats_b = band_bx.GetStatistics(True, True)
        #printa as estatísticas das bandas do dataset1 e dataset 2
        print("[ STATS 255] =  Band=%.1d, Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ((b+1), stats_a[0], stats_a[1], stats_a[2], stats_a[3] ))
        print("[ STATS 280] =  Band=%.1d, Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ((b+1), stats_b[0], stats_b[1], stats_b[2], stats_b[3] ))


if __name__ == '__main__':
    #image paths
    #TODO use lib sys to obtain parameters from command line
    image_path1 = '/home/fronza/Fronza_BDC/2_SEN2CORR_2_8_ancillary_data_test/2018_01_10/S2A_aux_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200311T190031.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
    image_path2 = '/home/fronza/Fronza_BDC/2_SEN2CORR_2_8_ancillary_data_test/2018_01_10/S2A_s_aux_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200311T193142.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
    output_folder = '/home/fronza/Fronza_BDC/2_SEN2CORR_2_8_ancillary_data_test/2018_01_10/output'

    print('STARTED diff_bands_stk')
    start = time.time()

    diff_bands_stk(image_path1, image_path2, output_folder)

    #limpa as variáveis
    ds=None
    ds1=None
    ds2=None

    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))