select
    stop_id,
    stop_name,
    stop_lat,
    stop_lon,
    parent_station,
    wheelchair_boarding,
    level_id,
    platform_code
from {{ ref("metro_stops")}}