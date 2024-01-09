import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

# Function to create a Folium map
def create_map():
    # Load data
    Companies_23 = pd.read_csv('Modified_Companies_23.csv')

    # Creating a base map using Folium
    map = folium.Map(location=[40.7128, -74.0060], zoom_start=4)

    # Adding markers for each company
    for _, row in Companies_23.iterrows():
        tooltip = f"{row['Company']}\nViolation: {row['Violation']}\nDate: {row['Date']}\nAction: {row['Action']}"
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=tooltip,
            icon=folium.Icon(icon="info-sign")
        ).add_to(map)
    
    return map

# Streamlit app layout
st.title('Company Locations Map')
st.write('This is a map of company locations.')

# Create the map and display it in Streamlit
company_map = create_map()
st_folium(company_map, width=700, height=500)
