import streamlit as st
import pandas as pd
import snowflake.connector as sf
import altair as alt
import plotly.express as px

# Connect to Snowflake
conn = sf.connect(user='AMANISOUAI',
                  password='Vuc88589', 
                  account='vh93549.eu-west-3.aws',
                  database='COVID',
                  schema='PUBLIC',
                  warehouse='COMPUTE_WH')
cur = conn.cursor()
def init():
#     if "wide_mode" not in st.session_state:
        st.set_page_config(layout="centered",page_title="Covid Dashboard",page_icon="chart_with_upwards_trend")
        # st.session_state.wide_mode = True
        st.header('Covid Dashboard')

# def start_app():
if __name__=="__main__":
    try:
        init()
        # headers = _get_websocket_headers()
        # logging.info(headers)
        # token = headers.get("X-Auth-Request-Access-Token")
        # if token is None:
        #     st.write("Unauthorized Access!")
        # else:
        
    except Exception as e:
        st.write(e)


# Define the query to retrieve total case count by country
query = '''
        SELECT COUNTRY_REGION, SUM(CASES) AS CASES
        FROM ECDC_GLOBAL
        GROUP BY COUNTRY_REGION;
        '''

# Execute the query and store the results in a Pandas dataframe
df_cases = pd.read_sql(query, conn)

# Create a bar chart showing the total number of cases by country
fig_cases = px.bar(df_cases, x='COUNTRY_REGION', y='CASES', title='Total Cases by Country')
st.plotly_chart(fig_cases)

# Define the query to retrieve mobility data for Alexandria, Virginia
# query1 = '''
#         SELECT DATE,
#                PROVINCE_STATE,
#                GROCERY_AND_PHARMACY_CHANGE_PERC,
#                PARKS_CHANGE_PERC,
#                RESIDENTIAL_CHANGE_PERC,
#                RETAIL_AND_RECREATION_CHANGE_PERC,
#                TRANSIT_STATIONS_CHANGE_PERC,
#                WORKPLACES_CHANGE_PERC
#         FROM GOOG_GLOBAL_MOBILITY_REPORT
#         WHERE COUNTRY_REGION = 'United States'
#             AND PROVINCE_STATE = 'Virginia'
#             AND SUB_REGION_2 = 'Alexandria';
#         '''

# # Execute the query and store the results in a Pandas dataframe
# df_mobility = pd.read_sql(query1, conn)

# # Melt the dataframe to transform it into long format for plotting
# df_mobility_melt = pd.melt(df_mobility, id_vars=['DATE', 'PROVINCE_STATE'], var_name='Location Type', value_name='Change Percentage')

# # Create a line chart showing the change in mobility over time in Alexandria, Virginia
# fig_mobility = px.line(df_mobility_melt, x='DATE', y='Change Percentage', color='Location Type', title='Change in Mobility over Time in Alexandria, Virginia')
# st.plotly_chart(fig_mobility)

# Define the query to retrieve mobility data for Alexandria, Virginia
query2 = '''
        SELECT DATE,
               PROVINCE_STATE,
               GROCERY_AND_PHARMACY_CHANGE_PERC,
               PARKS_CHANGE_PERC,
               RESIDENTIAL_CHANGE_PERC,
               RETAIL_AND_RECREATION_CHANGE_PERC,
               TRANSIT_STATIONS_CHANGE_PERC,
               WORKPLACES_CHANGE_PERC
        FROM GOOG_GLOBAL_MOBILITY_REPORT
        WHERE COUNTRY_REGION = 'United States'
            AND PROVINCE_STATE = 'Virginia'
            AND SUB_REGION_2 = 'Alexandria';
        '''

# Execute the query and store the results in a Pandas dataframe
df_mobility = pd.read_sql(query2, conn)

# Melt the dataframe to transform it into long format for plotting
df_mobility_melt = pd.melt(df_mobility, id_vars=['DATE', 'PROVINCE_STATE'], var_name='Location Type', value_name='Change Percentage')

# Create a line chart showing the change in mobility over time in Alexandria, Virginia
fig_mobility = px.line(df_mobility_melt, x='DATE', y='Change Percentage', color='Location Type', title='Change in Mobility over Time in Alexandria, Virginia')
st.plotly_chart(fig_mobility)





# Query the data
query5 = '''
SELECT DATE, COUNTRY_REGION, SUM(CASES) AS CASES
FROM ECDC_GLOBAL
GROUP BY DATE, COUNTRY_REGION
'''
df = pd.read_sql(query5, conn)

# Create the chart
fig = px.line(df, x='DATE', y='CASES', color='COUNTRY_REGION',
              title='New Cases by Date and Country')
st.plotly_chart(fig)

###################################################### 

