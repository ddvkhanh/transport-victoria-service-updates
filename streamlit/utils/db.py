#dummy file to test connection to BigQuery

from typing import Any, Sequence
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from google.api_core import exceptions as gcp_exceptions


# Create API client. Ensures the client is built once and shared across reruns and sessions instead of being rebuilt on every import.
@st.cache_resource
def get_bq_client():
     credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
     client = bigquery.Client(credentials=credentials)
     return client



# Run a parameterized BigQuery query and return rows as a list of dicts.
@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql, params=None):   
    client = get_bq_client()

    bq_params = []
    for name, bq_type, value in params or ():
        if isinstance(value, (list, tuple)):
            bq_params.append(bigquery.ArrayQueryParameter(name, bq_type, list(value)))
        else:
            bq_params.append(bigquery.ScalarQueryParameter(name, bq_type, value))

    job_config = bigquery.QueryJobConfig(query_parameters=bq_params)

    try:
        job = client.query(sql, job_config=job_config)
        return [dict(row) for row in job.result()]
    except gcp_exceptions.GoogleAPIError as err:
        st.error(f"BigQuery query failed: {err}")
        return []