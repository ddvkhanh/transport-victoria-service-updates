import streamlit as st

from utils.db import run_query
st.title("Historical Trends")

# Chart 1: Distribution of Disruption Effects
st.subheader("Most Common Disruption Effects")

effects_sql = """
    SELECT frequency, effect   
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.distribution_of_disruption_effects`
"""
effects_df = run_query(effects_sql)

st.bar_chart(
    effects_df,
    x="effect",
    y="frequency",
    x_label="Effect of Disruption",
    y_label="Frequency",
    horizontal=True,
    width="stretch"
)

# Chart 2: Top Disruption Causes
st.subheader("Top Disruption Causes")

causes_sql = """
    SELECT frequency, cause
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.distribution_of_disruption_causes`
"""
causes_df = run_query(causes_sql)

st.bar_chart(
    causes_df,
    x="cause",
    y="frequency",
    x_label="Cause of Disruption",
    y_label="Frequency",
    horizontal=True,
    width="stretch"
)

#Chart 3: Disruptions Over Time
st.subheader("Disruptions Over Time")
disruptions_over_time_sql = """
    SELECT disruption_date, cause, disruption_count
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.distribution_of_disruptions_over_time`
    LIMIT 1000
"""
disruptions_over_time_df = run_query(disruptions_over_time_sql)

st.line_chart(
    disruptions_over_time_df,
    x="disruption_date",
    y="disruption_count",
    color="cause",
    x_label="Date",
    y_label="Number of Disruptions",
    width="stretch"
)