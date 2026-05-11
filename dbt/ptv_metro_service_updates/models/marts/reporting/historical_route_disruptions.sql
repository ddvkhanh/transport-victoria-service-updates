/**
  Historical route-level disruptions. Latest update per (entity, route).
  Excludes general route-only alerts. direction_id intentionally dropped.
*/


{{ config(
    materialized = 'table',
    partition_by={
      "field": "active_period_start",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by=['route_sk']
) }}


with base as (

    select
        f.entity_id,
        f.ingest_timestamp,
        f.route_sk,
        f.alert_classification_sk,
        f.disruption_duration_seconds,  -- kept for the conversion below
        f.active_period_start_date_key,
        f.active_period_end_date_key
    from {{ ref("fct_service_update_impacts") }}
    where is_route_alert = true
        and active_period_start_date_key is not null
),

deduped as (
    select
        *,
        row_number() over (
            partition by entity_id, route_sk
            order by ingest_timestamp desc
        ) as rn
    from base
)

select
    d.entity_id,
    d.ingest_timestamp,
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    ac.cause,
    ac.effect,
    ac.severity_level,
    ds.full_date as active_period_start_date,
    de.full_date as active_period_end_date,
    round(d.disruption_duration_seconds / 86400.0, 2) as disruption_duration_days
from deduped d
left join {{ ref("dim_alert_classification") }} ac on d.alert_classification_sk = ac.alert_classification_sk
left join {{ ref("dim_routes") }} r on d.route_sk = r.route_sk
left join {{ ref("dim_date") }} ds on d.active_period_start_date_key = ds.date_key
left join {{ ref("dim_date") }} de on d.active_period_end_date_key = de.date_key
where d.rn = 1