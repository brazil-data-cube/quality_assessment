import gdal
import numpy as np
import matplotlib.pyplot as plt
import os

imagePath1 = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/S2A_MSIL2A_20180110T132221_N0206_R038_T23LLF_20191216T040849_255.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
imagePath2 = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/S2A_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200206T173655_280.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'

ds1x = imagePath1
ds2x = imagePath2

#carrega o dataset
#ds1x = '/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_06_19/S2A_MSIL2A_20180619T132231_N0206_R038_T23LLF_20180619T150922_255.SAFE/GRANULE/L2A_T23LLF_A015622_20180619T132232/IMG_DATA/R10m'
#ds2x = '/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_06_19/S2A_MSIL2A_20180619T132231_N9999_R038_T23LLF_20200206T164947_280.SAFE/GRANULE/L2A_T23LLF_A015622_20180619T132232/IMG_DATA/R10m'
output_folder = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/diff'

#pega o stk de bandas .tif
for filename in os.listdir(ds1x):
    if filename.endswith('.tif'):
        i1 = filename
        ds1 = gdal.Open(os.path.join(ds1x, filename))

for filename in os.listdir(ds2x):
    if filename.endswith('.tif'):
        i2 = filename
        ds2 = gdal.Open(os.path.join(ds2x, filename))

#gdal.Open no dataset
#ds1 = gdal.Open("/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_01_10/S2A_MSIL2A_20180110T132221_N0206_R038_T23LLF_20191216T040849_255.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m/T23LLF_20180110T132221_255.tif")
#ds2 = gdal.Open("/home/fronza/Fronza_BDC/1_SEN2CORR_TESTE1/2018_01_10/S2A_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200206T173655_280.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m/T23LLF_20180110T132221_280.tif")

#define o range de bandas da comparação
numbands = ds1.RasterCount

#lógica do loop
#for j in range(bands_a):
#       band = a.GetRasterBand(j+1)
#       stats = band.GetStatistics( True, True )
#       print("[ STATS 255] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( stats[0], stats[1], stats[2], stats[3] ))

#define o driver
driver = gdal.GetDriverByName("GTiff")

#cria o nome do arquivo de saída
output_file = os.path.basename(i1) + "_DIF_" + os.path.basename(i2)
print(output_file)
os.chdir(output_folder)
print("CURRENTDIR:" + os.getcwd())

#dimensoes do raster
xsize = ds1.RasterXSize
ysize = ds1.RasterYSize

#cria o dataset vazio com as bandas da diferença
dataset = driver.Create(output_file, xsize, ysize, numbands, gdal.GDT_Float32)

# follow code is adding GeoTranform and Projection
geotrans=ds1.GetGeoTransform()  #get GeoTranform from existed 'data0'
proj=ds1.GetProjection() #you can get from a exsited tif or import 
dataset.SetGeoTransform(geotrans)
dataset.SetProjection(proj)

#setting nodata value
dataset.GetRasterBand(1).SetNoDataValue(-9999)

#loop da diferença para gerar as bandas
for b in range(numbands):
    #variáveis para gerar as estatísticas de ds1 e ds2
    band_ax = ds1.GetRasterBand(b+1)
    band_bx = ds2.GetRasterBand(b+1)
    #constroi o numpy array para fazer a diferença nas bandas
    band_a = ds1.GetRasterBand(b+1).ReadAsArray()
    band_b = ds2.GetRasterBand(b+1).ReadAsArray()
    #transforma para float
    band_a = band_a.astype(float)
    band_b = band_b.astype(float)
    #define -9999 para nan 
    band_a[band_a== -9999]=np.nan
    band_b[band_b== -9999]=np.nan
    #calcula a diferença para a banda
    band_diff = band_a - band_b
    #escreve a diferença no array
    dataset.GetRasterBand(b+1).WriteArray(band_diff)
    #obtem as estatísticas do dataset1 e dataset2
    stats_a = band_ax.GetStatistics(True, True)
    stats_b = band_bx.GetStatistics(True, True)
    #printa as estatísticas das bandas do dataset1 e dataset 2
    print("[ STATS 255] =  Band=%.1d, Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ((b+1), stats_a[0], stats_a[1], stats_a[2], stats_a[3] ))
    print("[ STATS 280] =  Band=%.1d, Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ((b+1), stats_b[0], stats_b[1], stats_b[2], stats_b[3] ))
    #plt.imshow(band_diff)
    #plt.show()
    # output_file = os.path.basename(ds2) + "__X__" + os.path.basename(ds2)
    # str(b+1) + "__" + adiciona o numero da banda na saída


#limpa a variável dataset
dataset.FlushCache()
dataset=None
ds1=None
ds2=None
