-- This macro utilizes BigQuery's JSON_QUERY_ARRAY function to unnest JSON arrays, allowing to work with each element of the array as a separate row in the query results.

{% macro unnest_json_array(json_column, json_path) %}
    UNNEST(JSON_QUERY_ARRAY({{ json_column }}, '{{json_path}}'))
{% endmacro %}