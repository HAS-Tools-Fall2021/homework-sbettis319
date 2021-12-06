# %%
import pandas as pd
import numpy as np

# %%
url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=09506000" \
       "&referred_module=sw&period=&begin_date=1989-01-01&end_date=2020-12-03"

# Now we can read it with read_table command the same as we did before
# (note run this without the skiprows and names to show what those are doing)
data = pd.read_table(url, sep='\t', skiprows=30,
                      names=['agency_cd', 'site_no',
                              'datetime', 'flow', 'code'],
                              parse_dates=['datetime'])
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek
datai = data.copy()
datai = datai.set_index('datetime')

# %%
def forecasts(start, end):
        '''
        This function determines the week 1 and week 2 forecast predictions based on Camp Verde data
        Parameters:
        "start" represents this Saturday, the 20th.
        "end" represents the end of the first week, the 17th.
        Outputs:
        This function returns a print statement that provides the forecasted flows for week 1 and week 2. 
        '''

        week_median1 = np.median(datai['flow']['2010-12-5':'2019-12-12'])
        week_median2 = np.median(datai['flow']['2010-12-19':'2019-12-26'])
        prediction = print("The forecast for week 1 is:", week_median1 , \
                "and the forecast for week 2 is:", week_median2)
        return(prediction)

forecasts(5, 21)
# %%
