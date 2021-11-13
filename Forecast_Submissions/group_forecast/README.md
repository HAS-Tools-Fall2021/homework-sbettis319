# Forecast_Submissions

## Team 1
- Sierra Bettis
- Gigi Giralte
- Xiang Zhong

### Date: 11/14/2021

### Assignment Number: 12
____________
### Summary
For this week's forecast task, Sierra established the whole structure of our scripts and handled the map; Gigi provided her function for forecasting; Xiang got the timeseries of predicted precipitation from GFS.

Our logic of combination is: ...

One week forecast streamflow is () cfs;
Two week forecast streamflow is () cfs.

---
### Forecast function
---
### Map
---
### Graph
The graph we generated is a time series plot for next two weeks' accumulated precipitation.

We first grabbed the data from NOAA NCEI's data archive using urllib package, and since the grabbed data is saved in grb2 format, we used pygrib package to help open and extract data values.

Because we did not find a subset tool for the data, we have to open a global map for each file and grab the grid nearest to River Verde to get a single grid value. The grabbed single grid value was then written in a data frame and saved in a csv file to be applied in our forecast.

The predicted precipitation data is 3-hourly average value, from the plot we can tell there might be some rainfall next week (remember to double check this part). 

(Gigi please help add how we used this data to your great forecast function~)
