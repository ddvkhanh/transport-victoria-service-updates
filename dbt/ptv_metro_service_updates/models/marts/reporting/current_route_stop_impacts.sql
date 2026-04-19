/** 
This model identifies the current route-stop impacts based on the active period of the service updates. 
Since this model focuses on route-stop level impacts, we need to deduplicate the data to ensure that for each route-stop combination, we only keep the most recent update (based on ingest_timestamp) in case there are multiple updates (e.g: directions) affecting the same route-stop combination with overlapping active periods.
*/

{{ config(
    materialized = 'table'
    partition_by={
      "field": "active_period_start",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by=['route_id', 'stop_id']
) }}

with current_rows as (

    select
        entity_id,
        ingest_timestamp,
        active_period_start,
        active_period_end,
        cause,
        effect,
        description_text,
        header_text,
        severity_level,
        route_id,
        route_short_name,
        route_long_name,
        route_type,
        route_color,
        stop_id,
        stop_lat,
        stop_lon,
        stop_name,
        agency_id,
        agency_name
    from {{ ref("fct_service_update_impacts") }}
    where safe_cast(active_period_start as timestamp) <= current_timestamp()
      and (
        safe_cast(active_period_end as timestamp) >= current_timestamp()
        or active_period_end is null
      )
       and stop_id is not null
),

deduped as (

    select
        *,
        row_number() over (
            partition by entity_id, route_id, stop_id
            order by ingest_timestamp desc
        ) as rn
    from current_rows

)

select
    entity_id,
    ingest_timestamp,
    active_period_start,
    active_period_end,
    cause,
    effect,
    description_text,
    header_text,
    severity_level,
    route_id,
    route_short_name,
    route_long_name,
    route_type,
    route_color,
    stop_id,
    stop_lat,
    stop_lon,
    stop_name,
    agency_id,
    agency_name
from deduped
where rn = 1