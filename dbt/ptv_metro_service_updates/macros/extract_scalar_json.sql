-- This macro  utilizes BigQuery's JSON_VALUE function to retrieve the scalar value, for extracting simple values from JSON structures.

{% macro extract_scalar_json(json_column, json_path, alias = None) %}
    json_value({{json_column}}, '{{json_path}}')
    {%- if alias %} as {{ alias }} {%- endif%}
{% endmacro %}}