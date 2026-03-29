-- This model selects the latest service updates for each entity_id based on the ingest_timestamp.
-- It only contains the base information, for detailed alert (1 entity can have multiple alert, we refer to int_service_updates_latest_alert
with latest_service_updates as (
    select
        entity_id,
        entity_timestamp,  
        ingest_timestamp,
        row_number() over (partition by entity_id  order by ingest_timestamp desc) as row_num
    from {{ ref('stg_service_alerts_base') }}
)

select
    base.entity_id,
    base.entity_timestamp,  
    base.ingest_timestamp,
    base.alert_json,
    base.cause,
    base.effect,
    base.description_text,
    base.header_text,
    base.severity_level

from {{ ref('stg_service_alerts_base') }} as base
join latest_service_updates l
    on base.entity_id = l.entity_id
    and base.ingest_timestamp = l.ingest_timestamp
where l.row_num = 1