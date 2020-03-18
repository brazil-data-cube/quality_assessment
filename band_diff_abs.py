#import libraries
from osgeo import gdal
import numpy as np
import os
import time
import matplotlib.pyplot as plt

#define início de contador tempo
tstart = time.time()

img1 = '/home/fronza/Fronza_BDC/2_SEN2COR_2_8_ancillary_data_test/LC8_DN/220069'
img2 = '/home/fronza/Fronza_BDC/2_SEN2COR_2_8_ancillary_data_test/LC8_DN/220069'


#cria listas vazias
listbands1 = list()
listbands2 = list()

for filename1 in os.listdir(img1):
    if filename1.endswith(('B1.TIF', 'B2.TIF', 'B3.TIF')):
        listbands1.append(os.path.join(filename1))

for filename2 in os.listdir(img2):
    if filename2.endswith(('B4.TIF', 'B5.TIF', 'B6.TIF')):
        listbands2.append(os.path.join(filename2))


#for filename1 in os.listdir(img1):
#    if filename1.endswith(('_B02_10m.jp2', '_B03_10m.jp2', '_B04_10m.jp2')):
#        listbands1.append(os.path.join(filename1))

#for filename2 in os.listdir(img2):
#    if filename2.endswith(('_B02_10m.jp2', '_B03_10m.jp2', '_B04_10m.jp2')):
#        listbands2.append(os.path.join(filename2))

listbands1 = sorted(listbands1)
listbands2 = sorted(listbands2)

print(*listbands1, sep = "\n")
print("nova lista")
print(*listbands2, sep = "\n") 

 # Create GTIF file
driver = gdal.GetDriverByName("GTiff")

#output_file = img1.split("/")[-3] + "__DIF__" + img2.split("/")[-3] + ".tif"
output_file = listbands1[0][:40] + "__DIF.tif"
#ref t1 banda 1
ref = gdal.Open(os.path.join(img1, filename1))

#usa a referencia
xsize = ref.RasterXSize
print(xsize)
ysize = ref.RasterYSize
print(ysize)

numbands = len(listbands1)
dataset = driver.Create(output_file, xsize, ysize, numbands, gdal.GDT_Float32)

print(numbands)

# follow code is adding GeoTranform and Projection
geotrans=ref.GetGeoTransform()  #get GeoTranform from existed 'data0'
proj=ref.GetProjection() #you can get from a exsited tif or import 
dataset.SetGeoTransform(geotrans)
dataset.SetProjection(proj)
print(listbands1[0][:40])
#for t1 and t2 abs diff
for filename in range(len(listbands1)):
    ds1 = gdal.Open(os.path.join(img1, listbands1[filename]))
    xsize = ds1.RasterXSize
    ysize = ds1.RasterYSize
    bandref = np.array(ds1.GetRasterBand(1).ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize))
    ds2 = gdal.Open(os.path.join(img2, listbands2[filename]))
    bandtar = np.array(ds2.GetRasterBand(1).ReadAsArray(xoff=0, yoff=0, win_xsize=xsize, win_ysize=ysize))
    bandref = bandref.astype(float)
    bandtar = bandtar.astype(float)
    bandref[bandref== -9999]=np.nan
    bandtar[bandtar== -9999]=np.nan
    #print(bandref.size)
    #print(bandtar.size)
    band_diff = np.abs(bandref - bandtar)
    #diff = ds1 - ds2
    dataset.GetRasterBand(filename+1).WriteArray(band_diff)
    #setting nodata value
    dataset.GetRasterBand(1).SetNoDataValue(-9999)

dataset.FlushCache()
dataset=None
ref.FlushCache()
ref = None   