import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
from fredapi import Fred
# Initialize Fred API with a personal API key
fred = Fred(api_key='5f9c44331b1d3985ff8f129641df06bd')
# Fetch unemployment data and apply filters
unemp_df = fred.search('unemployment rate state', filter=('frequency', 'Monthly'))
unemp_df = unemp_df.query(
    'seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"'
)
unemp_df = unemp_df.loc[unemp_df['title'].str.contains('Unemployment Rate')]

# Retrieve data for each series
all_results = []
for myid in unemp_df.index:
    results = fred.get_series(myid)
    if results.isna().all():
        continue  # Si todos son NaN, saltar esta serie y no agregarla
    else:
        results = results.to_frame(name=myid)
        all_results.append(results)
        time.sleep(0.1)

# Combine all results into one DataFrame
uemp_results = pd.concat(all_results, axis=1)

# Drop columns with insufficient data
cols_to_drop = [col for col in uemp_results.columns if uemp_results[col].count() <= 4]
uemp_results = uemp_results.drop(columns=cols_to_drop, axis=1)

fig=px.line(uemp_results)
fig.show()
