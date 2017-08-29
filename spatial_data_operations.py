import numpy as np
import numpy.ma as ma

from scipy import interpolate


def create_mask(data_A, lat_A, lon_A, data_B, lat_B, lon_B, condition = lambda x: x==2):
    #create a mask for array B from an array A of different grid
#     1) We regrid data_A to the spatial grid of data_B
#     2) Masking here is based on treshold values: we should define it with lambda function, 
#     eg: x==2 - means mask out all values, where (regridded) data_A is equal 2 
#     eg2: x>1 means that we mask out all values greater than 1, etc
    
    lon_A_1d = np.ndarray.flatten(lon_A)
    lat_A_1d = np.ndarray.flatten(lat_A)
    data_A_1d = np.ndarray.flatten(data_A)

    mask_interpolated = interpolate.griddata((lon_rastr_1d, lat_rastr_1d), data_A_1d, (lon, lat), method='nearest')
    masked_data_B = np.ma.masked_where(condition(mask_interpolated), data_B)
    
    return masked_data_B
