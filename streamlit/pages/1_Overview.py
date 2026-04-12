import pandas as pd
import streamlit as st
from utils.db import run_query

st.title('Overview')

# Summary metrics
st.subheader('Current And Upcoming Disruptions')

metrics_sql = """
select
    count(*) as active_impacts,
    count(distinct route_id) as impacted_routes,
    count(distinct stop_id) as impacted_stops
from `ptv-metro-service-updates.ptv_metro_dataset_marts.current_service_disruptions`
"""
metrics_rows = run_query(metrics_sql)

metrics = metrics_rows[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Active Impacts",
    value=metrics["active_impacts"],
    border=True
)

col2.metric(
    label="Impacted Routes",
    value=metrics["impacted_routes"],
    border=True
)

col3.metric(
    label="Impacted Stops",
    value=metrics["impacted_stops"],
    border=True
)

# Map of current disruptions affecting stops
st.subheader("Map of Current Disruptions Affecting Stops")
map_sql = """
select distinct stop_name, stop_lat, stop_lon
from `ptv-metro-service-updates.ptv_metro_dataset_marts.current_service_disruptions`
where stop_lat is not null and stop_lon is not null
"""
map_rows = run_query(map_sql)

if map_rows:
    map_df = pd.DataFrame(map_rows)
    st.map(map_df, latitude="stop_lat", longitude="stop_lon", zoom=10)
