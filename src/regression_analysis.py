##### Data Set up #####
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np 
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
df_crosswalk = pd.read_csv(JOINED_ENCAMP_TRACTS)
# Step 2: Aggregate up to the quarter date, tract level
df_crosswalk = df_crosswalk.groupby(['geoid', 'date'])[['tents', 'structures', 'vehicles']].sum()

# Step 3: Merge data files on id 
df_311_crosswalk = pd.read_csv('joined_311_tracts.csv')

df_311_crosswalk['total_encampments'] = 1
df_311_crosswalk = df_311_crosswalk.groupby(['geoid', 'date'])[['total_encampments']].sum()


merged_df = pd.merge(df_311_crosswalk, df_crosswalk, on=['geoid', 'date'], how='inner')

acs_data = pd.read_csv('sf_census_tracts.csv')
acs_data = acs_data.rename(columns={"TL_GEO_ID": "geoid"})

merged_df = pd.merge(merged_df, acs_data, on=['geoid'], how='inner')




# Assuming 'df' is your DataFrame and 'id' is the column defining clusters
# 'y' is the dependent variable, 'x' is the independent variable

# 1. Define the OLS model using formula API
model = smf.ols(formula='y ~ x', data=df)

# 2. Fit the model specifying 'cluster' as the covariance type
# The 'groups' keyword argument should refer to the column that defines your clusters
results = model.fit(cov_type='cluster', cov_kwds={'groups': df['id']})

# 3. Print the summary with the corrected standard errors and p-values
print(results.summary())

