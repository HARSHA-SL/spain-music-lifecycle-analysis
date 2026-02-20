import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Spain Top 50 Lifecycle Analytics",
    page_icon="🎵",
    layout="wide"
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------
st.title("🎵 Spain Top 50 – Song Lifecycle Analytics")
st.markdown("Analyze how songs enter, peak, and exit Spain’s Top 50 playlist.")

st.markdown("---")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("output/final_lifecycle_dataset.csv")

lifecycle = load_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("Filters")

explicit_filter = st.sidebar.selectbox(
    "Explicit Content",
    ["All", "Explicit Only", "Clean Only"]
)

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
    filtered_data = filtered_data[
        filtered_data['album_type'] == album_filter.lower()
    ]

# If no data after filtering
if filtered_data.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ---------------------------------------------------
# KPI Section
# ---------------------------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Songs", filtered_data.shape[0])
col2.metric("Average Lifespan (Days)", round(filtered_data['total_days'].mean(), 2))
col3.metric("Average Days to Peak", round(filtered_data['days_to_peak'].mean(), 2))

st.markdown("---")

# ---------------------------------------------------
# Lifecycle Distribution
# ---------------------------------------------------
st.subheader("Lifecycle Type Distribution")

lifecycle_counts = filtered_data['lifecycle_type'].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(lifecycle_counts)

with col2:
    st.write("### Distribution Summary")
    st.write(lifecycle_counts)

st.markdown("---")

# ---------------------------------------------------
# Song Explorer
# ---------------------------------------------------
st.subheader("🎧 Song Lifecycle Explorer")

selected_song = st.selectbox(
    "Select a Song",
    sorted(filtered_data['song_id'].unique())
)

song_data = filtered_data[filtered_data['song_id'] == selected_song]

col1, col2, col3 = st.columns(3)

col1.metric("Total Days", int(song_data['total_days'].values[0]))
col2.metric("Peak Rank", int(song_data['peak_rank'].values[0]))
col3.metric("Days to Peak", int(song_data['days_to_peak'].values[0]))

col4, col5 = st.columns(2)

col4.metric("Entry Date", song_data['entry_date'].values[0])
col5.metric("Exit Date", song_data['exit_date'].values[0])

st.markdown("---")

# ---------------------------------------------------
# Comparison Charts
# ---------------------------------------------------
st.subheader("📈 Performance Comparisons")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Singles vs Albums – Avg Lifespan")
    avg_life = filtered_data.groupby('album_type')['total_days'].mean()
    st.bar_chart(avg_life)

with col2:
    st.markdown("#### Explicit vs Clean – Avg Lifespan")
    avg_explicit = filtered_data.groupby('is_explicit')['total_days'].mean()
    st.bar_chart(avg_explicit)

st.markdown("---")

# ---------------------------------------------------
# Top Performers Section
# ---------------------------------------------------
st.subheader("🏆 Top Performers")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top 10 Longest Surviving Songs")
    top_long = filtered_data.sort_values(
        'total_days', ascending=False
    ).head(10)
    st.dataframe(top_long[['song_id','total_days','peak_rank']],
                 use_container_width=True)

with col2:
    st.markdown("#### Top 10 Fastest Rising Songs")
    top_fast = filtered_data.sort_values(
        'days_to_peak'
    ).head(10)
    st.dataframe(top_fast[['song_id','days_to_peak','peak_rank']],
                 use_container_width=True)

st.markdown("---")

st.caption("Built with Python & Streamlit | Lifecycle Analytics Project")
