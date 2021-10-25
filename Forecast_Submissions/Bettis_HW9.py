# %%
# Import needed modules
import pandas as pd
import matplotlib.pyplot as plt
from numpy.lib.function_base import average, median
import datetime
import os
import dataretrieval.nwis as nwis
import json
import urllib.request as req
import urllib
# Set a grey background
import seaborn as sns
sns.set(style="darkgrid")
df = sns.load_dataset('iris')

# %%
# Importing a URL to get data from instead of calling it from a text file
# We should break the URL up onto multiple lines so it will be easier to read
# Verde River Near Camp Verde
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=09506000" \
       "&referred_module=sw&period=&begin_date=1989-01-01&end_date=2020-10-21"

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
# Mesonet Example
# Here are some helpful links for getting started
# https://developers.synopticdata.com/about/station-variables/
# https://developers.synopticdata.com/mesonet/explorer/
# https://explore.synopticdata.com/metadata/stations?status=ACTIVE

# First Create the URL for the rest API
# Insert your token here
mytoken = '2937e314803a4e31b8423f6b5da86644'

# This is the base url that will be the start our final url
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for Montezuma Castle near Camp Verde
args = {
    'start': '200001014000',
    'end': '202110230000',
    'obtimezone': 'UTC',
    'vars': 'air_temp',
    'stids': 'MCZA3',
    'units': 'precip|mm',
    'token': mytoken}
# Takes your arguments and paste them together
# Into a string for the api
# (Note you could also do this by hand, but this is better)
apiString = urllib.parse.urlencode(args)
print(apiString)

# Add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Now we are ready to request the data
response = req.urlopen(fullUrl) 
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_1']

precip_data = pd.DataFrame({'Precipitation (mm)': precip},
                           index=pd.to_datetime(dateTime))

# Now we can combine this into a pandas dataframe
data = pd.DataFrame({'Precipitation': precip}, index=pd.to_datetime(dateTime))
# %%
# Now convert this to weekly data using resample
# Could not actually use this
weekly_data = data.resample('W').mean()
print(weekly_data)
# %%
# Finding Forecast Values
datai = datai[datai.index.month == 10]
octmedian = datai['2015-10-24':'2020-10-31'].median()
print('Week 1 forecast is 129 cfs')
# %%
datai = datai[datai.index.month == 11]
novmedian = datai['2015-11-01':'2020-11-06'].median()
print('Week 1 forecast is 159 cfs')
# %%
# Graph for streamflow in 2010-2020 from October 24-31
fig, ax = plt.subplots()
for i in range(2010, 2020):
    plot_data = data[(data['year'] == i) & (data['month'] == 10)]
    ax.plot(plot_data['day'], plot_data['flow'],
    label=i)
    ax.set(title="Last week of October flow, 24-31", xlim=[24, 31], ylim=[50, 260])
    ax.legend(ncol=2)
plt.show()
fig.savefig("Graph1.png")
# %%
# Graph for streamflow in 2010-2020 from November 1-6
fig, ax = plt.subplots()
for i in range(2010, 2020):
    plot_data = data[(data['year'] == i) & (data['month'] == 11)]
    ax.plot(plot_data['day'], plot_data['flow'],
    label=i)
    ax.set(title="1st Week of November flow, 1-6", xlim=[1, 6], ylim=[50, 260])
    ax.legend(ncol=2)
plt.show()
fig.savefig("Graph2.png")

# %%
