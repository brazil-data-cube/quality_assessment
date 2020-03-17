#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import os
import time
import sys
# 3rdparty
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def compare_linregress(image_path1,image_path2, output_folder):
    #pega o stk de bandas .tif img1
    for filename in os.listdir(image_path1):
        if filename.endswith('.tif'):
            i1 = filename
            print(i1)
            ds1 = gdal.Open(os.path.join(image_path1, filename))

    #pega o stk de bandas .tif img2
    for filename in os.listdir(image_path2):
        if filename.endswith('.tif'):
            i2 = filename
            print(i2)
            ds2 = gdal.Open(os.path.join(image_path2, filename))

    #os.chdir(dir) vai para o diretório definido em os.chdir
    os.chdir(output_folder)

    #deve ser feito um loop pra iterar nas bandas
    numbands = ds1.RasterCount
    print(numbands)

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

    if len(sys.argv) <= 3: # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED compare_linregress')
    start = time.time()
    image_path1, image_path2, output_folder = sys.argv[1], sys.argv[2], sys.argv[3]
    compare_linregress(image_path1,image_path2, output_folder)
    ds1=None
    ds2=None
    x=None
    y=None
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
