select
    b.entity_id,
    b.entity_timestamp,
    b.ingest_timestamp,
    b.cause,
    b.effect,
    b.description_text,
    b.header_text,
    b.severity_level,
    ie.informed_entity_index,
    ie.agency_id,
    ie.direction_id,
    ie.route_id,
    ie.stop_id,
    ap.active_period_index,
    ap.active_period_start,
    ap.active_period_end

from {{ ref('stg_service_alerts_base') }} b
left join {{ ref('stg_service_alerts_informed_entities') }} as ie
    on b.entity_id = ie.entity_id
    and b.ingest_timestamp = ie.ingest_timestamp
left join {{ ref('stg_service_alerts_active_periods') }} as ap
    on b.entity_id = ap.entity_id
    and b.ingest_timestamp = ap.ingest_timestamp
