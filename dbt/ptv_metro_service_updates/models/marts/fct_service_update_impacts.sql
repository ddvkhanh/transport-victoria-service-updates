{{ config(
    materialized = 'table'
) }}

select
    {{ dbt_utils.generate_surrogate_key([
        'sl.entity_id',
        'sl.ingest_timestamp',
        'sl.informed_entity_index'
    ]) }} as service_update_route_sk,
    sl.entity_id,
    sl.entity_timestamp,
    sl.ingest_timestamp,
    sl.active_period_start,
    sl.active_period_end,
    sl.cause,
    sl.effect,
    sl.description_text,
    sl.header_text,
    sl.severity_level,
    sl.direction_id,
    sl.route_id,
    dr.route_short_name,
    dr.route_long_name,
    dr.route_type,
    dr.route_color,
    sl.stop_id,
    ds.stop_name,
    sl.agency_id,
    da.agency_name
from {{ ref("int_service_updates_latest_impacts") }} sl
left join {{ ref("dim_routes") }} as dr
    on sl.route_id = dr.route_id
left join {{ ref("dim_agency") }} as da
    on sl.agency_id = da.agency_id
left join {{ ref("dim_stops") }} as ds
    on sl.stop_id = ds.stop_id