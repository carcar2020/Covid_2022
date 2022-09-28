from xmlrpc.client import UNSUPPORTED_ENCODING
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date
import plotly.express as px 
import streamlit as st
from PIL import Image

# Importing image 
image = Image.open('arrow2.png')
image2 = Image.open('co19.png')

# ":bar_chart:"
st.set_page_config(page_title = " COVID-2022", page_icon = image2 , layout= "wide")


# better performance
@st.cache
def get_data_from_csv():

    df = pd.read_csv("COVIDdata8.csv")
    return df
df = get_data_from_csv()

    


# Removing Data that will not be used for analyzes.
df = df.drop(columns= ['WHO_region', 'Cumulative_cases', 'Cumulative_deaths' ])


# Converting column Date_reported into datetime data type.
df['Date_reported'] = pd.to_datetime(df['Date_reported'])

# Filtering the Data for 2022 Only.
nf = df[df['Date_reported'] >= '01-01-2022']

# Copied Dataframe and extracted the month to create a month column
da = nf.copy()
da['Month'] = da['Date_reported'].dt.month

da.rename(columns = {'New_cases': 'Total Cases', 'New_deaths': 'Total Deaths'}, inplace = True)


# Sidebar that lets you filter data by Country
st.sidebar.header("Filter Data Here:")

Country = st.sidebar.multiselect(
            "Select the Country:",  options = da['Country'].unique(), default = ['United States of America'] )

df_selection = da.query( "Country == @Country")


# MAINPAGE
st.title(":bar_chart: Covid-19 2022")
st.markdown("##")
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
                    """
    
st.markdown(hide_st_style, unsafe_allow_html = True) 
st.markdown("***")
total_covid19_p = 0
# TOP KPI'S 
total_covid19_cases = int(df_selection['Total Cases'].sum())
total_covid19_deaths = int(df_selection['Total Deaths'].sum())
if total_covid19_cases and total_covid19_deaths != 0:
   total_covid19_p = float((total_covid19_deaths / total_covid19_cases) *100 )


   left_column, middle_column, right_column, right_column2 = st.columns(4)
   with left_column:
    st.subheader("Total Cases:")
    st.subheader(f"{total_covid19_cases:,}")
   with middle_column:
    st.subheader("Total Deaths")
    st.subheader(f"{total_covid19_deaths:,}")
   with right_column:
    st.subheader("Death Rate")
    if total_covid19_p != 0:
        st.subheader("{:.3f}%".format(total_covid19_p))
    else:
        st.subheader(f"0")
    with right_column2:
        st.subheader("Updated")
        st.subheader(f"9-24-2022")



   #Total Covid-19 Cases by Month [BarChart]

    totalcovid19_cases_by_month = (df_selection.groupby(by='Month').sum()[['Total Cases']].sort_values(by='Month')
    )

    totalcovid19_cases_by_month.rename(index={1: 'January', 2: 'February', 3: 'March', 4:'April', 5:'May', 6:'June', 7:'July', 8: 'August', 9: 'September'}, inplace = True)
    
    fig_month_total = px.bar ( totalcovid19_cases_by_month, x = totalcovid19_cases_by_month.index, y= 'Total Cases', 
                          title= "<b>Total Covid Cases By Month</b>", 
                          color_discrete_sequence= ["#95A5A6"] * len(totalcovid19_cases_by_month),text_auto='.2s' ,  
                          template = "plotly_white") 

    fig_month_total.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
    fig_month_total.update_layout( plot_bgcolor = "rgb(205, 97, 85)", yaxis = (dict(showgrid=False)), xaxis = dict(tickmode="linear") )

    
    
    #Total Covid-19 Cases by Month [Line Chart]
    fig_month_total_lineplot = px.line(totalcovid19_cases_by_month, x = totalcovid19_cases_by_month.index, y= 'Total Cases',
                                       title = '<b>Covid Cases Trend</b>')
    
    fig_month_total.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
    fig_month_total_lineplot.update_layout( plot_bgcolor = "rgb(205, 97, 85)", yaxis = (dict(showgrid=False)), xaxis = dict(tickmode="linear") )
    
    
    
    # Covid Deaths by month [Barchart]
   Deaths_by_month = df_selection.groupby(by='Month').sum()[['Total Deaths']].sort_values(by='Month')
   
   Deaths_by_month.rename(index={1: 'January', 2: 'February', 3: 'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9: 'September'}, inplace = True)
   fig_Monthly_Death = px.bar( Deaths_by_month, x= Deaths_by_month.index, y= "Total Deaths",
   title = "<b>Deaths By Month</b>", color_discrete_sequence = ["#95A5A6"]* len(Deaths_by_month),
   template = "plotly_white", text_auto='.2s'
    
    )
   fig_Monthly_Death.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) 
   fig_Monthly_Death.update_layout(  xaxis = dict(tickmode="linear"), plot_bgcolor="rgb(205, 97, 85)",
                                yaxis= (dict(showgrid=False)), 
                                )


   left_column,middle_column, right_column = st.columns(3)



   left_column.plotly_chart(fig_month_total, use_container_width = True)
   right_column.plotly_chart(fig_month_total_lineplot, use_container_width = True)
   middle_column.plotly_chart(fig_Monthly_Death, use_container_width = True)

    
 

# needs better error handeling
else:
    st.header(" PLEASE SELECT A COUNTRY") 
    st.image(image, caption='')