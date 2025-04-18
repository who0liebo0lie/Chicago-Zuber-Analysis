#!/usr/bin/env python
# coding: utf-8

# ## Chicago Taxi Company Evaluation

# SQL Project on Zuber 
# Project will show competency on evaluating a Chicago based ride share app (Zuber) for patterns in the available information.  Details to be discovered are understanding passenger preferences and the impact of external factors on rides.
# 
# Several files will be uploaded:
# 
# 1)company table contains data columns of:
# company_name: taxi company name
# trips_amount: the number of rides for each taxi company on November 15-16, 2017.
# 
# 2)neighborhood_average_dropoff table contains data columns of:
# dropoff_location_name: Chicago neighborhoods where rides ended
# average_trips: the average number of rides that ended in each neighborhood in November 2017.
# 
# 3)loop table contains data from previous SQL project regarding data from rides traveling between the Loop neighborhood to O'Hare International Airport.  The columns are:
# start_ts
# pickup date and time
# weather_conditions
# weather conditions at the moment the ride started
# duration_seconds
# ride duration in seconds
# 
# The files will be imported and studied. Evaluation will be made for each file type to ensure data types are correct.  Visual for top taxi companies will be generated. The top 10 neighborhoods will be identified in terms of drop-offs with visuals. Project will also test the following hypothesis:
# "The average duration of rides from the Loop to O'Hare International Airport changes on rainy Saturdays."

# In[1]:


#import libraries 
import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats as st
import plotly.graph_objects as go
from scipy.stats import ttest_ind


# In[2]:


#import csv file 
company = pd.read_csv('/datasets/project_sql_result_01.csv')
print(company.head())
print(company.info())
#note that there are no empty columns
#the data types for each column seem correct.  The company name is an object and trips_amount is an integer.  


# In[3]:


#check for duplicated values 
company.duplicated().sum()


# In[4]:


#confirm no empty columns 
company.isna().sum()


# In[5]:


top_company=company.sort_values(by='trips_amount', ascending=False)
top_company.head(10)


# In[6]:


#check datatypes of dataframe 
top_company.info()


# In[7]:


top_company.head(20).plot.barh(
title='Most Used Taxi Companies for November 15/16, 2017',
color='purple', 
x='company_name',
y='trips_amount',
xlabel='Number of Trips', 
ylabel='Taxi Company')

#x='trips_amount',
#y='company_name',
#xlabel='Number of Trips', 
#ylabel='Taxi Company')


# The most popular taxi company to be used is "Flash Cab".  Flash Cab is now the lead competitior for Zuber.  Their name implies part of their service is successful due to their speed of answering calls.  Their number of completed trips is nearly double its closest four competitors. Unsure if their dominancy is due to the area they service, the number of employees, or types of services they provide (restricting range of rides).  

# In[8]:


#import csv file 
neighborhood_average_dropoff = pd.read_csv('/datasets/project_sql_result_04.csv')
print(neighborhood_average_dropoff.head())
print(neighborhood_average_dropoff.info())
#note that there are no empty columns
#the data types for each column seem correct.  The location name is an object and average_trips is a float.  


# In[9]:


#check for duplicated values 
neighborhood_average_dropoff.duplicated().sum()


# In[10]:


#confirm no empty columns 
neighborhood_average_dropoff.isna().sum()


# In[11]:


#sort the neighborhood_average_dropoff dataframe for highest value 
top_neighborhoods = neighborhood_average_dropoff.sort_values(by='average_trips', ascending=False)
top_neighborhoods.head(20)


# In[12]:


#add visualization for most active areas. 
top_neighborhoods.head(10).plot(
kind='bar',
title='Most Active Zuber Neighborhoods of November 2017',
color='pink', 
x='dropoff_location_name',
y='average_trips',
xlabel='Neighborhood', 
ylabel='Average Number of Trips')


# The most popular neighborhood to take a Zuber is the Loop.  Seeing as this is the centralized business district of Chicago this makes sense.  Many people would be in the neighborhood without a car as a visitor or not want to utilize their own car in the area due to the difficulty in parking.  The least used neighborhood is Sheffield & DePaul which is less tourist area.   

# In[13]:


#import csv file 
loop = pd.read_csv('/datasets/project_sql_result_07.csv')
print(loop.head())
print(loop.info())


# In[14]:


#check for duplicates
loop.duplicated().sum()


# In[15]:


#evaluate if duplicate or unique values 
loop.value_counts()


# removed instruction to drop duplicates due to correct note above. 

# In[16]:


#check for blank values
loop.isna().sum()


# In[17]:


#convert start_ts to date and time
loop['start_ts'] = pd.to_datetime(loop['start_ts'])

# Separate the data
rainy = loop[(loop['weather_conditions'] == 'Bad') & (loop['start_ts'].dt.dayofweek == 5)]['duration_seconds']
non_rainy = loop[(loop['weather_conditions'] == 'Good') & (loop['start_ts'].dt.dayofweek == 5)]['duration_seconds']

# Perform t-test
t_stat, p_value = ttest_ind(rainy, non_rainy, nan_policy='omit')

# Set significance level
alpha = 0.05

# Interpret the results
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant change in ride duration on rainy Saturdays.")
else:
    print("Fail to reject the null hypothesis. No significant change in ride duration on rainy Saturdays.")


# Hypothesis Testing 
# Is the average duration of rides from the Loop to O'Hare International Airport change on rainy Saturdays? 
# 
# Null hypothesis is that the average duration of rides is the same, regardless of the weather. 
# Alternative hypothesis is that average duration of rides differs according to the weather.  This will be evaluated by information on a rainy Saturday. Using alpha threshold of 0.05 becasue this demonstrates statistical signficance.   

# General Conclusion:
#     Zuber is aiming to be a new ride source for the Chicago area. Based on the data from a date in November their lead competitor will be a company called Flash Cab. Unsure if their dominancy is due to the area they service, the number of employees, or types of services they provide (restricting range of rides). Zuber could look into merging/purchasing their company since they have dominance.  An even more cost effective way would be to consider purchasing the 3/4th most popular companies (Medallion Leasing or Yellow Cab).  The price would be lower and the merge with Zuber would set Zuber up in the neighborhood as direct compeititors. This would help focus efforts on the three most popular areas (The Loop, River North, and Steeterville). These are all high tourist areas. However even in tourist areas the weather will effect the Zuber app.  Rides will take longer when there is precipitation.  
