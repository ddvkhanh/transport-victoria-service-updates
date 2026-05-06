select
    {{ dbt_utils.generate_surrogate_key(['route_id']) }}  as route_sk,
    route_id,
    agency_id,
    route_short_name,
    route_long_name,
    route_type,
    route_color,
    route_text_color
from {{ ref('metro_routes') }}