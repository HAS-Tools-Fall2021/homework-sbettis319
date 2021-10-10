# %%
# Import the modules we will use
import os
import numpy as np
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average, median
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 
sns.set(style="darkgrid")
df = sns.load_dataset('iris')
# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week7.txt'
filepath = os.path.join('..', '..', 'data', filename)
print(os.getcwd())
print(filepath)

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep='\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()
np.size(flow_data)
np.ndim(flow_data)

# %% Function with a for loop
# Trying to find the mean flow values for days in October
def oct_mean(month, daysofmonth, startyear, data) : 
    oct_mean = np.zeros(31)
    for d in range(31):
        daytemp = d+1
        tempdata = data[(data['year'] >= 2016) & (data['month'] == 10) & (data['day'] == daytemp)]
        oct_mean[d] = np.mean(tempdata['flow'])
        print('Iteration', d, 'Day=', daytemp, 'Flow=', 
        oct_mean[d])
    return oct_mean
oct_mean (10, 11, 2016, data)

# %%
## Finding my forecast submission values
flow_median1 = np.median(flow_data[(flow_data[:, 2] <= 18) & 
(flow_data[:, 1] == 10), 3])
flow_median2 = np.median(flow_data[(flow_data[:, 2] >  18) & 
(flow_data[:, 1] == 10), 3])
print("My forecast for week 1 is ", flow_median1, "cfs")
print("My forecast for week 2 is ", flow_median2, "cfs")

print("Flow seems to be larger for the second week forecast")
# %%
# Graph 1: Flow in 2010-2020 from October 11-18
fig, ax = plt.subplots()
for i in range(2010, 2020):
        plot_data=data[(data['year'] == i) & (data['month'] == 10)]
        ax.plot(plot_data['day'], plot_data['flow'],
                label = i)
        ax.set(title = "October Flow, 11-18", xlim=[11, 18], ylim=[0, 300])
        ax.legend(ncol = 2)
plt.show()

print("2018 had a an above average flow on the 13th and 14th of the month")
# %%
# Graph 2: Flow in 2010-2020 from October 18-25
fig, ax = plt.subplots()
for i in range(2010, 2020):
        plot_data=data[(data['year'] == i) & (data['month'] == 10)]
        ax.plot(plot_data['day'], plot_data['flow'],
                label=i)
        ax.set(title = "October Flow, 18-25", xlim=[18, 25], ylim=[0, 300])
        ax.legend(ncol = 2)
plt.show()

print("2010 had an above average flow on the 22nd")
# %% 
# Graph 3 : Box and Whisker plot showing the flow for everyday
fig, ax = plt.subplots()
ax = sns.boxplot(x='day', y="flow",  data=data, linewidth=0.1)
ax.set(yscale='log')
ax.set_xlabel('Forecast Week')
ax.set_ylabel('Flow (cfs)')
plt.show()
# %%
