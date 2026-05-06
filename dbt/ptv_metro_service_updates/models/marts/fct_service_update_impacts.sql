{{ config(
    materialized='table',
    partition_by={
        "field": "active_period_start",
        "data_type": "timestamp",
        "granularity": "day"
    },
    cluster_by=['route_id', 'stop_id']
) }}

with impacts as (

    select
        i.entity_id,
        i.entity_timestamp,
        i.ingest_timestamp,
        i.informed_entity_index,
        i.active_period_index,
        i.cause,
        i.effect,
        i.severity_level,
        i.description_text,
        i.header_text,
        i.agency_id,
        i.direction_id,
        i.route_id,
        i.stop_id,
        safe_cast(i.active_period_start as timestamp) as active_period_start,
        safe_cast(i.active_period_end   as timestamp) as active_period_end
    from {{ ref('int_service_updates_latest_impacts') }} i

)

select
    -- Surrogate key
    {{ dbt_utils.generate_surrogate_key([
        'entity_id',
        'ingest_timestamp',
        'informed_entity_index',
        'active_period_index'
    ]) }}                                                              as service_update_sk,

    -- Degenerate dimensions
    entity_id,
    entity_timestamp,
    ingest_timestamp,
    informed_entity_index,
    active_period_index,
    direction_id,
    description_text,
    header_text,

    -- Foreign keys
    {{ dbt_utils.generate_surrogate_key([
        'i.cause', 'i.effect', 'i.severity_level'
    ]) }}                                                              as alert_classification_sk,
    r.route_sk,
    s.stop_sk,
    a.agency_sk,
    cast(format_date('%Y%m%d', date(i.active_period_start)) as int64)  as active_period_start_date_key,
    cast(format_date('%Y%m%d', date(i.active_period_end))   as int64)  as active_period_end_date_key,


    -- Timestamps (for partition + reporting filters)
    active_period_start,
    active_period_end,

    -- Measures
    timestamp_diff(active_period_end, active_period_start, SECOND)     as disruption_duration_seconds,
    case
        when active_period_start <= current_timestamp()
         and (active_period_end >= current_timestamp() or active_period_end is null)
        then true else false
    end                                                                as is_currently_active,
    case when route_id is not null and stop_id is null then true else false end  as is_route_alert,
    case when stop_id is not null then true else false end             as is_stop_alert
from impacts