import streamlit as st
import requests
import pandas as pd

st.title('21 days temperature forecast')

url = 'https://api.met.no/weatherapi/subseasonal/1.0/complete?lat=59.94&lon=10.72'

headers = {
  'User-Agent': 'Didrik R.',
  'From': 'didrik.roest@yahoo.com'
}

response = requests.get(url, headers=headers)

data = response.json()

timeseries = data['properties']['timeseries']

time = []
air_temperature_mean = []

for t in timeseries:
  time.append(t['time'])
  air_temperature_mean.append(t['data']['next_24_hours']['details']['air_temperature_mean'])


df = pd.DataFrame(list(zip(time, air_temperature_mean)), columns=['time', 'air_temperature_mean'])
df['time'] = pd.to_datetime(df['time']).dt.date

df = df.rename(columns={'time':'date'})

st.subheader('Data Preview')
st.write(df.head())
  
st.subheader('Data Summary')
st.write(df.describe())

st.subheader('Plot data')

st.line_chart(df.set_index('date')['air_temperature_mean'])