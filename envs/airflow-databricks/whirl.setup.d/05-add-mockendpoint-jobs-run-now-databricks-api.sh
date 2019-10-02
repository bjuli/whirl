#!/usr/bin/env bash

echo "============================================="
echo "== Configure Databricks API 'jobs/run-now' =="
echo "============================================="

# Mock result for api/2.0/jobs/run-now endpoint
curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOF_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/run-now",
    "headers": {
      "Content-Type": ["application/json"],
      "Authorization": ["Bearer .*"]
    },
    body: {
      "type": "JSON_PATH",
      "jsonPath": "$..job_id"
    }
  },
  "httpResponseTemplate": {
    "template": "runId = Math.random() * (100000 - 1) + 1;
    body = JSON.stringify({ run_id: Math.floor(runId), number_in_job: 1 });
    return {
        statusCode: 200,
        headers: {
            'content-type': [
                'application/json'
            ]
        },
        body: {
          'type': 'JSON',
          'json': body
        }
    };",
    "templateType": "JAVASCRIPT"
  }
}
_EOF_

