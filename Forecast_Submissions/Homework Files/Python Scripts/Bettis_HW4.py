# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
from numpy.core.fromnumeric import ndim
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('../data', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Starter Code
# Count the number of values with flow > 600 and month ==7
flow_count = np.sum((flow_data[:,3] > 600) & (flow_data[:,1]==7))

# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', np.round(flow_mean,2), "when this is true")

# Make a histogram of data
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column - grab out the 10th, 50th and 90th percentile flow values
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)

# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])
# %%
flow_data.ndim
flow_data.shape
flow_data.size

# %%
#Trying to figure out histograms

flow_mean = np.mean(flow_data[(flow_data[:,3] > 100) & (flow_data[:,1]==9),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', np.round(flow_mean,2), "when this is true")

# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

flow_mean = np.mean(flow_data[(flow_data[:,3] < 100) & (flow_data[:,1]==9),3])
print("Flow meets this critera", flow_count, " times")
print('And has an average value of', np.round(flow_mean,2), "when this is true")

# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

flow_mean = np.mean(flow_data[(flow_data[:,3] < 100) & (flow_data[:,1]==9) & (flow_data[:,2]== 20), 3])

print(flow_mean)

flow_mean = np.mean(flow_data[(flow_data[:,3] > 100) & (flow_data[:,1]==9) & (flow_data[:,2]== 20), 3])

print(flow_mean)

# %% Question 3
flow_mean = np.mean(flow_data[(flow_data[:,3] > 140) & (flow_data[:,1]==9), 3])

print(flow_mean)

# %% Question 4
flow_mean = np.mean(flow_data[(flow_data[:,3] > 140) & (flow_data[:,1]==9)& (flow_data[:,0] <= 2000), 3])

print(flow_mean)

flow_mean = np.mean(flow_data[(flow_data[:,3] > 140) & (flow_data[:,1]==9)& (flow_data[:,0] >= 2010), 3])

print(flow_mean)
# %% Question 5
flow_mean = np.mean(flow_data[(flow_data[:,3] > 140) & (flow_data[:,1]==9)& (flow_data[:,2] <= 15), 3])

print(flow_mean)

flow_mean = np.mean(flow_data[(flow_data[:,3] > 140) & (flow_data[:,1]==9)& (flow_data[:,2] >= 15), 3])

print(flow_mean)
# %%
