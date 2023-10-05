# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 02:56:31 2023

@author: lenovo
"""

import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import haversine_distances
from math import radians, degrees, asin, atan2

# Read coordinates from Excel
df = pd.read_excel('C:\\Users\\lenovo\\Desktop\\Streamlit\\Unpaved Road DBSCAN.xlsx')
latitudes = df['Latitude'].tolist()
longitudes = df['Longitude'].tolist()

# Convert latitudes and longitudes to radians for haversine_distances
coordinates = [(radians(lat), radians(lon)) for lat, lon in zip(latitudes, longitudes)]
distance_matrix = haversine_distances(coordinates, coordinates) * 6371000  # Radius of Earth in meters

# Apply DBSCAN with a maximum distance of 50 meters
dbscan = DBSCAN(eps=50, min_samples=2, metric='precomputed')
clusters = dbscan.fit_predict(distance_matrix)

# Assuming 'clusters' is the variable containing cluster labels
unique_clusters = set(clusters)

for cluster_label in unique_clusters:
    cluster_points = [coordinates[i] for i, label in enumerate(clusters) if label == cluster_label]
    print(f'Cluster {cluster_label}: {cluster_points}')

# Create a DataFrame to store the clusters and their corresponding coordinates
cluster_df = pd.DataFrame({'Cluster': clusters, 'Latitude': latitudes, 'Longitude': longitudes})

# Convert back to latitude and longitude
radius = 6371000  # Radius of Earth in meters

# Save the DataFrame to an Excel file
cluster_df.to_excel('Unpaved_Roads_DBSCAN.xlsx', index=False)
