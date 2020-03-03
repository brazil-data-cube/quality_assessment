from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

#folder read
img1 = "/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_06_19/S2A_MSIL2A_20180619T132231_N0206_R038_T23LLF_20180619T150922_255.SAFE/GRANULE/L2A_T23LLF_A015622_20180619T132232/IMG_DATA/R10m"
img2 = "/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_06_19/S2A_MSIL2A_20180619T132231_N9999_R038_T23LLF_20200206T164947_280.SAFE/GRANULE/L2A_T23LLF_A015622_20180619T132232/IMG_DATA/R10m"

#Open dataset
#img1x = gdal.Open(img1)
#img2x = gdal.Open(img2)


#pega o stk de bandas .tif
for filename in os.listdir(img1):
    if filename.endswith('.tif'):
        i1 = filename
        img1x = gdal.Open(os.path.join(img1, filename))


for filename in os.listdir(img2):
    if filename.endswith('.tif'):
        i2 = filename
        img2x = gdal.Open(os.path.join(img2, filename))


#Define path saída
path = '/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_06_19/diff'

#os.chdir(dir) vai para o diretório definido em os.chdir
os.chdir(path)

#deve ser feito um loop pra iterar nas bandas
numbands = img1x.RasterCount

for b in range(numbands):
    ds = img1x
    bandref = np.array(ds.GetRasterBand(b+1).ReadAsArray())
    ds = img2x
    bandtar = np.array(ds.GetRasterBand(b+1).ReadAsArray())
    #Convert np array to float
    bandref = bandref.astype(float)
    bandtar = bandtar.astype(float)
    #set NaN == -9999
    bandref[bandref== -9999]=np.nan
    bandtar[bandtar== -9999]=np.nan
    # A 1-D array, containing the elements of the input, is returned. 
    x = bandref.ravel()
    y = bandtar.ravel()
    #mask in NaN data
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]
    # # desenho da reta, dados 2 pontos extremos
    x_label=None
    y_label=None
    out_file = os.path.basename(i1) + "__" + str(b+1)+ "__" + os.path.basename(i2)
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    r2 = r_value**2

    print("slope:{}".format(slope))
    print("intercept:{}".format(intercept))
    print("r_value:{}".format(r_value))
    print("p_value:{}".format(p_value))
    print("std_error:{}".format(std_err))
    print("r-squared:{}".format(r2))

    #plota histograma 2d
    fig = plt.figure(figsize=(10, 10), facecolor='w')
    ax1 = fig.add_subplot(111)
    textstr = " n={}\n R = {:.4f} \n {} = {:.4f} \n stderr = {:.4f} \n intercept={:.4f}\n slope={:.4f}".format(x.shape[0], r_value, '${R^2}$', r2, std_err, intercept, slope)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.01)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11, verticalalignment='top', bbox=props)
    cmin=0
    cmax=10000
    n_bins=500
    plt.hist2d(x, y, bins=(n_bins, n_bins), cmin=5, range=((cmin, cmax), (cmin, cmax)), cmap='plasma')

    # # desenho da reta, dados 2 pontos extremos
    x2 = np.array([0, 10000])
    plt.plot(x2, x2, color = ('#808080'), ls='dashed', linewidth=1)
    plt.plot(x2, slope * x2 + intercept, '--k', linewidth=1)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.xlabel(os.path.basename(i1) + "_band_"+ str(b+1))
    plt.ylabel(os.path.basename(i2) + "_band_"+ str(b+1))
    plt.colorbar()
    plt.savefig(out_file +'.png', dpi=300, bbox_inches='tight')
    plt.close(fig=None)
