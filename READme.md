
## Problem statement
This project builds an end-to-end data pipeline using the GTFS (General Transit Feed Specification) Realtime datasets for Metro Train, provided by the Victorian Department of Transport and Planning.
Public transport services are frequently impacted by disruptions such as maintenance works, traffic incidents, and special events. However, these disruptions are not always easy to analyze systematically over time.
The objective of this project is to ingest and process real-time service alert data to enable analysis of:

- the frequency of service disruptions,

- the types and impact of incidents on train operations,

- and how disruptions vary across different times of day.

The pipeline uses a micro-batch ingestion approach, where data is retrieved from the API every 15 minutes. This design enables near real-time visibility while maintaining a simpler and more cost-effective architecture compared to full streaming solutions.

## Tech stack 
- ***Docker*** for containerized local development and deployment consistency
- ***Google Cloud Platform (GCP)*** for cloud storage and analytics services
- ***Terraform*** for infrastructure provisioning and environment setup
- ***Kestra*** for workflow orchestration and scheduled micro-batch ingestion every 15 minutes
- ***dbt*** for data modeling, transformation, and analytical layer development
- ***Google Cloud Storage (GCS)*** as the raw data lake
- ***BigQuery*** as the analytical data warehouse
- ***Streamlit*** for dashboarding and interactive data exploration

## Project architecture
![Project architecture](./images/flowchart-infra.png)


## Steps
1. Ensure uv is installed, if not:
```
pip install uv
```
 
Then sync with the project's uv config using:
```
uv sync
```

2. Register an account with 
Follow `` to get API key
Create a file .env 
```
PTV_KEYID = <Your-API-Key>
```

3. GCP Setup
- Create a serviced account in GCP
- Grant the service account with permissions:
    - Storage Admin
    - BigQuery Admin

- Generate and download the JSON key file, store it in the root folder .gc/
- Set up local authentication with gcloud

3. Terraform setup
- 