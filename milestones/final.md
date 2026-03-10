# Project: All Access Livable Housing

## Members
- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>


## Data Documentation
Sources of data and any key gaps include:
#1: DataSF Open Data Portal - (1) 311 Cases - Deduplicating data was required; (2) Quarterly count of tents, structures, and lived-in vehicles - Data interpolation was required; (3) Evictions data
#2: Census Data - (1) ACS data - Manual imputation was required for negative values; (2) California and SF census tracts
#3: Zillow Observed Renter Index (ZORI) - Imputation was required to fill missing data
#4: HUD ZIP Code Crosswalks - Data was separated across multiple Excel files with inconsistently named columns, and imputation was required to fill missing data
#5: Sacramento 2024 PIT Count Report

The data flows through a centralized pipeline starting with automated API extraction and CSV/XLSX extraction. ZIP-level ZORI data is disaggregated to census tracts using HUD crosswalks and normalized with ACS median rent values. Daily 311 service calls, daily eviction records, and quarterly encampment counts are spatially joined to tracts and aggregated to the monthly level. Eviction counts are converted to tract-level monthly rates using census data. Quarterly encampment counts are interpolated to estimate monthly values. Tract-level street homeless population estimates are then generated using multipliers from the literature. All processed datasets are merged into a single tidy CSV, which feeds into the dashboard.

To understand this project, one should know that we used interpolation and HUD crosswalk calculations to align all data to the same spatial and temporal scale (from ZIP code or quarterly levels to monthly census tract level). The quarterly encampment counts also required direct communication with the SF Open Data Portal to obtain the underlying data.


## Project Structure
The root consists mainly of src (directory containing our source files) and other key directories (tests, raw-data, clean-data). Focusing on the src directory, we have 7 main modules spanning 3 key sections that feed into __main__: 
1. Data retrieval (get_api_data)
2. Data cleaning and processing (process_data, spatial_join, analyze_data, run_regression)
3. Data visualization (visualize, dashboard)
The above are supported by datatypes, which contains global variables used across them.

Our project pipeline begins with data retrieval. The get_api_data module retrieves eviction data from an external API and saves the results to a CSV file for use in subsequent steps.

The next stage focuses on data cleaning and processing, beginning with process_data. This module merges ACS data with tract shapefiles, cleans encampments and 311 data, imputes missing Zillow data, processes crosswalks, deduplicates and standardizes key fields, and exports cleaned datasets to CSV and shapefiles in the cleaned-data folder. We then implemented spatial_join, which applies quadtrees to match point coordinates from cleaned evictions, encampments, and 311 reports datasets to appropriate census tract polygons. The analyze_data module then aggregates counts from spatially joined datasets and consolidates metrics for analysis and visualization. run_regression examines the relationship between tract characteristics and monthly 311-reported addresses using OLS regression.

The last section focuses on visualizations and dashboarding. The visualize module generates graphs including a choropleth map, regression graph, and line graphs of rent and encampments over time. The dashboard module integrates these visualizations into an interactive interface with background information, key statistics, and a series of visualizations that illustrate how homelessness trends in SF have evolved over time.

The above modules feed into our __main__.py file, which allows the entire pipeline to be executed from the command line. Given that our modules are all interlinked, this enables users to launch the dashboard, or even regenerate clean data files, ensuring the reproducibility of our analysis. 


## Team responsibilities
### Haeji
- Implemented initial filtering of ZORI data for SF zip codes (2020-2024)
- Built an automated API pipeline to retrieve, filter, and save real-time SF eviction records as standardized CSVs (get_api_data.py)
- Computed eviction rates by normalizing monthly eviction counts with census populations
- Spearheaded dashboard implementation, ensuring smooth integration of processed data into an interactive analytical tool
- Optimized map, plot, and regression code for dashboard interactivity
- Wrote `pytest` tests for eviction dataset, api datasets, and tidying csv

### Lily
- Developed clean_address and clean_parenthesis to de-duplicate 311 service request data
- Implemented initial cleaning functions for 311 and encampment datasets
- Created run_regression.py to conduct tract-level regression analysis
- Developed regression coefficient visualization to support data interpretation
- Built initial line graphs for encampments and street homeless population estimates
- Reviewed interpolation, imputation, and other data processing choices
- Wrote `pytest` tests for de-duplication, 311 and encampment datasets

### Amy
- Co-wrote script (with Amanda) to scrape shelter waitlist datasets (later archived)
- Implemented final cleaning functions for 311 and encampment datasets (Pandas)
- Built the complete ingestion and cleaning pipeline for monthly median rent data (aside from Haeji's initial filtering step): imputed missing ZORI values, processed 20 HUD crosswalk Excel files (including imputation), and calculated weighted averages to generate tract-level monthly rent estimates
- Interpolated quarterly encampments to estimate monthly counts for each encampment type 
- Built final line graphs for encampments and street homeless population estimates
- Built line graph visualization for monthly median rent by ZIP code
- Assisted Haeji with dashboard by leading dashboard design (determining layout, visual structure, and interactive flow) and wrote textual content
- Wrote `pytest` tests for ZORI dataset and HUD crosswalks

### Amanda
- Co-wrote script (with Amy) to scrape shelter waitlist datasets (later archived)
- Cleaned and processed Census and ACS data to consolidate key metrics into tract-level CSV and shapefile outputs
- Implemented geospatial matching to assign point-based data (coordinates) to census tracts for evictions, encampments, and 311 datasets
- Aggregated encampment reports and 311 service call data by month and census tract 
- Built choropleth map with interactive tooltip to visualize key metrics across census tracts and time periods
- Built a command-line interface to streamline data processing and analysis workflows
- Wrote `pytest` tests for census and ACS data processing and spatial join


## Final thoughts
Our project set out to examine the relationship between the number of unsheltered individuals and housing prices in SF from 2020 to 2024 at the census tract level. We aimed to better understand the spatial patterns of homelessness and the factors driving variation across tracts. As we explored the problem, we identified additional relevant datasets (311 calls, eviction records) that enriched our analysis. We built a comprehensive data pipeline to harmonize these diverse sources, created visualizations to explore trends, and developed an interactive dashboard through independent research.

Our analysis revealed clear spatial concentrations of homelessness in the Tenderloin and the Mission (areas well known for homelessness). Interestingly, it also suggested a gradual shift further south into India Basin and Bayview-Hunters Point (areas not typically associated with homelessness), with a growing proportion of individuals living in vehicles rather than tents. This shift may reflect recent encampment sweeps in central neighborhoods, which may have displaced individuals toward southern areas and contributed to increases in vehicle-based homelessness. Regression analysis also found a correlation between higher citizen-reported encampments (311 service calls) and tracts with larger White populations. 

Beyond these findings, this project strengthened our technical and analytical skills, including data retrieval, cleaning, spatial analysis, and visualization. Overall, it helped us consolidate these skills while producing analyses related to real-world issues.