 /**
  Most common disruption causes by frequency.
  Excludes general route-only alerts.
*/

{{ config(materialized='view') }}

 select
    count(*) as frequency,
    ac.cause
 from {{ ref("fct_service_update_impacts") }} f
 left join {{ ref("dim_alert_classification") }} ac on f.alert_classification_sk = ac.alert_classification_sk
 where f.is_stop_alert
   and ac.cause is not null
 group by ac.cause
 order by frequency desc