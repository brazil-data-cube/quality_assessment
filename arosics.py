from arosics import COREG_LOCAL
from osgeo import gdal
import geoarray
import numpy
import os

bands = ['blue', 'bnir']#, 'coastal', 'evi', 'green', 'ndvi', 'nir', 'red', 'redge1', 'redge2', 'redge3', 'swir1', 'swir2']

img_reference = '/home/marujo/Downloads/arosics_test/2018_12/S2_10_1M_MED_089098_2018-12-01_2018-12-31_{}.tif'
img_target = '/home/marujo/Downloads/arosics_test/2018_11/S2_10_1M_MED_089098_2018-11-01_2018-11-30_{}.tif'
# vrt_ref = '/home/marujo/Downloads/arosics_test/2018_12/ref.vrt'
# vrt_targ = '/home/marujo/Downloads/arosics_test/2018_11/targ.vrt'
vrt_ref = 'ref.vrt' #create vrt on current working dir
vrt_targ = 'ref.vrt' #create vrt on current working dir

shp_output = '/home/marujo/Downloads/arosics_test/output/output_shapefile.shp'

def stack_virtual_raster(image_patter, bands, output):
    band_list = list()
    for band in bands:
        img_path = image_patter.format(band)
        band_list.append(img_path)

    #Set Virtual Raster options
    vrt_options = gdal.BuildVRTOptions(separate='-separate')
    #Create virtual raster
    ds = gdal.BuildVRT(output, band_list, options=vrt_options)
    return ds

### Create Virtual Raster
ds_ref = stack_virtual_raster(img_reference, bands, vrt_ref)
ds_targ = stack_virtual_raster(img_reference, bands, vrt_targ)

### Open Gdal Dataset
ref_array = ds_ref.ReadAsArray()
targ_array = ds_targ.ReadAsArray()

### Load into GeoArray
r_geoArr = geoarray.GeoArray(numpy.transpose(ref_array, (1,2,0))) #transpose due to geoarray using wrong gdal dimensions
t_geoArr = geoarray.GeoArray(numpy.transpose(targ_array, (1,2,0))) #transpose due to geoarray using wrong gdal dimensions

kwargs = {
    # 'grid_res'     : 100,
    # 'window_size'  : (128,128),
    'grid_res'     : 200,
    'window_size'  : (64,64),
    'path_out'     : '/home/marujo/Downloads/arosics_test/output/out.tif',
    'projectDir'   : '/home/marujo/Downloads/arosics_test/output/',
    'q'            : False,
}

CRL = COREG_LOCAL(r_geoArr, t_geoArr, **kwargs)
CRL.correct_shifts()

###Visualize tie point grid with INITIAL shifts present in your input target image
# CRL.view_CoRegPoints(figsize=(15,15), backgroundIm='ref')

###Visualize tie point grid with shifts present AFTER shift correction
# CRL_after_corr = COREG_LOCAL(img_reference, CRL.path_out, **kwargs)
# CRL_after_corr.view_CoRegPoints(figsize=(15,15),backgroundIm='ref')

#export shapefile
CRL.tiepoint_grid.to_PointShapefile(path_out=shp_output)

del ds_ref, ds_targ
print('END')