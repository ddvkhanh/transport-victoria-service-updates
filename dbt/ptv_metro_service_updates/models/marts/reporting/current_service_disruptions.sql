
 select
    active_period_start,
    active_period_end,
    cause,
    effect,
    description_text,
    header_text,
    severity_level,
    direction_id,
    route_id,
    route_short_name,
    route_long_name,
    route_type,
    route_color,
    stop_id,
    stop_name,
    agency_id,
    agency_name
 from {{ ref("fct_service_update_impacts") }}
where safe_cast(active_period_start as timestamp) <= current_timestamp()
  and (
    safe_cast(active_period_end as timestamp) >= current_timestamp()
    or active_period_end is null
  )
