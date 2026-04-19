/**
    This report shows the distribution of disruptions over time, allowing stakeholders to identify trends and patterns in service disruptions.
*/

select 
    date(active_period_start) as disruption_date,
    cause,
    count(distinct(route_id)) as disruption_count
from {{ ref("fct_service_update_impacts") }}
group by disruption_date, cause