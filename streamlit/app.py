import streamlit as st
# 1. import streamlit
# 2. set page config
# 3. define page objects
# 4. define navigation
# 5. render shared sidebar text
# 6. run selected page


st.set_page_config(
    page_title="Transport Victoria Service Updates - Metro",
    page_icon=":metro:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "https://github.com/ddvkhanh/transport-victoria-service-updates",
    }
)


pages = [
    st.Page("pages/1_Overview.py", title="Overview"),
    st.Page("pages/2_Active_Disruptions.py", title="Active Disruptions"),
    st.Page("pages/3_Historical_Trends.py", title="Historical Trends")
]

pg = st.navigation(pages)

with st.sidebar:
    st.markdown("## Transport Victoria Service Updates - Metro")
    st.markdown("This app provides insights into the current and historical service disruptions in the Melbourne metro area. Use the navigation menu to explore different aspects of the data.")
    
pg.run()


# st.map(filtered_data)

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache_data)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)