import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
import os.path

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set page title:
st.set_page_config( page_title='Cocoa Bean Import'
                  , page_icon=':chocolate_bar:'
                  , layout='wide'
                  )


# Load data:
@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.read_csv(path)
    return data

imp = load_data('cocoa_import.csv')

imp_geo = imp.groupby(['Geo', 'Year']).sum().reset_index()
imp_geo['YoY (% change)'] = imp_geo.groupby(['Geo'])['Tonnes'].pct_change()*100
imp_geo['World %'] = imp_geo['Tonnes']/imp_geo.groupby('Year')['Tonnes'].transform('sum')*100

europe = imp_geo[imp_geo.Geo == 'Europe']
asia = imp_geo[imp_geo.Geo == 'Asia & Oceania']
america = imp_geo[imp_geo.Geo == 'Americas']

# Load cocoa bean image:
cocoa_bean = Image.open(os.path.join('images', 'cocoa_beans.png'))

#------------------------------------------------------------------ SIDEBAR ------------------------------------------------------------------

# Cocoa bean image:
st.sidebar.image(cocoa_bean, use_column_width=True)

# Year slider:
year = st.sidebar.slider('Select Year:', min_value=2017, max_value=2021, value=2021, step=1)


#---------------------------------------------------------------- MAIN PAGE -----------------------------------------------------------------

# Page title:
st.title('COCOA BEAN IMPORT')
st.markdown('##')

# Define KPI's % of all cocoa beans imports by year:
eu_kpi = europe.query('Year==@year')
kpi_europe = round(eu_kpi['World %'],2).to_string(index=False)

ao_kpi = asia.query('Year==@year')
kpi_asia = round(ao_kpi['World %'],2).to_string(index=False)

am_kpi = america.query('Year==@year')
kpi_america = round(am_kpi['World %'],2).to_string(index=False)


st.write("Europe is the world's largest importer of cocoa beans. It accounts for", kpi_europe, "% of total global import in", str(year), "making it the world's largest cocoa bean importer.")
st.write("Europes diverse market of processing and manufacturing as well as an increasing demand for specialty chocolates means Europe will remain a top importer for the foreseeable future.")

# Display KPI(s):
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown('#### Europe')
    st.markdown(f"{kpi_europe}%")
with middle_column:
    st.markdown('#### Asia & Oceania')
    st.markdown(f"{kpi_asia}%")
with right_column:
    st.markdown('#### Americas')
    st.markdown(f"{kpi_america}%")

st.markdown('##')
st.write("Charts below provide an overview of year on year percentage change of cocoa bean imports and total tonnes of this commodity imported by year and geographical area.")

# Define YoY (% change) bar for Europe:
yoy_eu = px.bar(europe, y='YoY (% change)', x='Year', height=300)
yoy_eu.update_traces(marker_color=['#BDA5AC' if i<=0 else '#2D7DB6' for i in europe['YoY (% change)']], showlegend=False)
yoy_eu.update_yaxes(title=None, range=[-20,30])
yoy_eu.update_xaxes(title=None)
yoy_eu.update_layout( margin=dict(r=0, l=0, t=0))

# Define YoY (% change) bar for Asia & Oceania:
yoy_ao = px.bar(asia, y='YoY (% change)', x='Year', height=300)
yoy_ao.update_traces(marker_color=['#BDA5AC' if i<=0 else '#2D7DB6' for i in asia['YoY (% change)']], showlegend=False)
yoy_ao.update_yaxes(title=None, range=[-20,30])
yoy_ao.update_xaxes(title=None)
yoy_ao.update_layout( margin=dict(r=0, l=0, t=0))

# Define YoY (% change) bar for Americas:
yoy_am = px.bar(america, y='YoY (% change)', x='Year', height=300)
yoy_am.update_traces(marker_color=['#BDA5AC' if i<=0 else '#2D7DB6' for i in america['YoY (% change)']], showlegend=False)
yoy_am.update_yaxes(title=None, range=[-20,30])
yoy_am.update_xaxes(title=None)
yoy_am.update_layout( margin=dict(r=0, l=0, t=0))

# Display YoY (% change) charts:
left_column, middle_column, right_column=st.columns(3)
left_column.plotly_chart(yoy_eu, use_container_width=True)
middle_column.plotly_chart(yoy_ao, use_container_width=True)
right_column.plotly_chart(yoy_am, use_container_width=True)


# Define area chart for Europe:
eu_line = px.area(europe, x="Year", y='Tonnes', width = 600, markers=True)
eu_line.update_traces(marker_color='#2D7DB6', showlegend=False)
eu_line.update_yaxes(title=None)
eu_line.update_xaxes(title=None)
eu_line.update_layout( margin=dict(r=0, l=0, t=0))

# Define area chart for Asia & Oceania:
ao_line = px.area(asia, x="Year", y='Tonnes', width = 600, markers=True)
ao_line.update_traces(marker_color='#2D7DB6', showlegend=False)
ao_line.update_yaxes(title=None)
ao_line.update_xaxes(title=None)
ao_line.update_layout( margin=dict(r=0, l=0, t=0))

# Define area chart for Americas:
am_line = px.area(america, x="Year", y='Tonnes',color="Geo", width = 600, markers=True)
am_line.update_traces(marker_color='#2D7DB6', showlegend=False)
am_line.update_yaxes(title=None)
am_line.update_xaxes(title=None)
am_line.update_layout( margin=dict(r=0, l=0, t=0))

