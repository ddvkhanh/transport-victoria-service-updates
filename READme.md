
## Project statement
This project builds an end-to-end data pipeline using the GTFS (General Transit Feed Specification) Realtime datasets for Yarra Trams, provided by the Victorian Department of Transport and Planning.
Public transport services are frequently impacted by disruptions such as maintenance works, traffic incidents, and special events. However, these disruptions are not always easy to analyze systematically over time.
The objective of this project is to ingest and process real-time service alert data to enable analysis of:

- the frequency of service disruptions,

- the types and impact of incidents on tram operations,

- and how disruptions vary across different times of day.

In the first stage, the pipeline implements a micro-batch ingestion approach, where data is fetched from the API every 30 minutes. The data is then stored and transformed to support analytical queries and dashboard visualizations.

## Tools 



## Project structure


## Steps
1. Ensure uv is installed, if not:
```
pip install uv
```
 
Then sync with the project's uv config using:
```
uv sync
```

2. 