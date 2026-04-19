/** 
    This report identifies the most common disruption effects in the service updates, ranked by their frequency of occurrence. 
 **/

 select
    count(*) as frequency,
    effect
 from {{ ref("fct_service_update_impacts") }}
 group by effect
 order by frequency desc