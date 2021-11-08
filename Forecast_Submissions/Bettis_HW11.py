# This script assumes you have already downloaded several netcdf files
# see the assignment instructions for how to do this
# %%
import pandas as pd
import matplotlib.pyplot as plt
# netcdf4 needs to be installed in your environment for this to work
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import fiona
import shapely
from netCDF4 import Dataset

# NOTE To install the packages you need you should use the following line:
# conda install rioxarray dask netCDF4 bottleneck
# %%
# Net CDF file historical time series
# Specific Humidity
data_path1 = os.path.join('/Users/sierra/Desktop/Desktop - Sierra’s MacBook Pro/Fall 2021/HASTools/homework-sbettis319/data/specific_humidity.nc')

# Read in the dataset as an x-array
dataset = xr.open_dataset(data_path1)
# Look at it
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
precip = dataset['shum']
precip

# Now to grab out data first lets look at spatail coordinates:
dataset['shum']['lat'].values.shape
# The first 4 lat values
dataset['shum']['lat'].values
dataset['shum']['lon'].values

# Now looking at the time;
dataset["shum"]["time"].values
dataset["shum"]["time"].values.shape


# Now lets take a slice: Grabbing data for just one point
lat = dataset["shum"]["lat"].values[0]
lon = dataset["shum"]["lon"].values[0]
print("Long, Lat values:", lon, lat)
one_point = dataset["shum"].sel(lat=lat,lon=lon)
one_point.shape

# Use x-array to plot timeseries
one_point.plot.line()
precip_val = one_point.values

# Make a nicer timeseries plot
f, ax = plt.subplots(figsize=(12, 6))
one_point.plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="grey",
                    markerfacecolor="magenta",
                    markeredgecolor="gray")
ax.set(title="Time Series for a latitude of 32 and a longitude of 264")

# Convert to dataframe
one_point_df = one_point.to_dataframe()

# %%
# Making a spatial map of one point in time (histogram)
start_date = "2000-01-01"
end_date = "2021-11-01"

timeslice = dataset["shum"].sel(
    time=slice(start_date, end_date))

timeslice.plot()

# %%
# Forecast
# Verde River Near Camp Verde
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=09506000" \
       "&referred_module=sw&period=&begin_date=1989-01-01&end_date=2020-11-05"

# Now we can read it with read_table command the same as we did before
# (note run this without the skiprows and names to show what those are doing)
data = pd.read_table(url, sep='\t', skiprows=30,
                      names=['agency_cd', 'site_no',
                              'datetime', 'flow', 'code'],
                              parse_dates=['datetime'])

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek
datai = data.copy()
datai = datai.set_index('datetime')
# %%
# Finding Forecast Values
datai = datai[datai.index.month == 11]
novmedian1 = datai['2015-11-7':'2020-11-13'].median()
#print('Week 1 forecast is 156 cfs')
# %%
datai = datai[datai.index.month == 11]
novmedian2 = datai['2015-11-14':'2020-11-20'].median()
#print('Week 1 forecast is 154 cfs')
# %%
