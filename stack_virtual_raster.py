import os
import rasterio
import time
import gdal

#define os paths de imagens
imagePath1 = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/S2A_MSIL2A_20180110T132221_N0206_R038_T23LLF_20191216T040849_255.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
imagePath2 = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/S2A_MSIL2A_20180110T132221_N9999_R038_T23LLF_20200206T173655_280.SAFE/GRANULE/L2A_T23LLF_A013334_20180110T132224/IMG_DATA/R10m'
output_folder = '/home/fronza/Fronza_BDC/1_SEN2CORR_V_TESTE/2018_01_10/diff'

#inicio processamento imagem sen2corr 2.5.5
os.chdir(imagePath1)

print("STARTED")
start = time.time()

#cria uma lista vazia
li_bands1 = list()
#procura as bandas blue, green, red, nir do sentinel 2 e coloca na lista
for filename in os.listdir(imagePath1):
    if filename.endswith("_B02_10m.jp2"):
        li_bands1.append(os.path.join(filename))

for filename in os.listdir(imagePath1):
    if filename.endswith("_B03_10m.jp2"):
        li_bands1.append(os.path.join(filename))
            
for filename in os.listdir(imagePath1):
    if filename.endswith("_B04_10m.jp2"):
       li_bands1.append(os.path.join(filename))

for filename in os.listdir(imagePath1):
    if filename.endswith("_B08_10m.jp2"):
        li_bands1.append(os.path.join(filename))
print(li_bands1)
#define as opções do virtual Raster
vrt_options = gdal.BuildVRTOptions(separate='-separate')
#cria o virtual raster
ds1 = gdal.BuildVRT('img1.vrt', li_bands1, options=vrt_options)
#define nome do tif de saída
output_filename1 = imagePath1.split("/")[-3] + '_stk.tif'  
#cria o tif de saída
gdal.Translate(output_filename1, ds1, format='GTiff')

#inicio processamento imagem sen2corr 2.8.0
os.chdir(imagePath2)

#cria uma lista vazia
li_bands2 = list()
#procura as bandas blue, green, red, nir do sentinel 2 e coloca na lista
for filename in os.listdir(imagePath2):
    if filename.endswith("_B02_10m.jp2"):
        li_bands2.append(os.path.join(filename))

for filename in os.listdir(imagePath2):
    if filename.endswith("_B03_10m.jp2"):
        li_bands2.append(os.path.join(filename))
            
for filename in os.listdir(imagePath2):
    if filename.endswith("_B04_10m.jp2"):
       li_bands2.append(os.path.join(filename))

for filename in os.listdir(imagePath2):
    if filename.endswith("_B08_10m.jp2"):
        li_bands2.append(os.path.join(filename))

#define as opções do virtual Raster
vrt_options = gdal.BuildVRTOptions(separate='-separate')
#cria o virtual raster
ds2 = gdal.BuildVRT('img2.vrt', li_bands2, options=vrt_options)
#define nome do tif de saída
output_filename2 = imagePath2.split("/")[-3] + '_stk.tif'  
#cria o tif de saída
#os.chdir(output_folder)
gdal.Translate(output_filename2, ds2, format='Gtiff')

end = time.time()
print("ENDED")
print("TOTAL ELAPSED TIME:", (end - start) )