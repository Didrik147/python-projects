import streamlit as st
import requests
import pandas as pd

st.title('21 days temperature forecast')

url = 'https://api.met.no/weatherapi/subseasonal/1.0/complete?lat=59.94&lon=10.72'

headers = {
  'User-Agent': st.secrets["user_agent"],
  'From': st.secrets["from"]
}

response = requests.get(url, headers=headers)
data = response.json()

timeseries = data['properties']['timeseries']

time = []
air_temperature_mean = []
air_temperature_min = []
air_temperature_max = []

for t in timeseries:
  time.append(t['time'])
  air_temperature_mean.append(t['data']['next_24_hours']['details']['air_temperature_mean'])
  air_temperature_min.append(t['data']['next_24_hours']['details']['air_temperature_min'])
  air_temperature_max.append(t['data']['next_24_hours']['details']['air_temperature_max'])


df = pd.DataFrame(list(zip(
  time, air_temperature_mean, air_temperature_min, air_temperature_max
  )), columns=['time', 'air_temperature_mean', 'air_temperature_min', 'air_temperature_max'])

df['time'] = pd.to_datetime(df['time']).dt.date
df = df.rename(columns={'time':'date'})
df = df.set_index('date')

st.header('Oslo - Blindern')

st.subheader('Data Preview')
st.write(df.head())
  
st.subheader('Data Summary')
st.write(df.describe())

st.subheader('Plot data')

#st.line_chart(df.set_index('date')['air_temperature_mean'])
st.line_chart(
  df,
  color=['#0f0', '#66f', '#f22'],
  x_label='Date',
  y_label = 'Temperature (°C)',
)