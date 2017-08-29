import numpy as np
import numpy.ma as ma
import gdal

def readFile(filename, nbofbands=1, nth_point=10):
    filehandle = gdal.Open(filename)
    if filehandle is None:
      print ('Unable to open ', filename)
      sys.exit(1)
    
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    print (geotransform)

    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    
    band_data=np.zeros((ysize, xsize, filehandle.RasterCount), dtype=np.float64)
    
    print ("[ RASTER BAND COUNT ]: ", filehandle.RasterCount)
    for band in range(filehandle.RasterCount):
      band +=1
      print ("[ GETTING BAND ]: ", band)
      scrband = filehandle.GetRasterBand(band)

      if scrband is None:
        continue
      band_data[::nth_point, ::nth_point, band-1] = scrband.ReadAsArray()

    return xsize,ysize, geotransform, geoproj, band_data
    
    
def get_latlon(band_data, geotransform, nth_point=10):
    # "I'm making the assumption that the image isn't rotated/skewed/etc. 
    # This is not the correct method in general, but let's ignore that for now
    # If dxdy or dydx aren't 0, then this will be incorrect"
    
    # geotransform is a gdal way of describing the data grid, see http://www.gdal.org/gdal_tutorial.html
    # nth_point is needed to artificially decrease high spatial resolution of 40-m Sentinel-1 images 
    # eg: 40*10th point => resolution of ~400 m
   
    Xpixel, Yline = np.meshgrid(np.arange(0, band_data.shape[1], nth_point), 
                                np.arange(1, band_data.shape[0], nth_point))
    lon_rastr = geotransform[0] + Xpixel*geotransform[1] + Yline*geotransform[2]
    lat_rastr = geotransform[3] + Xpixel*geotransform[4] + Yline*geotransform[5]
    return lon_rastr, lat_rastr
    
    
    
