--- This macro utilizes BigQuery's JSON_QUERY function to retrieve the JSON object, which is useful for handling nested JSON structures.

{% macro extract_query_json(json_column, json_path) %}
    JSON_QUERY({{json_column}}, '{{json_path}}')
{% endmacro %}}