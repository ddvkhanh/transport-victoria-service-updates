import streamlit as st
import altair as alt
import pandas as pd
from utils.db import run_query
import plotly.express as px

st.title("Historical Trends")
st.info("Historical counts include all recorded service impact records, so a single disruption may be counted more than once where separate impacts are recorded for different travel directions.")

# Chart 1: Distribution of Disruption Effects
st.subheader("Most Common Disruption Effects")

effects_sql = """
    SELECT frequency, effect   
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.distribution_of_disruption_effects`
"""
with st.spinner("Loading disruption effects…"):
    effects_df = pd.DataFrame(run_query(effects_sql))

effects_df = effects_df.rename(columns={
    "frequency": "Frequency",
    "effect": "Disruption Effect"
})

if not effects_df.empty:
    fig_effects = px.pie(
    effects_df,
    names="Disruption Effect",
    values="Frequency",
    )

    st.plotly_chart(fig_effects, width="stretch")
else:
    st.info("No disruption effect data available.")

# Chart 2: Top Disruption Causes
st.subheader("Top Disruption Causes")

causes_sql = """
    SELECT frequency, cause
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.distribution_of_disruption_causes`
"""

with st.spinner("Loading disruption causes…"):
    causes_df = pd.DataFrame(run_query(causes_sql))
    
causes_df = causes_df.rename(columns={
    "frequency": "Frequency",
    "cause": "Disruption Cause"
})

if not causes_df.empty:
    fig_causes = px.bar(
        causes_df,
        x="Disruption Cause",
        y="Frequency"
    )
    st.plotly_chart(fig_causes, width="stretch")
else:
    st.info("No disruption cause data available.")

#Chart 3: Disruptions Over Time
st.subheader("Disruptions Over Time")

disruptions_over_time_sql = """
    SELECT
        disruption_date,
        cause,
        disruption_count
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.distribution_of_disruptions_over_time`
    ORDER BY disruption_date
"""

with st.spinner("Loading disruption history…"):
    rows = run_query(disruptions_over_time_sql)

if rows:
    df = pd.DataFrame(rows)
    df["disruption_date"] = pd.to_datetime(df["disruption_date"]).dt.date

    min_date = df["disruption_date"].min()
    max_date = df["disruption_date"].max()

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
    end_date = col2.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

    if start_date > end_date:
        st.warning("Start date must be earlier than or equal to end date.")
    else:
        filtered_df = df[
            (df["disruption_date"] >= start_date) &
            (df["disruption_date"] <= end_date)
        ]

        chart = (
            alt.Chart(filtered_df)
            .mark_bar()
            .encode(
                x=alt.X("disruption_date:T", title="Date"),
                y=alt.Y("disruption_count:Q", title="Number of Disruptions"),
                color=alt.Color("cause:N", title="Cause"),
                tooltip=[
                    alt.Tooltip("disruption_date:T", title="Date"),
                    alt.Tooltip("cause:N", title="Cause"),
                    alt.Tooltip("disruption_count:Q", title="Disruptions"),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(chart, use_container_width=True)
else:
    st.info("No historical disruption data available.")

#Chart 4: Top 5 Impacted Routes
st.subheader("Top 5 Impacted Routes Over Time")

impacted_routes_over_time_sql = """
    SELECT route_id, route_short_name, disruption_count
    FROM `ptv-metro-service-updates.ptv_metro_dataset_marts.ranked_impacted_routes_over_time`
"""

impacted_routes_rows = run_query(impacted_routes_over_time_sql)

if (impacted_routes_rows):
    impacted_routes_df = pd.DataFrame(impacted_routes_rows)

    impacted_routes_df = impacted_routes_df.rename(columns={
        "route_id": "Route ID",
        "route_short_name": "Route Short Name",
        "disruption_count": "Number of Disruptions"
    })

    st.dataframe(impacted_df, width="stretch", hide_index=True)
else:
    st.info("No impacted route data available.")