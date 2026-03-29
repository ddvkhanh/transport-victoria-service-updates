select 
    route_id,
    route_short_name,
    route_long_name,
    route_type,
    route_color,
    route_text_color
from {{ ref("metro_routes")}} as routes