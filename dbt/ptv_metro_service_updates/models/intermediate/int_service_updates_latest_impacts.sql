select
    lb.entity_id,
    lb.entity_timestamp,
    lb.ingest_timestamp,
    lb.cause,
    lb.effect,
    lb.description_text,
    lb.header_text,
    lb.severity_level,
    ie.informed_entity_index,
    ie.agency_id,
    ie.direction_id,
    ie.route_id,
    ie.stop_id,
    ap.active_period_index,
    ap.active_period_start,
    ap.active_period_end

from {{ ref('int_service_updates_latest_base') }} lb
left join {{ ref('stg_service_alerts_informed_entities') }} as ie
    on lb.entity_id = ie.entity_id
    and lb.ingest_timestamp = ie.ingest_timestamp
left join {{ ref('stg_service_alerts_active_periods') }} as ap
    on lb.entity_id = ap.entity_id
    and lb.ingest_timestamp = ap.ingest_timestamp