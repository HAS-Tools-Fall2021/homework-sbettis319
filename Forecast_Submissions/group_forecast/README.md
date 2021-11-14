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

One week forecast streamflow is 144.6 cfs.\
Two week forecast streamflow is 143.1 cfs.

---
### Forecast function
In our function to determine our Week 1 and Week 2 forecasted flow values, there were two separate parts: if there was no forecasted precipitation and if there was forecasted precipitation.

For the first part, if there was no forecasted precipitation, it would take the flow values from this past week (November 7 - November 13) and find the average of them. From there, the minimum value for that week and maximum value for that week would be found. The difference between these two would be taken. For the Week 1 forecast, it is the average from the past week and the Week 2 forecast is the average minus the difference between the max and min values.

If there was precipitation forecasted, the steps are similar. The first thing is to get the average from this past week. One of the parameters is the amount of precipitation forecasted (in inches) and about one inch is 14 cfs so this value is multiplied by 14. From here, to find the Week 1 forecast, you take the forecast mean and add the forecasted flow. To find the Week 2 forecast, you take the forecast mean and subtract the forecasted flow.

---
### Map
The map was created using the NCEP Reanalysis data precipitation data ('prate') that was turned into a geodataframe and resampled to get annual precipiation data as well as USGS Watershed Boundary HUC4. A point was also added for the location of the stream gauge (Verde River near Camp Verde). A basemap of landscape was also added to visualize the annual precipiation and the watershed boundaries.

![](assets/README-0fdeb2d0.png)

---
### Graph
The graph we generated is a time series plot for next two weeks' accumulated precipitation.

We first grabbed the data from NOAA NCEI's data archive using urllib package, and since the grabbed data is saved in grb2 format, we used pygrib package to help open and extract data values.

Because we did not find a subset tool for the data, we have to open a global map for each file and grab the grid nearest to River Verde to get a single grid value. The grabbed single grid value was then written in a data frame and saved in a csv file to be applied in our forecast.

The predicted precipitation data is 3-hourly average value, from the plot we can tell there might be some rainfall next week (remember to double check this part).

Assuming that there is predicted precipitation values for the next two weeks, this total number would be converted into inches (if not already in inches) and entered as a parameter into our forecast function. From here, since about one inch of water is equal to 14cfs, we multiply the inches value by 14. This is then added to the mean flow for this past week as our week 1 forecast and then subtracted from the mean flow for the week 2 forecast.


![](assets/README-69b0c05b.png)
