/**
  Distribution of disruptions over time, broken down by cause.
  Counts distinct routes per (date, cause). Excludes general route-only alerts.
*/

{{ config(
    materialized='table',
    partition_by={
      "field": "disruption_date",
      "data_type": "date"
    },
    cluster_by=['cause']
) }}

select 
    date(d.full_date) as disruption_date,
    ac.cause,
    count(distinct(r.route_id)) as disruption_count
from {{ ref("fct_service_update_impacts") }} f
left join {{ ref("dim_alert_classification") }} ac on f.alert_classification_sk = ac.alert_classification_sk
left join {{ ref("dim_routes") }} r on f.route_sk = r.route_sk
left join {{ ref("dim_date") }} d on f.active_period_start_date_key = d.date_key
where f.is_stop_alert    and f.active_period_start_date_key is not null
group by disruption_date, ac.cause