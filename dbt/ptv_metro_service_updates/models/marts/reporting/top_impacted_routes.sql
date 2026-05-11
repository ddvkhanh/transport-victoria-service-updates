/** 
    This report identifies the top 5 routes most impacted by service disruptions, ranked by the number of total alerts of disruptions received.
*/

select
    r.route_id,
    r.route_short_name,
    count(distinct f.entity_id) as disruption_count
from {{ ref("fct_service_update_impacts") }} f
left join {{ ref("dim_routes") }} r on f.route_sk = r.route_sk
where r.route_id is not null
group by r.route_id, r.route_short_name
order by disruption_count desc