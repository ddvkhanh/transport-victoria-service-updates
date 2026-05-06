select
    {{ dbt_utils.generate_surrogate_key(['agency_id']) }}  as agency_sk,
    agency_id,
    agency_name,
    agency_timezone,
    agency_lang
from {{ ref("metro_agency") }} as agency