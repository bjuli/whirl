#!/usr/bin/env bash

echo "============================================="
echo "== Configure Databricks API 'jobs/run-now' =="
echo "============================================="

# Mock result for api/2.0/jobs/get endpoint
curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOF_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/get",
    "headers": {
        "Content-Type": ["application/json"],
        "Authorization": ["Bearer .*"]
    },
    "queryStringParameters": {
            "job_id": ["[0-9]+"]
        }
  },
  "httpResponseTemplate": {
    "template": "body = JSON.stringify(
        {
          job_id: ((request.queryStringParameters || {})['job_id'] || [1])[0],
          settings: {
            name: 'job-name',
            new_cluster: {
              spark_version: '5.2.x-scala2.11',
              spark_conf: {
                'spark.databricks.delta.preview.enabled': 'true',
                'spark.sql.hive.metastore.jars': 'builtin',
                'spark.sql.execution.arrow.enabled': 'true',
                'spark.sql.hive.metastore.version': '1.2.1'
              },
              node_type_id: 'Standard_DS4_v2',
              spark_env_vars: {
                PYSPARK_PYTHON: '/databricks/python3/bin/python3'
              },
              num_workers: 2
            },
            libraries: [],
            email_notifications: {},
            schedule: {
              quartz_cron_expression: '59 59 23 31 DEC ? 2099',
              timezone_id: 'Europe/Amsterdam'
            },
            spark_python_task: {
              python_file: 'dbfs:/mnt/libraries/mock_job/mock_job-main.py',
              parameters: [
                '--arg1',
                'foo',
                '--arg2',
                'bar'
              ]
            },
            max_concurrent_runs: 1
          },
          created_time: 1557997134925,
          creator_user_name: '_svc_mockuser@mocker.microsoft.com'
        }
    );
    return {
        statusCode: 200,
        headers: {
            'content-type': [
                'application/json'
            ]
        },
        body: body
    };",
    "templateType": "JAVASCRIPT"
  }
}
_EOF_

