import streamlit as st
import pandas as pd

df_day_cleaned = pd.read_csv('day.csv')
df_day_cleaned['dteday'] = pd.to_datetime(df_day_cleaned['dteday'])


def get_season(month):
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'autumn'
    else:
        return 'unknown'


df_day_cleaned['season'] = df_day_cleaned['dteday'].dt.month.apply(get_season)


st.title("Bike Rental Dashboard")


min_date = df_day_cleaned['dteday'].min()
max_date = df_day_cleaned['dteday'].max()
start_date, end_date = st.date_input("Select Date Range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))


df_filtered = df_day_cleaned[(df_day_cleaned['dteday'] >= pd.to_datetime(start_date)) & (df_day_cleaned['dteday'] <= pd.to_datetime(end_date))]


total_bikes = df_filtered['cnt'].sum()
st.metric(label="Total Bikes Rented", value=total_bikes)


season_counts = df_filtered.groupby('season')['cnt'].sum()


st.subheader("Total Renters per Season")
st.bar_chart(season_counts)


for season, count in season_counts.items():
    st.write(f"{season.capitalize()}: {count} bikes rented")
