/**
 * This model creates a historical route-level view of service disruptions by retaining
 * the most recent update for each disruption entity and route combination.
 * It is partitioned by the start of the active period to optimize date-based queries,
 * and clustered by route_id to improve route-level filtering and aggregation.
 */

{{ config(
    materialized = 'table',
    partition_by={
      "field": "active_period_start",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by=['route_id']
) }}


with base as (

    select
        entity_id,
        ingest_timestamp,
        route_id,
        route_short_name,
        route_long_name,
        cause,
        effect,
        severity_level,
        safe_cast(active_period_start as timestamp) as active_period_start,
        safe_cast(active_period_end as timestamp) as active_period_end
    from {{ ref("fct_service_update_impacts") }}
    where route_id is not null
       and safe_cast(active_period_start as timestamp) is not null
),

deduped as (
    select
        *,
        row_number() over (
            partition by entity_id, route_id
            order by ingest_timestamp desc
        ) as rn
    from base
)

select
    entity_id,
    ingest_timestamp,
    route_id,
    route_short_name,
    route_long_name,
    cause,
    effect,
    severity_level,
    active_period_start,
    active_period_end
from deduped
where rn = 1