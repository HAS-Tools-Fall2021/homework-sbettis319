# %%
# Import Statements
import pandas as pd
import os
import matplotlib.pyplot as plt
from pandas.io.parsers import read_csv
from shapely import geometry
import xarray as xr
import contextily as ctx
#import rioxarray
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature
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
# Map!
file = os.path.join('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/Average_Annual_Precipitation_-_AZ_(1961_-_1990)-shp/Average_Annual_Precipitation_-_AZ_(1961_-_1990).shp')
fiona.listlayers(file)
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

precip_project = precip.to_crs(epsg=4269)
fig, ax = plt.subplots(figsize=(10, 10))
precip_project.plot(categorical=False,
                legend=True, markersize=45, cmap='OrRd', ax=ax)
ax.set(title = "Arizona annual precip from 1961-1991",
                xlabel = 'latitude', ylabel = 'longitude')
plt.show()
# Adding a point for the location of the stream gauge
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])
point_geom = [Point(xy) for xy in point_list]
point_geom

# Map a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=precip_project.crs)

point_project = point_df.to_crs(epsg=4269)

fig, ax = plt.subplots(figsize=(10, 10))
precip_project.plot(categorical=False,
                legend=True, markersize=45, cmap='OrRd', ax=ax)
point_project.plot(ax=ax, color='black', marker='x', 
        label = 'Stream Gauge - mean flow for last week: 143.9 cfs')
ax.set(title = "Arizona annual precip from 1961-1991 and Stream Gauge",
                xlabel = 'latitude', ylabel = 'longitude')
ax.legend()
plt.show()

# %%
# Other map that does not work
# Watershed Boundary
# Example reading in a geodataframe
file = os.path.join('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/Shape')
fiona.listlayers(file)
HU4 = gpd.read_file(file, layer="WBDHU4")

HU4.crs
# %%
# NCEP Reanalysis data --> precip
data = ('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/X107.2.20.129.315.18.5.30.nc')
dataset = xr.open_dataset(data)
dataset
# We can inspect the metadata of the file like this:
metadata = dataset.attrs
metadata
# And we can grab out any part of it like this:
metadata['dataset_title']

# We can also look at other  attributes like this
dataset.values
dataset.dims
dataset.coords

# Focusing on just the precip values
precip = dataset['prate']
precip

# Now to grab out data first lets look at spatail coordinates
dataset['prate']['lat'].values.shape
# The first 4 lat values
dataset['prate']['lat'].values
dataset['prate']['lon'].values

# Now looking at the time
dataset["prate"]["time"].values
dataset["prate"]["time"].values.shape


# Now lets take a slice: Grabbing data for just one point
lat = dataset["prate"]["lat"].values[0]
lon = dataset["prate"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_point = dataset["prate"].sel(lat=lat,lon=lon)
one_point.shape

# Use x-array to plot timeseries
one_point.plot.line()
precip_val = one_point.values

# Convert to dataframe
one_point_df = one_point.to_dataframe()

# Dataframe to geodataframe
gdf_precip = gpd.GeoDataFrame(one_point_df.resample('Y').mean)
fig, ax = plt.subplots(figsize=(10, 10))
gdf_precip.plot(ax=ax)
ax.set_title("Precip")
plt.show()

## I need to get the geometry somehow
precip_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HU4.crs)

# %%
# Adding a point for the location of the stream gauge
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])
# Make these into spatial features
point_geom = [Point(xy) for xy in point_list]

# Map a dataframe of these points
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HU4.crs)
# %%
# Combining HU4 and points
HU4_project = HU4.to_crs(HU4.crs)
point_project = point_df.to_crs(HU4.crs)
# Now plot again
fig, ax = plt.subplots(figsize=(5, 5))
HU4.plot(categorical=False,
              legend=True, markersize=15, cmap='Set1',
              ax=ax)
point_project.plot(ax=ax, color='black', marker='o')
HU4_project.boundary.plot(ax=ax, color=None,
                           edgecolor='blue', linewidth=0.5)
ax.set(title ='Watershed Boundaries and Stream Gauge', xlabel ='latitude',
                ylabel ='longitude')

# %%
# Converting the previous map to lat and longitude by projecting
# everything to the HU4 crs
precip_project = HU4_project.to_crs(HU4.crs)
fig, ax = plt.subplots(figsize=(10, 10))
gdf_precip.plot(categorical=False,
              legend=True, color='black', marker='x', ax=ax)
point_project.plot(ax=ax, color='black', marker='o',
                    label ="Verde River at Camp Verde")
HU4.boundary.plot(ax=ax, color=None,
                edgecolor='blue',linewidth=0.5,
                label="AZ Watershed boundary")
ctx.add_basemap(ax, crs=HU4.crs)
ax.set(title ='Annual Precip, Watershed Boundaries, and Stream Gauge',
                xlabel ='latitude', ylabel ='longitude')
ax.legend()
#fig.savefig("Sub-basin AZ")
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
        # If there is no forecasted precip, use this chunk (lines 119 to 127):
        #week_flow = data1_i['flow'][('2021-' + str(month1) + '-' + str(day_start)):('2021-' + str(month2) + '-' + str(day_end))]
        #forecast_mean = np.mean(week_flow)

        #week_min = np.min(week_flow)
        #week_max = np.max(week_flow)
        #difference = week_max - week_min
        #forecast_wk2 = week_max - difference
        #prediction = print("The forecast for week 1 is:", forecast_mean, \
        #        "and the forecast for week 2 is:", forecast_wk2)

        # If there is forecasted precip, use this chunk (lines 130 to 138):
        week_flow1 = data1[(data1['year'] == 2021) & (data1['month'] == 11) & (data1['day'] >= day_start) & (data1['day'] <= day_end)]
        forecast_mean = np.mean(week_flow1['flow'])

        precip_to_flow = precip_chance * 14 
        forecast1 = forecast_mean + precip_to_flow 
        forecast2 = forecast_mean - precip_to_flow 

        prediction = print("The forecast for week 1 is:", forecast1, "cfs", \
                "and the week 2 forecast is", forecast2, "cfs")

        return(prediction)

precip_fore = np.sum(precip_df['precip']) / 25.4
forecasts(11, 11, 7, 13, precip_fore)  # precip_fore is the amount of precipitation that is forecasted in inches

# %%
