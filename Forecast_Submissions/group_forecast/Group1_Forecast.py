# %%
# Import Statements
import pandas as pd
import os
import matplotlib.pyplot as plt
from pandas.io.parsers import read_csv
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
url_1 = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=09506000&referred_module=sw&period=&begin_date=1990-01-01&end_date=2021-11-13"
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
# Map
file = os.path.join('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/Average_Annual_Precipitation_-_AZ_(1961_-_1990)-shp/Average_Annual_Precipitation_-_AZ_(1961_-_1990).shp')
precip = gpd.read_file(file)

type(precip)
precip.head
precip.columns

# Can see the geometry type of each row like this:
precip.geom_type
# can see the projection here
precip.crs
# And the total spatial extent like this:
precip.total_bounds

fig, ax = plt.subplots(figsize=(10, 10))
precip.plot(categorical=False,
                legend=True, markersize=45, cmap='OrRd', ax=ax)
ax.set_title("Arizona annual precip from 1961-1991")
plt.show()
# %%
# Graph: Time series of next two weeks' accumulated precipitation
# Grab the data
# Remember to change start_date to '20211111'
# Move all the import lines to the top later
import urllib.request as req
import pygrib as pg
import numpy as np
import pandas as pd
from datetime import datetime

start_date = '20211109'
base_url = "https://www.ncei.noaa.gov/data/global-forecast-system/access/grid-003-1.0-degree/forecast/202111/"+start_date+"/"

precip = np.zeros(112)

for i in range(51, 385, 3):
        if i < 10:
                filename = "gfs_3_" + start_date + "_0000_00" + str(i) + ".grb2"
        elif i < 100:
                filename = "gfs_3_" + start_date + "_0000_0" + str(i) + ".grb2"
        else:
                filename = "gfs_3_" + start_date + "_0000_" + str(i) + ".grb2"
        req.urlretrieve(base_url+filename, 'C:\\Users\\certain\\Desktop\\temp.grb2')
        dataset = pg.open('C:\\Users\\certain\\Desktop\\temp.grb2')
        if str(dataset[596])[0:32] == '596:Total Precipitation:kg m**-2':
                precip[int(i/3-1)] = dataset[596].values[34, 248]

date_time = pd.date_range(start='2021-11-14 3:00', periods=112, freq='3H')
precip_df = pd.DataFrame({'date_time': date_time, 'precip': precip})

precip_df.to_csv('precip.csv')
# please make sure to push this new csv :) 

# %%
# Get the graph
import matplotlib.pyplot as plt
precip_df = pd.read_table('precip.csv', skiprows=1,
                          sep=',', names=['id', 'date_time', 'precip'],
                          parse_dates=['date_time'])
precip_df = precip_df.set_index(["date_time"])
fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
precip_df.plot(y='precip', ax=ax)
ax.set(xlabel='Datetime',
       ylabel='3-hour Accumulated Precipitation',
       title='Forecast Precipitation from Nov 14, 2021 to Nov 27 (kg/m\u00b2)')
fig.savefig("Group1_Graph.png")

# %%
# Forecast Function
# hi xiang if you get to this, just keep the parameters and doc string included, even if some of the values aren't technically used, just so we have it :)
# also i updated this to have the correct dates (nov 7 - nov 13) so if you try to run it today on saturday, it won't work 
# also part 2 haha i updated the stream flow data in the second cell above to have saturday included so that won't work right now either (saturday) but it will work sunday :)
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
        # If there is no forecasted precip, use this chunk (lines 119 to 127). If there IS forecasted precip, COMMENT THIS WHOLE SECTION OUT
        week_flow = data1_i['flow'][('2021-' + str(month1) + '-' + str(day_start)):('2021-' + str(month2) + '-' + str(day_end))]
        forecast_mean = np.mean(week_flow)

        week_min = np.min(week_flow)
        week_max = np.max(week_flow)
        difference = week_max - week_min
        forecast_wk2 = week_max - difference
        prediction = print("The forecast for week 1 is:", forecast_mean, \
                "and the forecast for week 2 is:", forecast_wk2)

        # If there is forecasted precip, use this chunk (lines 130 to 138). If there ISN'T forecasted precip, COMMENT THIS OUT :)) 
        week_flow1 = data1[(data1['year'] == 2021) & (data1['month'] == 11) & (data1['day'] >= day_start) & (data1['day'] <= day_end)]
        forecast_mean = np.mean(week_flow1['flow'])

        precip_to_flow = precip_chance * 14 
        forecast1 = forecast_mean + precip_to_flow 
        forecast2 = forecast_mean - precip_to_flow 

        prediction = print("The forecast for week 1 is:", forecast1, "cfs", \
                "and the week 2 forecast is", forecast2, "cfs")

        return(prediction)


forecasts(11, 11, 7, 13, 0) #this zero should be the amount of precipitation that is forecasted in INCHES :) 