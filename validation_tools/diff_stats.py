#
# This file is part of Brazil Data Cube Validation Tools.
# Copyright (C) 2020 INPE.
#
# Python Native
import os
import time
import sys
# 3rdparty
import gdal
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np

def diff_bands_stats(input_folder, output_folder):
    '''
    documentar para sair automaticamente
    '''
    #inicializa variavel

    #pega a imagem de diferença na pasta
    for filename in os.listdir(input_folder):
        if '_DIF_' in filename:
            diffname = filename
            diffimg = gdal.Open(os.path.join(input_folder, filename))

    #os.chdir(dir) vai para o diretório definido em os.chdir
    os.chdir(output_folder)

    #conta bandas
    bands = diffimg.RasterCount
    
    #Define label x e y
    x_label=None
    y_label=None
      
    #compute histogram to each band
    for b in range(1, bands+1):
        data = diffimg.GetRasterBand(b).ReadAsArray()
        dmin = np.min(data) #min value
        dmax = np.max(data) #max value
        mean = np.mean(data) #calculate mean 
        median = np.median(data) #calculate median without value 0
        std = np.std(data) #calculate std without value 0
        var = np.var(data) #calculate var without value 0
        histog = np.hstack(data)	#Compute the histogram of a set of data.
        #define histogram intervals
        a = [-2000, -1000, -500, 0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000]
        print("[ STATS DIFF] =  Band=%.1d, Min=%.3f, Max=%.3f, Mean=%.3f, Median=%.3f, StdDev=%.3f, Variance=%.3f" % ((b), dmin, dmax, mean, median, std, var))
        #create fig    
        fig = plt.figure(figsize=(10, 10), facecolor='w')
        #create subplot to histogram stats
        ax1 = fig.add_subplot(111)
        #plot text in subplot
        textstr = "Band={}\n Dmin={:.4f} \n Dmax={:.4f} \n Mean= {:.4f} \n Median={:.4f}\n Std={:.4f} \n Variance={:.4f} \n".format(b, dmin, dmax, mean, median,std,var)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.01)
        #subplot dimensions
        ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11, verticalalignment='top', bbox=props)
        #plot histogram
        plt.hist(histog, bins=a)
        #define label e fonte de label
        plt.xlabel(x_label, fontsize=14)
        plt.ylabel(y_label, fontsize=14)
        #define label dos eixos x e y
        plt.xlabel("band_" + str(b))
        plt.ylabel("band_" + str(b))
        #plt.colorbar()
        print(os.path.basename(filename))
        out_file = os.path.basename(filename) + "_band_" + str(b)
        plt.savefig(out_file +'.png', dpi=300, bbox_inches='tight')
        plt.close(fig=None)

if __name__ == '__main__':

    if len(sys.argv) <= 2: # aqui fazes a verificacao sobre quantos args queres receber, o nome do programa conta como 1
        print('Argumentos insuficientes para rodar a função')
        sys.exit()
    print('STARTED diff_bands_stats')
    start = time.time()
    input_folder, output_folder = sys.argv[1], sys.argv[2]

    diff_bands_stats(input_folder, output_folder)
    end = time.time()
    print('ENDED')
    print('TOTAL ELAPSED TIME: {}'.format(end-start))
