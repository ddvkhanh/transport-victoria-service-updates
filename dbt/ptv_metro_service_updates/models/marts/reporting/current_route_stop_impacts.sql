/**
  Current active route-stop impacts.
  Deduplicates to one row per (route_sk, stop_sk), keeping the latest ingest.
  Excludes route-only alerts. Direction collapsed.
*/

{{ config(
    materialized='table',
    partition_by={
        "field": "active_period_start",
        "data_type": "timestamp",
        "granularity": "day"
    },
    cluster_by=['route_id', 'stop_id']
) }}

with current_rows as (

    select
        service_update_sk,
        entity_id,
        entity_timestamp,
        ingest_timestamp,
        informed_entity_index,
        active_period_index,
        direction_id,
        description_text,
        header_text,
        alert_classification_sk,
        route_sk,
        stop_sk,
        agency_sk,
        active_period_start_date_key,
        active_period_end_date_key,
        active_period_start,
        active_period_end,
        disruption_duration_seconds,
        is_currently_active,
        is_route_alert,
        is_stop_alert

    from {{ ref("fct_service_update_impacts") }}
    where is_currently_active = true
        and is_stop_alert = true

),

deduped as (

    select
        *,
        row_number() over (
            partition by route_sk, stop_sk
            order by ingest_timestamp desc
        ) as rn
    from current_rows

)

select
    f.entity_id,
    f.ingest_timestamp,
    f.active_period_start,
    f.active_period_end,
    d1.full_date as active_period_start_date,
    d2.full_date as active_period_end_date,
    f.disruption_duration_seconds,

    -- alert classification + degenerate text
    ac.cause,
    ac.effect,
    ac.severity_level,
    f.description_text,
    f.header_text,

    -- route attrs
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    r.route_type,
    r.route_color,

    -- stop attrs
    s.stop_id,
    s.stop_name,
    s.stop_lat,
    s.stop_lon,

    -- agency attrs
    a.agency_id,
    a.agency_name

from deduped                                       f
left join {{ ref('dim_alert_classification') }}    ac on f.alert_classification_sk      = ac.alert_classification_sk
left join {{ ref('dim_routes') }}                  r  on f.route_sk                     = r.route_sk
left join {{ ref('dim_stops') }}                   s  on f.stop_sk                      = s.stop_sk
left join {{ ref('dim_agency') }}                  a  on f.agency_sk                    = a.agency_sk
left join {{ ref('dim_date') }}                    d1 on f.active_period_start_date_key = d1.date_key
left join {{ ref('dim_date') }}                    d2 on f.active_period_end_date_key   = d2.date_key
where f.rn = 1
