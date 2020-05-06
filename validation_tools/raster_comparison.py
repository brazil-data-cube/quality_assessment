# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020.

# Python Native
import os
# 3rd party
import gdal
import numpy


def raster_intersection(path1, path2, output_dir=None, output_name=None, nodata1=None, nodata2=None):
    """Perform image intersection of two rasters with different extent and projection.
        Args:
            path1 (string) - path to image 1 (reference)
            path2 (string) - path to image 2 (target)
            output_dir (string) - path to output files
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
        Returns:
            dict Scene with sentinel file path
    """
    ### Open images
    ds1 = gdal.Open(path1)
    ds2 = gdal.Open(path2)
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

    ###Check if will create file on disk
    if output_dir is not None:
        driver = gdal.GetDriverByName("GTiff")
    else:
        driver = gdal.GetDriverByName("MEM")

    ###Create output datasource
    dataset = driver.Create(os.path.join(output_dir, output_name), xsize, ysize, 1, gdal.GDT_Float32)
    dataset.SetGeoTransform(geoTransform)
    dataset.SetProjection(projection)
    ###Setting nodata value
    dataset.GetRasterBand(1).SetNoDataValue(nodata)

    return ds1, ds2c, dataset


def raster_absolute_diff(path1, path2, output_dir=None, nodata1=None, nodata2=None):
    """Perform image absolute difference (support different extent and projection).
        Args:
            path1 (string) - path to image 1 (reference)
            path2 (string) - path to image 2 (target)
            output_dir (string) - path to output files
            nodata1 (number) - nodata value of image 1
            nodata2 (number) - nodata value of image 2
        Returns:
            dict Scene with sentinel file path
    """
    print('Calculating difference between {} and {}'.format(path1, path2))
    output_name = os.path.basename(path1)[0:-4] + "__DIF__" + os.path.basename(path2)[0:-4] + '.tif'
    ds1, ds2, dataset = raster_intersection(path1, path2, output_dir, output_name, nodata1, nodata2)

    ### Read bands with numpy to algebra
    nodata = dataset.GetRasterBand(1).GetNoDataValue()
    bandtar = numpy.array(ds1.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandtar = numpy.where(bandtar == nodata)
    bandref = numpy.array(ds2.GetRasterBand(1).ReadAsArray().astype(float))
    fill_bandref = numpy.where(bandref == nodata)

    ds1 = None
    ds2 = None
    diff = numpy.abs(bandtar - bandref)
    diff[fill_bandtar] = nodata
    diff[fill_bandref] = nodata
    dataset.GetRasterBand(1).WriteArray(diff)

    return dataset
