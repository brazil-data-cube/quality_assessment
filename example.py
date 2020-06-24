# Python Native
import time
# 3rdparty
from validationtools import raster_comparison
from osgeo import gdal


print("START")
start = time.time()

###INPUTS
path1 = '/path/to/image1'
path2 = '/path/to/image2'
###RESULTS
path_result_intersect1 = '/path/to/intersect1.tif'
path_result_intersect2 = '/path/to/intersect2.tif'
path_abs_diff = '/path/to/abs_diff.tif'

ds1 = gdal.Open(path1)
ds2 = gdal.Open(path2)

raster_comparison.raster_intersection(ds1, ds2, output_name1=path_result_intersect1, output_name2=path_result_intersect2)
raster_comparison.raster_absolute_diff(ds1, ds2, output_file=path_abs_diff)

end = time.time()
print("Duration time: {}".format(end - start))
print("END")
