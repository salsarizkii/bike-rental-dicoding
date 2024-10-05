import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# function ambil sum_weather_count
def sum_weather_count_df(df):
    sum_weather_count = df.groupby(["weathersit"]).resample(rule='D', on='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    
    return sum_weather_count

# function ambil peak_per_hour
def peak_per_hour_df(df):
    peak_per_hour = df.groupby(["hr"]).resample(rule='D', on='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    
    return peak_per_hour

# ambil data yang sudah clean
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# sort by date
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

# mengubah tipe data dteday menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# filter date
day_min_date = day_df["dteday"].min()
day_max_date = day_df["dteday"].max()

hour_min_date = hour_df["dteday"].min()
hour_max_date = hour_df["dteday"].max()

with st.sidebar:
    # Menambahkan gambar
    st.image("https://avatars.githubusercontent.com/u/121892960?v=4")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=day_min_date,
        max_value=day_max_date,
        value=[day_min_date, day_max_date]
    )

day_main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

hour_main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

# ambil df
weather_count_df = sum_weather_count_df(day_main_df)
peak_hour_df = peak_per_hour_df(hour_main_df)

st.header('Bike Rentals Analytics Dashboard :sparkle:')

# tampilan grafik pengaruh cuaca
st.subheader("Weather Impact on Bike Rentals")

pivot_data_weather = weather_count_df.pivot(index='dteday', columns='weathersit', values='cnt')

fig, ax = plt.subplots(figsize=(16, 8))
for col in pivot_data_weather.columns:
    ax.plot(pivot_data_weather.index, pivot_data_weather[col], label=f'Cuaca {col}')

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# tampilan grafik peak per hari
st.subheader("Peak Bike Rentals per Day")

fig, ax = plt.subplots(figsize=(16, 8))

for date in peak_hour_df['dteday'].unique():
    daily_data = peak_hour_df[peak_hour_df['dteday'] == date]
    ax.plot(daily_data['hr'], daily_data['cnt'], marker='o', label=date)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xticks(range(24))

st.pyplot(fig)