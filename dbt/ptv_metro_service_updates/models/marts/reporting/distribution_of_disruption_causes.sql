/** 
    This report identifies the most common disruption effects in the service updates, ranked by their frequency of occurrence. 
    It provides insights into the types of disruptions that are most frequently reported, which can help in prioritizing response efforts and improving service reliability. 
    The report aggregates the data from the latest service updates and counts the occurrences of each disruption effect, allowing stakeholders to understand the most prevalent issues affecting the service.
 **/

 select
    count(*) as frequency,
    cause
 from {{ ref("fct_service_update_impacts") }}
 group by cause
 order by frequency desc