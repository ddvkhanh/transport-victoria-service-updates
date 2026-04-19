/** 
    This report identifies the top 5 routes most impacted by service disruptions, ranked by the number of total alerts of disruptions received.
*/

select
    route_id,
    route_short_name,
    date(active_period_start) as disruption_date,
    count(distinct entity_id) as disruption_count
from {{ ref("fct_service_update_impacts") }}
where route_id is not null
group by route_id, route_short_name
order by disruption_count desc