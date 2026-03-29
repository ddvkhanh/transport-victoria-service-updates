with unnest_active_periods as (
    select
        entity_id,
        entity_timestamp,  
        ingest_timestamp,
        active_periods,
        offset as active_period_index
    from {{ ref('stg_service_alerts_base') }} as base
    left join {{ unnest_json_array('alert_json', '$.active_periods') }} as active_periods with offset
)
select
    entity_id,
    entity_timestamp,  
    ingest_timestamp,
    active_periods,
    active_period_index,
    {{ extract_scalar_json('active_periods', '$.start') }} as active_period_start,
    {{ extract_scalar_json('active_periods', '$.end') }} as active_period_end
from unnest_active_periods