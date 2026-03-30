# Kestra Orchestration

This directory contains the Kestra workflow configurations responsible for orchestrating the entire Transport Victoria Service Updates data pipeline.

The primary flow is defined in `ingest_data.yml` which runs on a cron schedule every 15 minutes (`*/15 * * * *`).

## Pipeline Tasks Overview

The DAG executes the following major tasks in sequence:

### 1. `ingest_metro_updates`
This task fetches the latest GTFS Realtime alerts from the PTV API. Since Kestra executes tasks in isolated environments, it uses a generic Kestra Working Directory to first clone the master branch of this repository (`clone_ingest_repo`). It then kicks off a Python script (`python`) inside a lightweight Docker container, injecting the PTV API Key via Kestra Secrets, installing dependencies, and running `app/ingest_data.py` to output the alerts as a newline-delimited JSON (`.ndjson`) file.

A sample of this .ndjson is in the `output/` folder

### 2. `upload_to_gcs`
Once the python script is finished, this task takes the dynamically generated `.ndjson` output file from Kestra's internal storage and safely uploads it into your designated raw data folder inside Google Cloud Storage (Data Lake).

### 3. `load_to_bigquery`
Triggered immediately after the successful upload, this task instructs BigQuery to load the raw `.ndjson` data directly from the GCS bucket into the raw base table (`service_updates_metro`). It appends new records into the table without overriding historical data (`WRITE_APPEND`).

### 4. `dbt_transformation`
With the new raw data successfully appended to BigQuery, this task triggers the data modeling phase. It utilizes a Docker runner container equipped specifically with dbt (`ghcr.io/kestra-io/dbt-bigquery:latest`). 
It passes in your GCP Service Account credentials dynamically via Kestra Secrets to generate the `creds.json` configuration file, resolves dbt dependencies, and successfully runs a `dbt build` on the entirety of the `ptv_metro_service_updates` dbt project.

### 5. `purge_files`
To ensure clean executions and save on internal storage space, this final clean-up task purges all temporary files (such as the `.ndjson` data file) from Kestra’s internal storage buffer. 

---
*Note: Ensure the required Kestra Key-Value pairs and Base64 Encoded Secrets are configured in your Kestra UI for the DAG to authenticate properly with GCP and PTV APIs.*
