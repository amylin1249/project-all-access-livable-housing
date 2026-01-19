# All Access Livable Housing

## Members

- Haeji Ahn <ahaeji925@uchicago.edu>
- Lily Hoffman <lshoffman@uchicago.edu>
- Amy Lin <amsylin@uchicago.edu>
- Amanda Song <amandasong@uchicago.edu>

## Abstract

Several cities in the US are experiencing a homelessness crisis, with San Francisco often cited due to its high housing prices and low supply. Our project aims to analyze homelessness patterns in San Francisco (and potentially the nearby cities of Oakland and Berkeley). 

Some questions we have are: 
-	How have homelessness rates changed in relation to housing prices over time?
-	Are there spatial patterns for where homeless encampments are located, especially compared with indicators like income levels, property values, and rent burden?
-	Are the locations and concentrations of homeless shelters aligned with encampments?
-	How have encampment locations shifted as the frequency of enforcement actions, like sweeps, increased?

Our project focus lends itself naturally to mapping. Since the city already publishes a map with the locations of encampments, we plan to use statistical analysis to improve the accuracy of estimates, and to pair these preexisting known locations with other relevant information (e.g., neighborhood composition, shelter locations). We want to include a time component, where the user could specify a date, and it will return multiple maps and relevant statistics. 


## Preliminary Data Sources

### Data Source #1: DataSF Open Data Portal
-	Summary: This data portal, published by the City of San Francisco, contains many datasets of interest. In particular, “311 Cases” provides a comprehensive list of 311 service calls (non-emergency municipal service requests) in SF, and there is a filtering category for “Homeless Concerns.” Because each call includes location (latitude and longitude), we will be able to map the calls to their respective tracts within the city. “Quarterly count of tents, structures, and lived-in vehicles” includes a quarterly count and locations of the tents, structures, and vehicles (both passenger + non-passenger) that seem to be lived in, which will enable us to analyze how their counts and locations have evolved over time, especially with external factors (e.g., raids). “HSH Shelter Waitlist” contains the current San Francisco adult shelter reservation waitlist. This dataset could be used to see trends in shelter demand. 
-	Source URL: 1) https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6/about_data, 2) https://data.sfgov.org/Housing-and-Buildings/Quarterly-count-of-tents-structures-and-lived-in-v/w9ip-yrij/about_data, 3) https://data.sfgov.org/Health-and-Social-Services/HSH-Shelter-Waitlist/w4sk-nq57/about_data
-	Source Type: API
-	Challenges: For “311 Cases”, there could be reporting bias (vs. official counts), since this data reflects citizen reporting behavior rather than a verified census. This may lead to higher densities in neighborhoods where residents are more likely to report issues, which might not perfectly align with the actual distribution of the unhoused population. There could also be issues with duplication, as multiple people could call for the same incident. For “Quarterly count of tents, structures, and lived-in vehicles”, the counts are conducted on a tent/structure/vehicle level rather than the count of individuals and may not provide a complete view of the density of homeless people in each neighborhood. For “HSH Shelter Waitlist,” the dataset is updated daily, which means that we would have to find an efficient way to look through all the archived datasets to have a count of the number of people on the waitlist over time. 

### Data Source #2: News Articles
-	Summary: We plan to scrape news sites (up to five) for articles that mention sweeps of homeless encampments and their locations, for the purpose of tracking where sweeps are conducted. Our current top choices (not in any particular order) for news sites are: the SF Chronicle, SFGATE, KTVU Fox 2 San Francisco, CalMatters, Mission Local, Berkeleyside, and the Oaklandside. 
-	Source URL: Varies. Here is an example article that mentions a sweep of a homeless encampment on Alameda Street between Bryant and Potrero in San Francisco: https://missionlocal.org/2015/08/the-death-and-life-of-a-san-francisco-homeless-encampment/ 
-	Source Type: Webpage (scraping)
-	Challenges: First, while some articles may name an intersection or a park, others may be too general to pinpoint a specific location (e.g., articles that only mention one street name). In addition, we will not be able to quantify the size of each encampment, which precludes us from doing any further analysis in that regard. Third, the SF Chronicle is arguably the most well-known local news source for the area, but it is paywalled, meaning that we likely cannot use it for our project. Finally, although the location of encampments is currently publicly made available by the City of San Francisco, meaning that they do not see any ethical concerns with this, we want to ensure that our mapping of sweeps would not cross any ethical boundaries. 

