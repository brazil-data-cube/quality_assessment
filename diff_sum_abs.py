import gdal
import os
import numpy as np

img1 = 'X:/BDC/Dados/LC8_DN/220069/'
img2 = 'X:/BDC/Dados/LC8_DN/220069/'

#cria listas vazias
listbands1 = list()
listbands2 = list()

for filename1 in os.listdir(img1):
    if filename1.endswith(('B1.TIF', 'B2.TIF', 'B3.TIF')):
        listbands1.append(os.path.join(filename1))

for filename2 in os.listdir(img2):
    if filename2.endswith(('B4.TIF', 'B5.TIF', 'B6.TIF')):
        listbands2.append(os.path.join(filename2))
print(listbands1)
print(listbands2)
 # Create GTIF file
driver = gdal.GetDriverByName("GTiff")

#conta numero de bandas
numbands = len(listbands1)

#define nome do output
output_file = listbands1[0][:40] + "__DIF.tif"
print(output_file)

#ref t1 banda 1
ref = gdal.Open(os.path.join(img1, filename1))

#usa a referencia para obter xsize e ysize
xsize = ref.RasterXSize
ysize = ref.RasterYSize

#cria a imagem de saída
dataset = driver.Create(output_file, xsize, ysize, 1, gdal.GDT_Float32)

# follow code is adding GeoTranform and Projection
geotrans=ref.GetGeoTransform()  #get GeoTranform from existed 'data0'
proj=ref.GetProjection() #you can get from a exsited tif or import 
dataset.SetGeoTransform(geotrans)
dataset.SetProjection(proj)

#cria lista vazia para receber os dados
results = []

for band in range(len(listbands1)):
    ds1 = gdal.Open(os.path.join(img1, listbands1[band]))
    ds2 = gdal.Open(os.path.join(img2, listbands2[band]))
    bandtar = np.array(ds1.GetRasterBand(1).ReadAsArray().astype(float))
    bandref = np.array(ds2.GetRasterBand(1).ReadAsArray().astype(float))
    results.append(np.abs(bandtar - bandref))
    diff_abs_sum = np.sum(results, axis=0)
    dataset.GetRasterBand(1).WriteArray(diff_abs_sum)

ds1 = None
ds2 = None
bandref = None
bandtar = None
ref = None
dataset=None
