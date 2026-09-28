{% macro backup_table() %}
  {% if execute %}
    {% if adapter.get_relation(database=database, schema=schema, identifier=this.name) %}
      {% set sql %}
        DROP TABLE IF EXISTS {{ this.name }}_backup;
        CREATE TABLE {{ this.name }}_backup AS 
        SELECT * FROM {{ this.name }};
      {% endset %}
      {% do run_query(sql) %}
    {% endif %}
  {% endif %}
{% endmacro %}