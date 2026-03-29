select
    entity_id,
    entity_timestamp,
    ingest_timestamp,
    {{ extract_query_json('alert', '$') }} as alert_json
from {{ source('raw_data', 'service_updates_metro') }} 
