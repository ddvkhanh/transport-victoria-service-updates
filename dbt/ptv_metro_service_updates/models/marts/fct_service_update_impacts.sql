{{ config(
    materialized='table',
    partition_by={
        "field": "active_period_start",
        "data_type": "timestamp",
        "granularity": "day"
    },
    cluster_by=['route_sk', 'stop_sk']
) }}

with impacts as (

    select
        i.entity_id,
        i.entity_timestamp,
        i.ingest_timestamp,
        i.cause,
        i.effect,
        i.description_text,
        i.header_text,
        i.severity_level,
        i.informed_entity_index,
        i.agency_id,
        i.direction_id,
        i.route_id,
        i.stop_id,
        i.active_period_index,
        safe_cast(i.active_period_start as timestamp) as active_period_start,
        safe_cast(i.active_period_end   as timestamp) as active_period_end
    from {{ ref('int_service_updates_latest_impacts') }} i

)

select
    -- Surrogate key (full grain hash)
    {{ dbt_utils.generate_surrogate_key(['entity_id', 'ingest_timestamp', 'informed_entity_index', 'active_period_index']) }} as service_update_sk,

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
    ac.alert_classification_sk,
    r.route_sk,
    s.stop_sk,
    a.agency_sk,
    cast(format_date('%Y%m%d', date(i.active_period_start)) as int64) as active_period_start_date_key,
    cast(format_date('%Y%m%d', date(i.active_period_end))   as int64) as active_period_end_date_key,

    -- Timestamps (partition field must be in SELECT)
    i.active_period_start,
    i.active_period_end,

    -- Measures
    timestamp_diff(i.active_period_end, i.active_period_start, SECOND) as disruption_duration_seconds,
    case
        when i.active_period_start <= current_timestamp()
         and (i.active_period_end >= current_timestamp() or i.active_period_end is null)
        then true else false
    end                                                                 as is_currently_active,
    case when r.route_sk is not null and s.stop_sk is null then true else false end as is_route_alert,
    case when s.stop_sk is not null then true else false end             as is_stop_alert

from impacts i
left join {{ ref("dim_alert_classification") }} ac on i.cause          IS NOT DISTINCT FROM ac.cause
                                                   and i.effect         IS NOT DISTINCT FROM ac.effect
                                                   and i.severity_level IS NOT DISTINCT FROM ac.severity_level
left join {{ ref("dim_routes") }}              r  on i.route_id    = r.route_id
left join {{ ref("dim_stops") }}               s  on i.stop_id     = s.stop_id
left join {{ ref("dim_agency") }}              a  on i.agency_id   = a.agency_id
