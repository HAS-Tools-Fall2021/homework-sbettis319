# %%
# Import Statements
import pandas as pd
import os
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
import numpy as np
from shapely.geometry import Point
from netCDF4 import Dataset

# %%
# Import Stream Gage Data (Camp Verde)
# CHANGE THE DATE AT THE END OF THE WEEK
url_1 = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=09506000&referred_module=sw&period=&begin_date=1990-01-01&end_date=2021-11-6"
data1 = pd.read_table(url_1, skiprows=30, names=['agency_cd', 'site_no',
                                               'datetime', 'flow', 'code'],
                                               parse_dates =['datetime'])

data1['year'] = pd.DatetimeIndex(data1['datetime']).year
data1['month'] = pd.DatetimeIndex(data1['datetime']).month
data1['day'] = pd.DatetimeIndex(data1['datetime']).day
data1['dayofweek'] = pd.DatetimeIndex(data1['datetime']).dayofweek

data1_i = data1.copy()
data1_i = data1_i.set_index('datetime')

# %%
# Map?? --> annual precip

# %%
# Graph?? 

# %%
# Forecast Function
# CHANGE THE DATE TO 11/7/21 and 11/13/21 ON SUNDAY!!! SO IT'S UPDATED :) 
def forecasts(month1, month2, day_start, day_end, precip_chance):
        '''
        This function determines the week 1 and week 2 forecast predictions based on the forecasted precip in Camp Verde

        Parameters:
        "month1" represents the month of November (int)
        "month2" represents November (int)
        "day_start" represents this past Sunday, the 7th. (int)
        "day_end" represents Saturday, the 13th. (int)
        "precip_chance" represents the total forecasted amount of precipitation in inches (int)

        Outputs:
        This function returns a print statement that provides the forecasted flows for week 1 and week 2. 
        '''
        # If there is no forecasted precip:
        week_flow = data1_i['flow'][('2021-' + str(month1) + '-' + str(day_start)):('2021-' + str(month2) + '-' + str(day_end))]
        forecast_mean = np.mean(week_flow)

        week_min = np.min(week_flow)
        week_max = np.max(week_flow)
        difference = week_max - week_min
        forecast_wk2 = week_max - difference
        prediction = print("The forecast for week 1 is:", forecast_mean, \
                "and the forecast for week 2 is:", forecast_wk2)

        # If there is forecasted precip:
        week_flow1 = data1[(data1['year'] == 2021) & (data1['month'] == 11) & (data1['day'] >= day_start) & (data1['day'] <= day_end)]
        forecast_mean = np.mean(week_flow1['flow'])

        precip_to_flow = precip_chance * 14 
        forecast1 = forecast_mean + precip_to_flow 
        forecast2 = forecast_mean - precip_to_flow 

        prediction2 = print("The forecast for week 1 is:", forecast1, "cfs", \
                "and the week 2 forecast is", forecast2, "cfs")

        return(prediction, prediction2)


forecasts(10, 11, 31, 6, 0)