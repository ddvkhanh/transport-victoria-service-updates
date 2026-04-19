/** 
    This report identifies the most common disruption causes in the service updates, ranked by their frequency of occurrence. 
 **/

 select
    count(*) as frequency,
    cause
 from {{ ref("fct_service_update_impacts") }}
 group by cause
 order by frequency desc