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
from `ptv-metro-service-updates.ptv_metro_dataset_marts.current_route_stop_impacts`
"""
metrics_rows = run_query(metrics_sql)

metrics = metrics_rows[0]
col2, col3 = st.columns(2)


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
st.info("This map shows the locations of stops currently affected by service disruptions. The color of the marker corresponds to the route color of the impacted route.")

map_sql = """
select distinct stop_name, stop_lat, stop_lon, concat('#', route_color) as route_color
from `ptv-metro-service-updates.ptv_metro_dataset_marts.current_route_stop_impacts`
where stop_lat is not null and stop_lon is not null
"""
map_rows = run_query(map_sql)

if map_rows:
    map_df = pd.DataFrame(map_rows)
    st.map(map_df, latitude="stop_lat", longitude="stop_lon", color="route_color", zoom=10)
