import pandas as pd
import streamlit as st
from utils.db import run_query

st.title("Active Disruptions")
st.info("This page provides a current operational view of disruptions by affected route and stop.")

st.subheader("Details of Current Disruptions")

route_input = st.text_input(
    "Route name",
    placeholder="Route name (e.g. 'Frankston')",
    icon=":material/search:"
).strip() or None

stop_input = st.text_input(
    "Stop name",
    placeholder="Stop name (e.g. 'Flinders Street')",
    icon=":material/search:"
).strip() or None

active_disruptions_sql = """
select
    route_short_name,
    stop_name,
    header_text,
    cause,
    effect,
    active_period_start,
    active_period_end,
    severity_level
from `ptv-metro-service-updates.ptv_metro_dataset_marts.current_route_stop_impacts`
where (@route is null or lower(route_short_name) like lower(concat('%', @route, '%')))
  and (@stop  is null or lower(stop_name)        like lower(concat('%', @stop,  '%')))
order by active_period_start desc
"""

params = (
    ("route", "STRING", route_input),
    ("stop",  "STRING", stop_input),
)
with st.spinner("Searching disruptions…"):
    disruptions_rows = run_query(active_disruptions_sql, params=params)

if disruptions_rows:
    disruptions_df = pd.DataFrame(disruptions_rows)

    disruptions_df = disruptions_df.rename(columns={
        "route_short_name": "Route Name",
        "stop_name": "Stop Name",
        "header_text": "Description",
        "cause": "Cause",
        "effect": "Effect",
        "active_period_start": "Start Time",
        "active_period_end": "End Time"
    })

    disruptions_df["Start Time"] = pd.to_datetime(disruptions_df["Start Time"]).dt.strftime("%d-%m-%Y %H:%M")
    disruptions_df["End Time"] = pd.to_datetime(disruptions_df["End Time"]).dt.strftime("%d-%m-%Y %H:%M")

    st.caption(f"Showing {len(disruptions_df)} disruption(s).")
    st.dataframe(disruptions_df, width="stretch", hide_index=True)
else:
    st.info("No active disruptions found.")