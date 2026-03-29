select
    entity_id,
    entity_timestamp,
    ingest_timestamp,
    alert_json,
    {{ extract_scalar_json('alert_json', '$.cause') }} as cause,
    {{ extract_scalar_json('alert_json', '$.effect') }} as effect,
    {{ extract_scalar_json('alert_json', '$.description_text') }} as description_text,
    {{ extract_scalar_json('alert_json', '$.header_text') }} as header_text,
    {{ extract_scalar_json('alert_json', '$.severity_level') }} as severity_level

from {{ ref('stg_services_entity_base') }} as base