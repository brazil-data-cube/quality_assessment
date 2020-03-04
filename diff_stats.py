import gdal
import os
from rasterio.plot import show
import numpy as np

pathdiff = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/diff'

#inicializa variavel
diff = None

#pega a imagem de diferença na pasta
for filename in os.listdir(pathdiff):
    if '_DIF_' in filename:
        diffname = filename
        diffimg = gdal.Open(os.path.join(pathdiff, filename))

bands = diffimg.RasterCount

#median(a[, axis, out, overwrite_input, keepdims])	Compute the median along the specified axis.
#average(a[, axis, weights, returned])	Compute the weighted average along the specified axis.
#mean(a[, axis, dtype, out, keepdims])	Compute the arithmetic mean along the specified axis.
#std(a[, axis, dtype, out, ddof, keepdims])	Compute the standard deviation along the specified axis.
#var(a[, axis, dtype, out, ddof, keepdims])	Compute the variance along the specified axis.
#nanmedian(a[, axis, out, overwrite_input, …])	Compute the median along the specified axis, while ignoring NaNs.
#nanmean(a[, axis, dtype, out, keepdims])	Compute the arithmetic mean along the specified axis, ignoring NaNs.
#nanstd(a[, axis, dtype, out, ddof, keepdims])	Compute the standard deviation along the specified axis, while ignoring NaNs.
#nanvar(a[, axis, dtype, out, ddof, keepdims])	Compute the variance along the specified axis, while ignoring NaNs.

for b in range(1, bands+1):
    data = diffimg.GetRasterBand(b).ReadAsArray().astype('float')
    mean = np.mean(data) #calculate mean 
    median = np.median(data) #calculate median without value 0
    std = np.std(data) #calculate std without value 0
    var = np.var(data) #calculate var without value 0
    #histogram(a[, bins, range, normed, weights, …])	Compute the histogram of a set of data.
    print("[ STATS DIFF] =  Band=%.1d, Mean=%.3f, Median=%.3f, StdDev=%.3f, Variance=%.3f" % ((b), mean, median, std, var))


print(diffname)
#rb = ds1.GetRasterBand(1)
#img_array = rb.ReadAsArray()
#show(img_array)

#diffimg
