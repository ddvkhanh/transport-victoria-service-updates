with unnest_informed_entities as (
    select
        entity_id,
        entity_timestamp,  
        ingest_timestamp,
        informed_entities,
        offset as informed_entity_index
    from {{ ref('stg_service_alerts_base') }} as base
    left join {{ unnest_json_array('alert_json', '$.informed_entities') }} as informed_entities with offset
)
select
    entity_id,
    entity_timestamp,  
    ingest_timestamp,
    informed_entities,
    informed_entity_index,
    {{ extract_scalar_json('informed_entities', '$.agency_id') }} as agency_id,
    {{ extract_scalar_json('informed_entities', '$.direction_id') }} as direction_id,
    {{ extract_scalar_json('informed_entities', '$.route_id') }} as route_id,
    {{ extract_scalar_json('informed_entities', '$.stop_id') }} as stop_id
from unnest_informed_entities
    
