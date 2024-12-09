# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
from fredapi import Fred

# Customize plots for matplotlib
plt.style.use('fivethirtyeight')  # Set the default plotting style
pd.set_option('display.max_columns', 500)  # Allow displaying up to 500 columns in pandas
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]  # Extract colors for consistent styling

# Initialize Fred API with a personal API key
fred = Fred(api_key='5f9c44331b1d3985ff8f129641df06bd')

# Search for economic data related to "S&P"
search_results = fred.search('S&P')  # Search FRED for series related to "S&P"

# Plot S&P 500 price data
sp500 = fred.get_series(series_id='SP500')  # Fetch the series data for S&P 500
sp500.plot(figsize=(10, 5), title='S&P 500', lw=2)
#plt.show()
plt.clf()
# Search for unemployment related IDs
#unemp_df = fred.search('unemployment')
#unrate = fred.get_series('UNRATE')
#unrate.plot()
#plt.show()
#plt.clf()
# Search for unemployment rate data by state with filters
unemp_df= fred.search('unemployment rate state', filter=('frequency', 'Monthly'))

unemp_df= unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')

unemp_df= unemp_df.loc[unemp_df['title'].str.contains('Unemployment Rate')]
all_results = []
for myid in unemp_df.index:
    results = fred.get_series(myid)
    results = results.to_frame(name=myid)
    all_results.append(results)

uemp_results = pd.concat(all_results,axis=1)
cols_to_drop = [col for col in uemp_results.columns if uemp_results[col].count() <= 4]
uemp_results = uemp_results.drop(columns = cols_to_drop, axis=1)
uemp_states = uemp_results.copy()
uemp_states = uemp_states.dropna()
print(uemp_results.shape)
print(uemp_results.head())
