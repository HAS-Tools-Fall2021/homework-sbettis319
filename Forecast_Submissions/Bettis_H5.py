# Starter code for homework 5

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.algorithms import quantile

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

filepath = '../data/streamflow_week5.txt'

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep = '\t', skiprows=30,
        names =['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] = data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# %%
# Sorry no more helpers past here this week, you are on your own now :)
# Hints - you will need the functions: describe, info, groupby, sort, head and tail.

# %%
##Question 1

print(data.columns)

print(data.index)

print(data.dtypes)
# %% Question 2

data['flow'].describe()

# %% Question 3

data.groupby(['month'])[['flow']].describe()

# %% Question 4

data.sort_values(by='flow', ascending=False).head(5)

data.sort_values(by='flow', ascending=False).tail(5)

# %% Question 5

Q5 = data.sort_values(['month','flow'], ascending= False)

print(Q5)

Q5.describe()

# %% Question 6

week1f = 400

upperlimit = week1f*1.1
lowerlimit = week1f*0.9

array = (data(['flow']>= upperlimit)& (data["flow"] <= lowerlimit)]

array.values

###code not running?
# %%
