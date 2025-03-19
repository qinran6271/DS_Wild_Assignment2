import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 加载数据（请确保 weather.csv 文件存在且包含所需的列，例如 'time' 和 'Ktemp'）
df = pd.read_csv("weather.csv")

# 2. 将时间列转换为 datetime 类型
df['time'] = pd.to_datetime(df['time'])

# 3. 将温度从 Kelvin 转换为 Fahrenheit
df['Ftemp'] = (df['Ktemp'] - 273.15) * (9/5) + 32

# 4. 提取年份和月份
df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month

# 5. 计算每年每月的平均温度
monthly_avg = df.groupby(['year', 'month'])['Ftemp'].mean().reset_index()

# 6. Streamlit 应用程序标题
st.title('每月平均温度（°F）')

# 7. 添加年份选择滑块（注意：默认选择最小年份）
years = monthly_avg['year'].unique()
selected_year = st.slider('选择年份', int(years.min()), int(years.max()), int(years.min()), step=1)

# 8. 筛选数据
filtered_data = monthly_avg[monthly_avg['year'] == selected_year]

# 9. 使用 Plotly 绘制折线图
fig = px.line(
    filtered_data,
    x='month',
    y='Ftemp',
    title=f'{selected_year} 年每月平均温度（°F）',
    labels={'month': '月份', 'Ftemp': '平均温度（°F）'}
)

# 10. 调整 x 轴显示，使得月份显示为 1 到 12
fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)

# 11. 在 Streamlit 中显示图表（支持鼠标悬停、缩放、拖拽等交互操作）
st.plotly_chart(fig)

# 12. 保存为包含 Plotly.js 的完整 HTML 文件（交互功能保留）
html_filename = "plot.html"
fig.write_html(html_filename, full_html=True, include_plotlyjs="cdn")

# 13. 提供下载 HTML 文件的按钮
with open(html_filename, "rb") as file:
    st.download_button("下载 HTML 文件", data=file, file_name=html_filename, mime="text/html")
