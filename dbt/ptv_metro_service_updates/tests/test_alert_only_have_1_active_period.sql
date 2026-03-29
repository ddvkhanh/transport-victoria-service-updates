/**
    This test checks that there is only 1 active period for each service alert. 
    If there are more than 1 active periods, it means that the latest service update is not correctly identified, and we need to investigate further.
**/

select
    entity_id,
    ingest_timestamp,
    count(*) as cnt
from {{ ref('stg_service_alerts_active_periods') }}
group by 1, 2
having count(*) > 1