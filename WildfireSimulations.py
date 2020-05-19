#!/usr/bin/env python
# coding: utf-8

# In[7]:


import copy
import folium
import numpy as np
import pandas as pd
import folium.plugins as plugins
from sklearn import preprocessing


# In[8]:



def getData():

    # read csv file
    data = pd.read_csv("./fire_archive_M6_96619.csv")
    
    # we will min-max scale brightenss (temperature) field 
    # of data to use it as color gradient in our map
    brightness = data[['brightness']].values.astype(float)
    min_max_scaler = preprocessing.MinMaxScaler()
    brightness_scaled = min_max_scaler.fit_transform(brightness)
    brightness_scaled = pd.DataFrame(brightness_scaled)

    data['brightness_scaled'] = brightness_scaled
    
    return data


# In[9]:



def getCoOrdinates(data):
    
    # get all the dates in dataset
    all_dates = data.acq_date.unique()

    # list to hold all location coordinates that have fire
    coordinates = []
    
    # list to hold all the coordinates that have fire on a given day
    locations_per_day = []

    # for each day get locations that have fire
    for date in range(len(all_dates)):
        
        data_per_day = data[data["acq_date"] == all_dates[date]]
        
        for lat, long, temp in zip(data_per_day['latitude'], data_per_day['longitude'], data_per_day['brightness_scaled']):
            locations_per_day.append([lat, long, temp])
        
        temp = copy.deepcopy(locations_per_day)
        coordinates.append(temp)

    return coordinates


# In[10]:



# get dataset
data = getData()
data.head()


# In[11]:



# get coordinates of all fire hotspots
coordinates = getCoOrdinates(data)


# In[12]:



# plot thoose coordinates according to timeline
aus_map = folium.Map([-23., 133.], zoom_start=4.5)
fire_growth = plugins.HeatMapWithTime(coordinates, radius = 10)
fire_growth.add_to(aus_map)

aus_map


# In[13]:




# save for future usage
aus_map.save('aus_map.html')


# In[ ]:




