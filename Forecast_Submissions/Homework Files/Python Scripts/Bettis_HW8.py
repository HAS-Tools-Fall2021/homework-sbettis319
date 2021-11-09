# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
# Set a grey background
sns.set(style="darkgrid")
df = sns.load_dataset('iris')
# %%
# Set the file name and path to where you have stored the data
filename = 'streamflow_week8.txt'
filepath = os.path.join('..', 'data', filename)
print(os.getcwd())
print(filepath)

# %%
# Read in our data as a dataframe - making the dates into a datetime object
data = pd.read_table(filepath, sep='\t', skiprows=30,
                      names=['agency_cd', 'site_no',
                              'datetime', 'flow', 'code'],
                              parse_dates=['datetime'])

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek
# %%
# Setting datetime as the index
datai = data.copy()
datai = datai.set_index('datetime')
datai.head()

# %% Function with a for loop
def function(month, daysofmonth, startyear, data):


    '''This function can be used to find October means for any year.
        Parameters
        ----------
        month: int
                Input the month of flows desired.
        daysofmonth: int
                Input what day of the month you want to look at.
        startyear: int
                Input the year you want to start with.
        data: int
                This is important for the data to output.
        Returns
        ------
        The October means for the month and year chosen.
    '''
oct_mean = np.zeros(31)


for d in range(31):
    daytemp = d+1
    tempdata = data[(data['year'] >= 2016) & (data['month'] == 10) &
        (data['day'] == daytemp)]
    oct_mean[d] = np.mean(tempdata['flow'])
    print('Iteration', d, 'Day=', daytemp, 'Flow=', oct_mean[d])

function(10, 17, 2016, data)

# %%
# Finding my forecast submission values using datatime
datai = datai[datai.index.month == 10]
octmean1 = datai['2010-10-17':'2020-10-23'].mean()
octmean2 = datai['2010-10-24':'2020-10-30'].mean()

print("My forecast for week 1 is ", octmean1, "cfs")
print("My forecast for week 2 is ", octmean2, "cfs")
print("Flow seems to be larger for the second week forecast")
# Just look at the flow values
# %%
# Graph 1: Flow in 2010-2020 from October 17-23
fig, ax = plt.subplots()
for i in range(2010, 2020):
    plot_data = data[(data['year'] == i) & (data['month'] == 10)]
    ax.plot(plot_data['day'], plot_data['flow'],
    label=i)
    ax.set(title="October Flow, 17-23", xlim=[17, 23], ylim=[50, 300])
    ax.legend(ncol=2)
plt.show()
fig.savefig("Graph1.png")
print("2010 had a an above average flow on the 22nd of the month")
# %%
# Graph 2: Flow in 2010-2020 from October 24-30
fig, ax = plt.subplots()
for i in range(2010, 2020):
    plot_data = data[(data['year'] == i) & (data['month'] == 10)]
    ax.plot(plot_data['day'], plot_data['flow'],
    label=i)
    ax.set(title="October Flow, 24-30", xlim=[24, 30], ylim=[50, 200])
    ax.legend(ncol=2)
plt.show()
fig.savefig("Graph2.png")
print("2011 had an above average flow from the 27-28th")
# %%
# Graph 3: Flow in 2010-2020 from October 18-30th (both weeks together)
fig, ax = plt.subplots()
for i in range(2010, 2020):
    plot_data = data[(data['year'] == i) & (data['month'] == 10)]
    ax.plot(plot_data['day'], plot_data['flow'],
    label=i)
    ax.set(title="October Flow, 17-30", xlim=[17, 30], ylim=[50, 260])
    ax.legend(ncol=2)
plt.show()
fig.savefig("Graph3.png")
print("Peaks in 2010 and 2015 might throw off the average flow values")
# %%
# Graph 4 : Box and Whisker plot showing the flow for everyday
fig, ax = plt.subplots()
ax = sns.boxplot(x='day', y="flow",  data=data, linewidth=0.1)
ax.set(yscale='log')
ax.set_xlabel('Forecast Week')
ax.set_ylabel('Flow (cfs)')
plt.show()
fig.savefig("Graph4.png")
