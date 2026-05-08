/**
  Most common disruption effects by frequency.
  Excludes general route-only alerts.
*/

{{ config(materialized='view') }}

select
    ac.effect,
    count(*) as frequency
from {{ ref('fct_service_update_impacts') }}    f
left join {{ ref('dim_alert_classification') }} ac on f.alert_classification_sk = ac.alert_classification_sk
where f.is_stop_alert
  and ac.effect is not null
group by ac.effect
order by frequency desc