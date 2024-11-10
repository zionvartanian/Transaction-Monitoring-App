import altair as alt
import pandas as pd
import streamlit as st
import datetime
from datetime import datetime 
from datetime import date,timedelta
import matplotlib.pyplot as plt


st.set_page_config(page_title="Charts", page_icon="📈")

st.title("Chart Creator")

st.write("Since the example CSV was made in 2023, if you are trying this app out make sure to look at the dates in the CSV to appropriately select for the ranges so graphs show up. If you just want to see how it works, select January 1st 2023 - Janurary 31st 2023.")


PaymentStatus = st.selectbox(
    'What Payment Status',
    ('All', 'Charge', 'Refund', 'Chargeback')
)

PaymentMethod = st.selectbox(
    'What Payment Method',
    ('All', 'Goods and Service', 'Friends and Family')
)

PaymentApplication = st.selectbox(
    'What Payment Application',
    ('All', 'Desktop', 'Tablet', 'Phone')
)

PaymentCountry = st.selectbox(
    'What Payment Country',
    ('All', 'US', 'UK', 'AU')
)

today = datetime.now()
days180 = date.today() - timedelta(days=180)

StartDate = st.date_input("Start Date (Default 180 Days Prior)", days180)
EndDate = st.date_input("End Date (Default 180 Days Prior)", today)

dfpreclean = st.file_uploader("Select CSV File")

if dfpreclean is not None:
    dfpreclean = pd.read_csv(dfpreclean)
else:
    st.stop()


dfpreclean.drop(['Transaction_ID','Auth_code'], axis=1, inplace=True)
dfpreclean2 = dfpreclean[dfpreclean['Success'] == 1]
dfpreclean2["Transaction_Notes"].fillna("N/A", inplace = True)
dfpreclean2['Day'] = pd.to_datetime(dfpreclean2['Day'])
df = dfpreclean2.loc[:,['Total', 'Transaction_Type', 'Type', 'Country', 'Source','Day', 'Customer_Name', 'Transaction_Notes']]

df['int_created_date'] = df['Day'].dt.year * 100 + df['Day'].dt.month


PaymentStatus

if PaymentStatus == 'Charge':
    df = df[df['Type']=='Charge']
elif PaymentStatus == 'Refund':
    df = df[df['Type']=='Refund']
elif PaymentStatus == 'Chargeback':
    df = df[df['Type']== 'Chargeback']
else:
    pass


if PaymentMethod == 'Goods and Service':
    df = df[df['Transaction_Type']=='Goods and Service']
elif PaymentMethod == 'Friends & Family':
    df = df[df['Transaction_Type']=='Friends & Family']
else:
    pass


if PaymentApplication == 'Desktop':
    df = df[df['Source']=='Desktop']
elif PaymentApplication == 'Tablet':
    df = df[df['Source']=='Tablet']
elif PaymentApplication == 'Phone':
    df = df[df['Source']== 'Phone']
else:
    pass


if PaymentCountry == 'US':
    df = df[df['Country'] == 'US']
elif PaymentCountry == 'UK':
    df = df[df['Country'] == 'UK']
elif PaymentCountry == 'AU':
    df = df[df['Country'] == 'AU']
else:
    pass

StartDate = pd.to_datetime(StartDate)
EndDate = pd.to_datetime(EndDate)

df = df[(df['Day'] >= StartDate) & (df['Day'] <= EndDate)]


StartDate = pd.to_datetime(StartDate)
EndDate = pd.to_datetime(EndDate)

df = df[(df['Day'] >= StartDate)&(df['Day'] <= EndDate)]

chart1 = alt.Chart(df).mark_bar().encode(
    alt.X("Total:Q", bin=True),
    y='count()',
).properties(
    title={
      "text": ["Count of Transactions"], 
      "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)

chart2 = alt.Chart(df).mark_boxplot(extent='min-max').encode(
    x='int_created_date:O',
    y='Total:Q'
).properties(
    title={
      "text": ["Box & Whisker By Month"], 
      "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)


bar3 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('sum(Total):Q', title='Total'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart3 = (bar3).properties(
    title={
        "text": ["Box Plot Mean Transaction Per Month"], 
        "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)

bar4 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('count(Total):Q', title='Count'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart4 = (bar4).properties(
    title={
      "text": ["Box Plot Transaction Count Per Month"], 
      "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)

tab1, tab2, tab3, tab4 = st.tabs(["Histogram", "Box/Whisker", "Box Plot Sum", "Box Plot Count"])

with tab1:
    st.altair_chart(chart1, use_container_width=True)

with tab2:
    st.altair_chart(chart2, use_container_width=True)

with tab3:
    st.altair_chart(chart3, use_container_width=True)

with tab4:
    st.altair_chart(chart4, use_container_width=True)

