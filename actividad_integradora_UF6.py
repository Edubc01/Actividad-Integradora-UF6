import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import time
import PIL as Image

st.set_page_config(page_title='Police Incident Reports from 2018 to 2020', layout='wide')

@st.cache
def run_fxn(n:int) -> list:
    return range (n)

def logoandtitle(title):
    st.markdown(f'<div class="custom-title">{title}</div>', unsafe_allow_html=True)

logoandtitle("Police Incident Reports from 2018 to 2020 in San Francisco")

# Código CSS
st.markdown("""
    <style>
        /* Importar una fuente de Google */
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

        .custom-title {
            color: white;
            text-align: center;
            font-family: 'Roboto', sans-serif; /* Cambiar la fuente */
            font-size: 3em; /* Tamaño de fuente */
            padding: 1rem;
            background-color: #081A41;
            border-radius: 8px;
            width: 100%; /* Ancho del título (ajustado al ancho de la página) */
            margin: auto; /* Centro el título */
            border: 2px solid white; /* Borde blanco */
        }
    </style>
""", unsafe_allow_html=True)

mostrar_sidebar = True

if mostrar_sidebar:
    st.sidebar.image("SFP.png", use_column_width=True)

    st.markdown("""
        <style>
            /* Estilos para el sidebar */
            .sidebar-content {
                background-color: #ECECEC;
            }
            .sidebar .stImage {
                max-width: 100px; 
                max-height: 20px; 
                width: 100%; 
                height: auto; 
            }
        </style>
    """, unsafe_allow_html=True)

df = pd.read_csv("Police.csv")

st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

mapa = pd.DataFrame()
mapa['Date']= df['Incident Date']
mapa['Day']= df['Incident Day of Week']
mapa['Police District']= df['Police District']
mapa['Neighborhood']= df['Analysis Neighborhood']
mapa['Incident Category']= df['Incident Category']
mapa['Incident Subcategory']= df['Incident Subcategory']
mapa['Resolution']= df['Resolution']
mapa['lat']= df['Latitude']
mapa['lon']= df['Longitude']
mapa = mapa.dropna()

subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist())

if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    mapa.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())

if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())

if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data

col1, col2 = st.columns(2)

with col1:
    st.markdown("Crimes ocurred per day of the week")
    st.bar_chart(subset_data['Day'].value_counts())

with col2:
    st.markdown("Crimes ocurred per date")
    st.line_chart(subset_data['Date'].value_counts())
        
st.header('') 

st.markdown("It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.")
st.markdown("Crime locations in San Francisco")
st.map(subset_data)
st.markdown('Type of crimes committed')
st.bar_chart(subset_data['Incident Category'].value_counts())

agree=st.button("Click to see Incident Subcategories")
if agree:
    st.markdown("Subtype of crimes commited")
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())
    
st.markdown("Resolution status")
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct = '%1.1f%%', startangle=20)
st.pyplot(fig1)

st.header("Heatmap")

fig = px.density_mapbox(subset_data, lat='lat', lon='lon', radius=10,
                                 center=dict(lat=subset_data['lat'].mean(), lon=subset_data['lon'].mean()),
                                 zoom=10, mapbox_style='carto-positron',
                                 title='Heat-map')
fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
st.plotly_chart(fig)

incidentesT = len(subset_data)
casos = len(subset_data[subset_data['Resolution'] == 'Open or Active'])

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div style="background-color:#081A41; padding: 10px; border-radius: 5px; text-align: center;">'
        f'<p style="color:white; font-size: 24px;">Cantidad de incidentes:                                   </p>'
        f'<div style="color:white; font-size: 32px;">\U0001F4C8<span>{incidentesT}</span></div>'
        '</div>',
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        f'<div style="background-color:#081A41; padding: 10px; border-radius: 5px; text-align: center;">'
        f'<p style="color:white; font-size: 24px;">Cantidad de casos activos:                                 </p>'
        f'<div style="color:white; font-size: 32px;">\U0001F4C8<span>{casos}</span></div>'
        '</div>',
        unsafe_allow_html=True
    )
        
st.header('') 

st.header("Incidents by category")

fig = px.histogram(subset_data['Incident Category'].value_counts().reset_index(), 
                                   x='index', y='Incident Category', 
                                   title='Incidents by category')
fig.update_xaxes(title='Incidents')
fig.update_yaxes(title='Category')
fig.update_layout(width=800, height=600)
st.plotly_chart(fig)

st.header("Incidents per day of the week")

mapa['Color'] = '#081A41'

fig = px.bar(subset_data, x='Day', 
                         title='Incidents per day of the week',
                         category_orders={'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']})
fig.update_yaxes(title='Quantity')
fig.update_layout(width=800, height=600)
st.plotly_chart(fig)