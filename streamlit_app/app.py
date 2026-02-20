import streamlit as st
import pandas as pd

st.title("Spain Top 50 – Song Lifecycle Analytics")

# Load data
lifecycle = pd.read_csv("final_lifecycle_dataset.csv")

st.sidebar.header("Filters")

# Explicit filter
explicit_filter = st.sidebar.selectbox(
    "Explicit Content",
    ["All", "Explicit Only", "Clean Only"]
)

# Album type filter
album_filter = st.sidebar.selectbox(
    "Album Type",
    ["All", "Single", "Album"]
)

filtered_data = lifecycle.copy()

# Apply explicit filter
if explicit_filter == "Explicit Only":
    filtered_data = filtered_data[filtered_data['is_explicit'] == True]
elif explicit_filter == "Clean Only":
    filtered_data = filtered_data[filtered_data['is_explicit'] == False]

# Apply album filter
if album_filter != "All":
    filtered_data = filtered_data[filtered_data['album_type'] == album_filter.lower()]

# KPIs
st.header("Key Metrics")

st.write("Total Songs:", filtered_data.shape[0])
st.write("Average Lifespan:", round(filtered_data['total_days'].mean(), 2))
st.write("Average Days to Peak:", round(filtered_data['days_to_peak'].mean(), 2))

# Lifecycle type distribution
st.header("Lifecycle Type Distribution")
st.bar_chart(filtered_data['lifecycle_type'].value_counts())

st.header("Song Lifecycle Explorer")

# Song dropdown
selected_song = st.selectbox(
    "Select a song",
    filtered_data['song_id'].unique()

)

# Filter data
song_data = filtered_data[filtered_data['song_id'] == selected_song]

# Display details
st.write("Entry Date:", song_data['entry_date'].values[0])
st.write("Exit Date:", song_data['exit_date'].values[0])
st.write("Total Days on Playlist:", song_data['total_days'].values[0])
st.write("Peak Rank:", song_data['peak_rank'].values[0])
st.write("Days to Peak:", song_data['days_to_peak'].values[0])

st.header("Singles vs Albums – Average Lifespan")

avg_life = filtered_data.groupby('album_type')['total_days'].mean()
st.bar_chart(avg_life)

st.header("Explicit vs Clean – Average Lifespan")

avg_explicit = filtered_data.groupby('is_explicit')['total_days'].mean()
st.bar_chart(avg_explicit)

st.header("Top 10 Longest Surviving Songs")

top_long = filtered_data.sort_values('total_days', ascending=False).head(10)
st.dataframe(top_long[['song_id','total_days','peak_rank']])

st.header("Top 10 Fastest Rising Songs")

top_fast = filtered_data.sort_values('days_to_peak').head(10)
st.dataframe(top_fast[['song_id','days_to_peak','peak_rank']])

