import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Load data (make sure that the weather.csv file exists and contains the required columns, e.g., 'time' and 'Ktemp')
df = pd.read_csv("weather.csv")

# 2. Convert the 'time' column to datetime type
df['time'] = pd.to_datetime(df['time'])

# 3. Convert temperature from Kelvin to Fahrenheit
df['Ftemp'] = (df['Ktemp'] - 273.15) * (9/5) + 32

# 4. Extract year and month from the time column
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month

# 5. Calculate the average temperature for each month of each year
monthly_avg = df.groupby(['year', 'month'])['Ftemp'].mean().reset_index()

# 6. Set the title for the Streamlit app
st.title('Monthly Average Temperature (°F)')

# 7. Add a slider to select the year (default is the minimum year)
years = monthly_avg['year'].unique()
selected_year = st.slider('Select Year', int(years.min()), int(years.max()), int(years.min()), step=1)

# 8. Filter the data for the selected year
filtered_data = monthly_avg[monthly_avg['year'] == selected_year]

# 9. Create a line chart using Plotly
fig = px.line(
    filtered_data,
    x='month',
    y='Ftemp',
    title=f'Monthly Average Temperature (°F) in {selected_year}',
    labels={'month': 'Month', 'Ftemp': 'Average Temperature (°F)'}
)

# 10. Adjust the x-axis to display months from 1 to 12
fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)

# 11. Display the interactive chart in Streamlit (supports hover, zoom, drag, etc.)
st.plotly_chart(fig)

# 12. Save the chart as a complete HTML file with Plotly.js (interactive features are retained)
html_filename = "plot.html"
fig.write_html(html_filename, full_html=True, include_plotlyjs="cdn")

# 13. Provide a download button for the HTML file
with open(html_filename, "rb") as file:
    st.download_button("Download HTML File", data=file, file_name=html_filename, mime="text/html")
