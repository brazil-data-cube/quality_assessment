#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import os
import time
# 3rdparty
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def compare_linregress(image_path1,image_path2, out_path):
    #pega o stk de bandas .tif img1
    for filename in os.listdir(image_path1):
        if filename.endswith('.tif'):
            i1 = filename
            ds1 = gdal.Open(os.path.join(image_path1, filename))

    #pega o stk de bandas .tif img2
    for filename in os.listdir(image_path2):
        if filename.endswith('.tif'):
            i2 = filename
            ds2 = gdal.Open(os.path.join(image_path2, filename))

    #os.chdir(dir) vai para o diretório definido em os.chdir
    os.chdir(out_path)

    #deve ser feito um loop pra iterar nas bandas
    numbands = ds1.RasterCount

    for b in range(numbands):
        bandref = np.array(ds1.GetRasterBand(b+1).ReadAsArray())
        bandtar = np.array(ds2.GetRasterBand(b+1).ReadAsArray())
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

if __name__ == '__main__':
    #image paths
    #TODO use lib sys to obtain parameters from command line

    #folder read
    image_path1 = "/home/fronza/Fronza_BDC/2_SEN2CORR_2_8_ancillary_data_test/2018_01_10/S2A_aux_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200311T190031.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m"
    image_path2 = "/home/fronza/Fronza_BDC/2_SEN2CORR_2_8_ancillary_data_test/2018_01_10/S2A_s_aux_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200311T193142.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m"
    #Define path saída
    out_path = '/home/fronza/Fronza_BDC/2_SEN2CORR_2_8_ancillary_data_test/2018_01_10/output'
    
    print('STARTED compare_linregress')
    start = time.time()

    compare_linregress(image_path1,image_path2, out_path)

    ds1=None
    ds2=None
    x=None
    y=None

    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
   