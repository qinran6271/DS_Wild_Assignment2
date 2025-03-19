import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Load data (make sure that weather.csv exists and contains the columns 'time' and 'Ktemp')
df = pd.read_csv("weather.csv")

# 2. Convert the 'time' column to datetime type
df['time'] = pd.to_datetime(df['time'])

# 3. Convert temperature from Kelvin to Fahrenheit
df['Ftemp'] = (df['Ktemp'] - 273.15) * (9/5) + 32

# 4. Extract year and month from the 'time' column
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month

# 5. Calculate the average temperature for each month of each year and create a pivot table
pivot_temp = df.groupby(['year', 'month'])['Ftemp'].mean().reset_index()
pivot_table = pivot_temp.pivot(index='year', columns='month', values='Ftemp')

# 6. Set the title and description for the Streamlit app
st.title("Temperature Heatmap")
st.write("Heatmap showing the average temperature (°F) by month and year.")

# 7. Create a heatmap using Plotly
fig = px.imshow(
    pivot_table,
    labels=dict(x="Month", y="Year", color="Avg Temp (°F)"),
    x=pivot_table.columns,
    y=pivot_table.index,
    aspect="auto",
    color_continuous_scale='RdYlBu_r'
)

st.plotly_chart(fig)
