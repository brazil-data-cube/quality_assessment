#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import os
# 3rd party
import gdal
import numpy as np


def list_bands(image_patter, bands):
    # Creates an empty list
    band_list = list()
    for band in bands:
        img_path = image_patter.format(band)
        band_list.append(img_path)
    return band_list


### INPUT ARGS
bands_lc8_toa = ('_B1.TIF', '_B2.TIF', '_B3.TIF', '_B4.TIF', '_B5.TIF', '_B6.TIF', '_B7.TIF',
                 '_B9.TIF')  # Landsat 8 comparable spectral bands
bands_s2_toa = ('_B01.jp2', '_B02.jp2', '_B03.jp2', '_B04.jp2', '_B8A.jp2', '_B11.jp2', '_B12.jp2',
                '_B10.jp2')  # Sentinel 2 comparable spectral bands

### INPUT PATHS
img_path_s2 = '/home/fronza/Fronza_BDC/4_SR_NBAR_VAL/Data/Images/TOA/L1C_T21LXK_A024088_20200201T135637/S2A_MSIL1C_20200201T135641_N0208_R067_T21LXK_20200201T154031.SAFE/GRANULE/L1C_T21LXK_A024088_20200201T135637/IMG_DATA/T21LXK_20200201T135641{}'
img_path_lc8 = '/home/fronza/Fronza_BDC/4_SR_NBAR_VAL/Data/Images/TOA/LC08_L1TP_227067_20200201_20200211_01_T1/LC08_L1TP_227067_20200201_20200211_01_T1{}'
# img_path_s2 = '/home/marujo/Downloads/comparison/S2A_MSIL1C_20200201T135641_N0208_R067_T21LXK_20200201T154031.SAFE/GRANULE/L1C_T21LXK_A024088_20200201T135637/IMG_DATA/T21LXK_20200201T135641{}'
# img_path_lc8 = '/home/marujo/Downloads/comparison/LC08_L1TP_227067_20200201_20200211_01_T1/LC08_L1TP_227067_20200201_20200211_01_T1{}'

### OUTPUT PATH
# output_folder = '/home/marujo/Downloads/comparison/out'
output_folder = '/home/fronza/Fronza_BDC/4_SR_NBAR_VAL/Data/Images/TOA/DIFF'

### LIST BANDS
li_bands_s2 = list_bands(img_path_s2, bands_s2_toa)
li_bands_lc8 = list_bands(img_path_lc8, bands_lc8_toa)

# for band in range(len(li_bands_s2)):
for band in range(1):
    print(band)
    ### Open images
    print(li_bands_s2[band])
    ds1 = gdal.Open(li_bands_s2[band])
    print(li_bands_lc8[band])
    ds2 = gdal.Open(li_bands_lc8[band])
    print(ds2)

    ### print median to check raster
    print(ds2.GetRasterBand(1).ReadAsArray().shape)
    print('MEDIAds2 ' + str(np.nanmean(np.array(ds2.GetRasterBand(1).ReadAsArray().astype(float)))))

    ### Get extent from ds1
    projection = ds1.GetProjectionRef()
    geoTransform = ds1.GetGeoTransform()

    ### Prints to guide
    print('Geotrans iniciais (extent diferente, resolucao diferente)')
    print(ds1.GetGeoTransform())
    print(ds2.GetGeoTransform())

    ###Get minx and max y
    minx = geoTransform[0]
    maxy = geoTransform[3]

    ###Raster dimensions
    xsize = ds1.RasterXSize
    ysize = ds1.RasterYSize

    maxx = minx + geoTransform[1] * xsize
    miny = maxy + geoTransform[5] * ysize

    ###Set output
    os.chdir(output_folder)
    gdaloptions = {'format': 'Gtiff', 'xRes': geoTransform[1], 'yRes': geoTransform[5], 'dstSRS': projection}
    # , 'outputBoundsSRS': projection, 'outputBounds':[minx, maxy, maxx, miny]
    ds2w = gdal.Warp('outputds2w.tif', ds2, **gdaloptions)

    print('Geotrans apos warp do 2 (extent difente, res igual):')
    print(ds1.GetGeoTransform())
    print(ds2w.GetGeoTransform())

    print(ds2w.GetRasterBand(1).ReadAsArray().shape)
    print('MEDIAw ' + str(np.nanmean(np.array(ds2w.GetRasterBand(1).ReadAsArray().astype(float)))))

    ds2c = gdal.Translate('outputds2c.tif', ds2w, format='Gtiff', projWin=[minx, maxy, maxx, miny],
                          outputSRS=projection)

    # print('Geotrans apos translate do 2 (extent quase igual, res igual):')
    # print([minx, maxy, maxx, miny])
    # print(ds1.GetGeoTransform())
    # print(ds2c.GetGeoTransform())

    # print(ds2c.GetRasterBand(1).ReadAsArray().shape)
    # print('MEDIAc ' + str(np.nanmean(np.array(ds2c.GetRasterBand(1).ReadAsArray().astype(float)))))

    ###Set driver
    driver = gdal.GetDriverByName("GTiff")

    ###Create output file
    output_name = os.path.basename(li_bands_s2[band]) + "__DIF__" + os.path.basename(li_bands_lc8[band]) + '.tif'
    os.chdir(output_folder)
    print("CURRENTDIR:" + os.getcwd())

    ###Cria o dataset vazio com a banda da diferença
    dataset = driver.Create(output_name, xsize, ysize, 1, gdal.GDT_UInt16)
    dataset.SetGeoTransform(geoTransform)
    dataset.SetProjection(projection)

    ###Setting nodata value
    # dataset.GetRasterBand(1).SetNoDataValue(-9999)

    ### Read bands with numpy to algebra
    bandtar = np.array(ds1.GetRasterBand(1).ReadAsArray().astype(float))
    bandref = np.array(ds2c.GetRasterBand(1).ReadAsArray().astype(float))

    print('Tamanho dos arrays (matriz com msms tamanhos)')
    print(bandref.shape)
    print(bandtar.shape)
    # print(ds1.GetGeoTransform())
    # print(ds2c.GetGeoTransform())
    diff = np.abs(bandtar - bandref)
    dataset.GetRasterBand(1).WriteArray(diff)

    ### Clear cache
    # dentro do for para esvaziar a variavel a cada iteração para q a proxima não pegue ja com valor dentro
    ds1 = None
    ds2 = None
    ds2w = None
    ds2c = None
    diff = None
    dataset = None
    bandtar = None
    bandref = None

    print("proxima banda")

