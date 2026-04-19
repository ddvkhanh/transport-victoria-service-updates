import streamlit as st

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