# Display area charts:
left_column, middle_column, right_column=st.columns(3)
left_column.plotly_chart(eu_line, use_container_width=True)
middle_column.plotly_chart(ao_line, use_container_width=True)
right_column.plotly_chart(am_line, use_container_width=True)




eu_imp = imp.query("Geo=='Europe' & Year==@year")
ao_imp = imp.query("Geo=='Asia & Oceania' & Year==@year")
am_imp = imp.query("Geo=='Americas' & Year==@year")


st.write("What countries import the most cocoa bean? On countries level, in"
, str(year)
, "the largest importers for Europe, Asia & Oceania and Americas are:"
, eu_imp.Importers[(eu_imp.Tonnes == eu_imp.Tonnes.max()) & (eu_imp.Year==year)].to_string(index=False)
, ", "
, ao_imp.Importers[(ao_imp.Tonnes == ao_imp.Tonnes.max()) & (ao_imp.Year==year)].to_string(index=False)
, "and"
, am_imp.Importers[(am_imp.Tonnes == am_imp.Tonnes.max()) & (am_imp.Year==year)].to_string(index=False)
, "respectively. Top importers are static per geography throuhtout the last five years captured.")

#Europe treemap for Europe:
tree_eu = px.treemap(eu_imp, path=["Importers"], values="Tonnes"
                 , color_discrete_sequence=['#2D7DB6', '#009EC9', '#00BDC3', '#26D7A8', '#9BEC86', '#F9F871']
                )
tree_eu.update_layout( margin=dict(r=7, l=20, t=0))
#tree_eu.palette = ['red', 'green', 'blue'];


#Europe treemap for  Asia & Oceania:
tree_ao = px.treemap(ao_imp, path=["Importers"], values="Tonnes"
                    , color_discrete_sequence=['#2D7DB6', '#009EC9', '#00BDC3', '#26D7A8', '#9BEC86', '#F9F871']
                    )

tree_ao.update_layout( margin=dict(r=7, l=20, t=0))

#Europe treemap for Americas:
tree_am = px.treemap(am_imp, path=["Importers"], values="Tonnes"
                    , color_discrete_sequence=['#2D7DB6', '#009EC9', '#00BDC3', '#26D7A8', '#9BEC86', '#F9F871']
                    )
tree_am.update_layout( margin=dict(r=7, l=20, t=0))

# Display treemap charts:
left_column, middle_column, right_column=st.columns(3)
left_column.plotly_chart(tree_eu, use_container_width=True)
middle_column.plotly_chart(tree_ao, use_container_width=True)
right_column.plotly_chart(tree_am, use_container_width=True)





# Display Select boxes:
left_column, middle_column, right_column = st.columns(3)
with left_column:
    eu_select = st.multiselect('Select European Country:'
                                    , options=eu_imp['Importers'].unique()
                                    , default=eu_imp.Importers[eu_imp.Tonnes == eu_imp.Tonnes.max()]
                                    )
with middle_column:

    ao_select = st.multiselect('Select Asian/Oceanian Country:'
                                    , options=ao_imp['Importers'].unique()
                                    , default=ao_imp.Importers[ao_imp.Tonnes == ao_imp.Tonnes.max()]
                                    )

with right_column:
    am_select = st.multiselect('Select American Country:'
                                    , options=am_imp['Importers'].unique()
                                    , default=am_imp.Importers[am_imp.Tonnes == am_imp.Tonnes.max()]
                                    )


# Bar charts:
eu_impbar = imp.query("Geo=='Europe' & Importers==@eu_select")

eu_bar = px.bar(eu_impbar, x='Year', y='Tonnes', )
eu_bar.update_yaxes(title=None)
eu_bar.update_xaxes(title=None)
eu_bar.update_layout( margin=dict(r=0, l=0, t=0))
eu_bar.update_traces(marker_color=['#F9F871' if i<0 else '#2D7DB6' for i in eu_impbar['Tonnes']], showlegend=False)

ao_impbar = imp.query("Geo=='Asia & Oceania' & Importers==@ao_select")

ao_bar = px.bar(ao_impbar, x='Year', y='Tonnes')
ao_bar.update_yaxes(title=None)
ao_bar.update_xaxes(title=None)
ao_bar.update_layout( margin=dict(r=0, l=0, t=0))
ao_bar.update_traces(marker_color=['#F9F871' if i<0 else '#2D7DB6' for i in ao_impbar['Tonnes']], showlegend=False)

am_impbar = imp.query("Geo=='Americas' & Importers==@am_select")

am_bar = px.bar(am_impbar, x='Year', y='Tonnes', )
am_bar.update_yaxes(title=None)
am_bar.update_xaxes(title=None)
am_bar.update_layout( margin=dict(r=0, l=0, t=0))
am_bar.update_traces(marker_color=['#F9F871' if i<0 else '#2D7DB6' for i in am_impbar['Tonnes']], showlegend=False)

# Display bar charts:
left_column, middle_column, right_column=st.columns(3)
left_column.plotly_chart(eu_bar, use_container_width=True)
middle_column.plotly_chart(ao_bar, use_container_width=True)
right_column.plotly_chart(am_bar, use_container_width=True)
