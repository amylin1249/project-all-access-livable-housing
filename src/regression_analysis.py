##### Data Set up #####
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np 
import altair as alt
import geopandas as gpd
from pathlib import Path
from datetime import datetime
from datatypes import (
  
    CLEAN_311,
    CLEAN_ENCAMP,
    CLEAN_ZILLOW,
    CLEAN_CROSSWALKS,
    JOINED_ENCAMP_TRACTS
)


# Step 1: Load in encampmment-tract crosswalk
df_crosswalk = pd.read_csv('joined_encampment_tracts.csv')
# Step 2: Aggregate up to the quarter date, tract level
df_crosswalk = df_crosswalk.groupby(['geoid', 'date'])[['tents', 'structures', 'vehicles']].sum().reset_index()

# Step 3: Merge data files on id 
df_311_crosswalk = pd.read_csv('joined_311_tracts.csv')

df_311_crosswalk['total_encampments'] = 1
df_311_crosswalk = df_311_crosswalk.groupby(['geoid', 'date'])[['total_encampments']].sum().reset_index()


merged_df = pd.merge(df_311_crosswalk, df_crosswalk, on=['geoid', 'date'], how='inner')

acs_data = pd.read_csv('sf_census_tracts.csv')
acs_data = acs_data.rename(columns={"TL_GEO_ID": "geoid"})

merged_df = pd.merge(merged_df, acs_data, on=['geoid'], how='inner')

merged_data = pd.read_csv('merged_data.csv')
## Only keep tract date eviction rate, and median rent ##

merged_data = merged_data[['tract', 'date', 'median_rent', 'eviction_rate']]
merged_data = merged_data.rename(columns={'tract': 'geoid'})

merged_df = pd.merge(merged_df, merged_data, on=['geoid', 'date'], how='inner')


### Run regressions ####

# 1. Define the OLS model using formula API
model = smf.ols(formula='total_encampments ~ median_rent + med_hh_inc + white_pct + eviction_rate + C(date)', data=merged_df)

# 2. Fit the model specifying 'cluster' as the covariance type
results = model.fit(cov_type='cluster', cov_kwds={'groups': merged_df['geoid']})

# 3. Print the summary with the corrected standard errors and p-values
print(results.summary())

model2 = smf.ols(formula='total_encampments ~ median_rent + med_hh_inc + white_pct + eviction_rate  + tents + structures + vehicles + C(date)', data=merged_df)
results2 = model2.fit(cov_type='cluster', cov_kwds={'groups': merged_df['geoid']})
print(results2.summary())


