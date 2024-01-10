
import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
from streamlit_folium import st_folium


# Load data outside the function and cache it
@st.cache_data  # This decorator caches the data, so it's only reloaded if the file changes
def load_data():
    return pd.read_csv('Modified_Companies_23.csv')

Companies_23 = load_data()

# Function to create a Folium map with an optional heatmap
def create_map(show_heatmap):
    # Creating a base map using Folium
    map = folium.Map(location=[40.7128, -74.0060], zoom_start=4)

    # If the heatmap toggle is on, add the heatmap layer
    if show_heatmap:
        heatmap_data = Companies_23[['Latitude', 'Longitude']].dropna().values.tolist()
        HeatMap(heatmap_data).add_to(map)
    else:
        # Adding markers for each company
        for _, row in Companies_23.iterrows():
            tooltip = f"Company: {row['Company']}"
            popup = f"""
                     <div>
                     <strong>Company:</strong> {row['Company']}<br>
                     <strong>Violation:</strong> <span style='color:red;'>{row['Violation']}</span><br>
                     <strong>Date:</strong> {row['Date']}<br>
                     <strong>Action:</strong> {row['Action']}<br>
                     <a href="{row['Link']}" target="_blank">More Info</a>
                     </div>
                     """
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                tooltip=tooltip,
                popup=popup,
                icon=folium.Icon(icon="info-sign")
            ).add_to(map)

    return map

# Streamlit app layout
st.title('IDOI Enforcement Action Visualizer for year 2023')
url = "https://www.in.gov/idoi/enforcement/enforcement-actions/"
st.write("[Data Source](%s)" % url)
st.write('This visualization presents the geographic distribution of companies included on the 2023 Enforcement Action List.')

show_heatmap = st.checkbox('Show Heatmap (Click me!)', value=False)

company_map = create_map(show_heatmap)
st_folium(company_map, width=700, height=500)

st.header('Types of Violation for companies')

# Data for chart
chart_data = pd.DataFrame({
    'Violation Type': [
        'Failure to Enter x Transactions', 
        'Suspension Order', 
        'No home State License', 
        'License Revocation', 
        'Administration Action', 
        'Failure to Report', 
        'Failure to pay taxes'
    ],
    'Count': [
        23, 
        1, 
        1, 
        1, 
        1, 
        1, 
        1
    ]
})

chart_data = chart_data.set_index('Violation Type')
st.bar_chart(chart_data)


st.header('Workflow for this visualization/website')
st.image('Workflow.png')
st.markdown("""
This website is made by Shiva Kumar Pendem to showcase skills to Indiana Department of Insurance.

Check out:
- [My Portfolio Website](https://shivakumarpendem.engineer/)
- [My Github](https://github.com/ShivaKumar8037)
""", unsafe_allow_html=False)
