# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020.

# Python Native
import os
# 3rd party
import gdal
import numpy


def raster_intersection(ds1, ds2, nodata1=None, nodata2=None, output_name1=None, output_name2=None):
    """Perform image intersection of two rasters with different extent and projection.
        Args:
            ds1 (GDAL dataset) - GDAL dataset of an image
            ds2 (GDAL dataset) - GDAL dataset of an image
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
            output_name1 (string) - path to output intersection of ds1
            output_name2 (string) - path to output intersection of ds2
        Returns:
            dataset1 (GDAL dataset), dataset2 (GDAL dataset): intersection dataset1 and intersection dataset2.
    """
    ###Setting nodata
    nodata = 0
    ###Check if images NoData is set
    if nodata2 is not None:
        nodata = nodata2
        ds2.GetRasterBand(1).SetNoDataValue(nodata)
    else:
        if ds2.GetRasterBand(1).GetNoDataValue() is None:
            ds2.GetRasterBand(1).SetNoDataValue(nodata)

    if nodata1 is not None:
        nodata = nodata1
        ds1.GetRasterBand(1).SetNoDataValue(nodata1)
    else:
        if ds1.GetRasterBand(1).GetNoDataValue() is None:
            ds1.GetRasterBand(1).SetNoDataValue(nodata)

    ### Get extent from ds1
    projection = ds1.GetProjectionRef()
    geoTransform = ds1.GetGeoTransform()

    ###Get minx and max y
    minx = geoTransform[0]
    maxy = geoTransform[3]

    ###Raster dimensions
    xsize = ds1.RasterXSize
    ysize = ds1.RasterYSize

    maxx = minx + geoTransform[1] * xsize
    miny = maxy + geoTransform[5] * ysize

    ###Warp to same spatial resolution
    gdaloptions = {'format': 'MEM', 'xRes': geoTransform[1], 'yRes': geoTransform[5], 'dstSRS': projection}
    ds2w = gdal.Warp('', ds2, **gdaloptions)
    ds2 = None

    ###Translate to same projection
    ds2c = gdal.Translate('', ds2w, format='MEM', projWin=[minx, maxy, maxx, miny], outputSRS=projection)
    ds2w = None
    ds1c = gdal.Translate('', ds1, format='MEM', projWin=[minx, maxy, maxx, miny], outputSRS=projection)
    ds1 = None

    ###Check if will create file on disk
    if output_name1 is not None or output_name2 is not None:
        driver = gdal.GetDriverByName("GTiff")
        if output_name1 is None:
            output_name1 = 'intersection1.tif'
        if output_name2 is None:
            output_name2 = 'intersection2.tif'
    else:
        driver = gdal.GetDriverByName("MEM")
        output_name1 = ''
        output_name2 = ''

    dataset1 = driver.Create(output_name1, xsize, ysize, 1, ds1c.GetRasterBand(1).DataType)
    dataset1.SetGeoTransform(geoTransform)
    dataset1.SetProjection(projection)
    dataset1.GetRasterBand(1).SetNoDataValue(nodata) ###Setting nodata value
    dataset1.GetRasterBand(1).WriteArray(ds1c.GetRasterBand(1).ReadAsArray())

    dataset2 = driver.Create(output_name2, xsize, ysize, 1, ds2c.GetRasterBand(1).DataType)
    dataset2.SetGeoTransform(geoTransform)
    dataset2.SetProjection(projection)
    dataset2.GetRasterBand(1).SetNoDataValue(nodata) ###Setting nodata value
    dataset2.GetRasterBand(1).WriteArray(ds2c.GetRasterBand(1).ReadAsArray())

    ds1c = None
    ds2c = None

    return dataset1, dataset2


def raster_absolute_diff(ds1, ds2, nodata1=None, nodata2=None, output_file=None):
    """Perform image absolute difference (support different extent and projection).
        Args:
            path1 (string) - path to image 1 (reference)
            path2 (string) - path to image 2 (target)
            output_dir (string) - path to output files
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
        Returns:
            dataset (GDAL dataset): dataset containing absolute difference between ds1 and ds2.
    """
    if output_file is None:
        output_file = 'abs_diff.tif'
    ds1_intersec, ds2_intersec = raster_intersection(ds1, ds2, nodata1, nodata2, None, None)

    ### Read bands with numpy to algebra
    nodata = ds1_intersec.GetRasterBand(1).GetNoDataValue()
    bandtar = numpy.array(ds1_intersec.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandtar = numpy.where(bandtar == nodata)
    bandref = numpy.array(ds2_intersec.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandref = numpy.where(bandref == nodata)

    ### Get extent from ds1
    projection = ds1.GetProjectionRef()
    geoTransform = ds1.GetGeoTransform()
    [cols, rows] = ds1.GetRasterBand(1).ReadAsArray().shape

    ds1 = None
    ds2 = None
    diff = numpy.abs(bandtar - bandref)
    diff[fill_bandtar] = nodata
    diff[fill_bandref] = nodata

    ###Check if will create file on disk
    if output_file is not None:
        driver = gdal.GetDriverByName("GTiff")
    else:
        driver = gdal.GetDriverByName("MEM")
        output_file = ''

    dataset = driver.Create(output_file, rows, cols, 1, ds1_intersec.GetRasterBand(1).DataType)
    dataset.SetGeoTransform(geoTransform)
    dataset.SetProjection(projection)
    dataset.GetRasterBand(1).SetNoDataValue(nodata)
    dataset.GetRasterBand(1).WriteArray(diff)

    return dataset