### Data Source #3: San Francisco Department of Homelessness and Supportive Housing (HSH) Reports and Data
-	Summary: This portal, while managed by the City of San Francisco, contains reports and data published by the San Francisco Department of Homelessness and Supportive Housing (HSH). We have primarily identified a few reports and datapoints that may be of higher relevance to our project: 1) Point-in-time count (biennial count of people experiencing homelessness), 2) Housing inventory (HSH’s inventory of housing program types by household type), 3) Shelter and crisis interventions (temporary interventions that serve as emergency shelters, seasonal shelters, or transitional housing), and 4) Access point locations (which serve as a proxy for shelters since these are initial entry points into the homelessness service system). These reports and data will be used to deepen our understanding of homelessness in the city, identify interventions and policies implemented, and complement earlier data sources to fill in data gaps. 
-	Source URL: https://www.sf.gov/resource--2024--research-and-reports; https://www.sf.gov/resource--2024--get-person-homelessness-help-san-francisco 
-	Source Type: Webpage (qualitative reports and summary data)
-	Challenges: 1) First, PIT count results that are publicly available mainly include aggregated numbers, which do not provide more granular data on specific encampments within the city. We will try to link the numbers here to the quarterly tent, structure, and vehicle count (which has a breakdown by location) to estimate the number of people at each location. It is also conducted biennially, which means that the counts do not reflect changes between count periods (every two years). 2) The PIT may also underestimate the number of homeless people in SF. While the count is released by the HSH, these numbers are also approximated due to limitations of the methodology adopted for the count. There are also plans to change the PIT count methodology in 2026, which may impact the scalability and comparability of our results to future projects. We hope to use statistical analysis to provide a more accurate estimate of the numbers. 3) Additionally, the Housing Inventory and Shelter and Crisis Interventions webpages seem to only provide current point-in-time data instead of time-series data, which may limit our ability to compare how such interventions have changed over time in response to changes in homelessness counts. Certain definitions of counts are also not very clear – for example, whether the inventory of housing resources refers to available or occupied units/beds. 4) The webpage on access point locations, while may be a close proxy to shelters given that shelter data are often not consolidated and published, are ultimately still different from shelters themselves. As a result, we do not have actual data on how shelter capacity is distributed across neighborhoods.

### Data Source #4: Zillow Renter Index
-	Summary: This is a smoothed measure of the typical observed market rate of rent across a given region. ZORI is a repeat-rent index that is weighted to the rental housing stock to ensure representativeness across the entire market, not just those homes currently listed for-rent. The index is dollar-denominated by computing the mean of listed rents that fall into the 35th to 65th percentile range for all homes and apartments in a given region, which is weighted to reflect the rental housing stock. It comes from Zillow.
-	Source URL: https://www.zillow.com/research/data/ 
-	Source Type: Bulk data
-	Challenges: The data is only available at the zip code level, which may not be granular enough for our analysis. In addition, it is only an approximation of rental price over a band. Alternatively, we may scrape rental data from Zillow to get a neighborhood index of renter affordability and develop a clearer sense of the rental price distribution. 

### Data Source #5: Census Data
-	Summary: The National Historical Geographic Information System (NHGIS) is a popular source for census data. Usually going all the way down to the census tract, it includes demographic information and housing information, including median rent, median property value, and rent burden. It is published by IPUMS at the University of Minnesota.
-	Source URL: https://data2.nhgis.org/main
-	Source Type: Bulk data
-	Challenges: Since some of us have worked with census data before, we don’t have any major concerns about it. We will just need to be thoughtful about how we spatially join it to the other data that we have. 

## Questions

1.	We would like to make sure that we sufficiently meet the requirement for simulation, prediction, or statistical analysis. We think that this project will involve statistical analysis, potentially around the relationship between changes in homelessness and changes in housing prices, or other demographic or external variables. We also want to see if statistical analysis can be used to generate more accurate estimates. Do you have any additional thoughts on other ways we can engage with the simulation or prediction piece? 
2.	As we discussed with you previously, we would like to ensure that this project is feasible given the constraints of the class (the amount of time we have to complete the project and the skills we will learn over the course of the quarter). From what we have here, do you see any places where you think we could narrow (or places we could expand if they are easier to work on or more relevant to what we will learn)? We recognize that we currently have many data sources and will also research more on our end to eventually filter only datasets that are necessary for our project.