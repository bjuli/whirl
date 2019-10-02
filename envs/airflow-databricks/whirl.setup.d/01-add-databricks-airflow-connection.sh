#!/usr/bin/env bash

echo "=============================="
echo "== Configure API Connection =="
echo "=============================="

airflow connections -a \
          --conn_id databricks_default \
          --conn_type HTTPS \
          --conn_host "localhost" \
          --conn_extra "{\"token\": \"secretDatabricksApiT0ken\"}"
