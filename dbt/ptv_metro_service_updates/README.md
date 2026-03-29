# Transport Victoria Service Updates - dbt Project

This dbt project is responsible for transforming the raw GTFS Realtime data (ingested from the PTV API via Kestra) into structured, query-optimized analytical tables in BigQuery.

## Model Layers

The project follows standard dbt modeling best practices, structuring models into three distinct layers: **Staging**, **Intermediate**, and **Marts**.

### 1. Staging (`models/staging/`)
The **staging** layer acts as the entry point for raw data. Here, raw JSON payloads from BigQuery base tables are unpacked, flattened, and explicitly cast to proper data types. These models are typically materialized as views.

- **`stg_services_entity_base.sql`**: Extracts the foundational entity structures (like `entity_id` and timestamp) from the raw stream.
- **`stg_service_alerts_base.sql`**: Unpacks the top-level structure of the JSON `alert` payload (cause, effect, header, description).
- **`stg_service_alerts_active_periods.sql`**: Unnests the generic `active_period` array from the JSON to map start and end times for the alert.
- **`stg_service_alerts_informed_entities.sql`**: Unnests the `informed_entity` array to determine exactly which routes, stops, or trips are affected by the disruption.

### 2. Intermediate (`models/intermediate/`)
The **intermediate** layer is where business logic, joins, and aggregations are applied to staging models. This layer prepares the data for the final reporting layer without exposing it directly to BI tools. 

- **`int_service_updates_latest_base.sql`**: Because the raw pipeline could ingests the same active incidents (creating duplicates over time), this model applies window functions to isolate only the *latest* update state for any given event.
- **`int_service_updates_latest_impacts.sql`**: Joins the deduplicated alerts with their corresponding active periods and informed entities, creating a cohesive, single view of the ongoing disruption impacts before dimensioning.

### 3. Marts (`models/marts/`)
The **marts** layer contains the final, business-ready models materialized as `tables`. These are the models consumed by Looker Studio and other downstream data analysts.

- **`fct_service_update_impacts.sql`**: The central fact table. It takes the latest unnested impacts from the intermediate layer and enriches them with proper metadata by joining the dimensional tables. *It utilizes the `dbt_utils` package (specifically `dbt_utils.generate_surrogate_key`) to construct a reliable primary key for each unique disruption record.* This yields a wide table perfect for generating dashboard charts (filtering by route names, measuring disruption duration, etc).
- **`dim_agency.sql`**: Dimension table for transporting agencies.
- **`dim_routes.sql`**: Dimension table mapping `route_id` to human-readable route names.
- **`dim_stops.sql`**: Dimension table for physical train stations/stops.

### Additional Concepts

- **Seeds (`seeds/`)**: Static CSV reference data that is loaded into the data warehouse (e.g., core dimension mapping for `metro_agency` and `metro_routes`) to join against real-time IDs.
- **Sources (`models/staging/sources.yml`)**: Defines the upstream raw BigQuery dataset and table (`ptv_metro_dataset.service_updates_metro`) so dbt can trace its lineage from extraction.
- **Testing (`schema.yml` and `tests/`)**: Data quality is ensured through automated testing.
  - **YAML Tests (`schema.yml`)**: Basic built-in integrity checks such as `not_null` and `unique` constraints are defined directly on key columns (e.g., surrogate keys and `entity_id` values).
  - **Custom SQL Tests (`tests/`)**: Custom singular tests are written inside the `tests/` folder to check specific business logic rules that go beyond column-level assertions.

---

### Commands to Run (for testing only as dbt build is already included in Kestra flow)

```bash
# Install required dbt packages (e.g., dbt_utils)
dbt deps

# Run all models, tests, and seeds
dbt build

# Run just the models
dbt run
```
