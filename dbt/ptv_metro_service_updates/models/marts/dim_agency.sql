select
    agency_id,
    agency_name,
    agency_timezone,
    agency_lang
from {{ ref("metro_agency") }} as agency