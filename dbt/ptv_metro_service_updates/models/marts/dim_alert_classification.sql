ith src as (

    select distinct
        cause,
        effect,
        severity_level
    from {{ ref('int_service_updates_latest_base') }}
    where coalesce(cause, effect, severity_level) is not null

)

select
    {{ dbt_utils.generate_surrogate_key([
        'cause',
        'effect',
        'severity_level'
    ]) }} as alert_classification_sk,
    cause,
    effect,
    severity_level
from src