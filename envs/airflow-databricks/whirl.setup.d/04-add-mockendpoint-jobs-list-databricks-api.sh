#!/usr/bin/env bash

echo "============================================"
echo "== Configure Databricks API \"jobs/list\" =="
echo "============================================"

# Mock result for api/2.0/jobs/list endpoint
curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOF_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/list",
    "headers": {
        "Content-Type": ["application/json"],
        "Authorization": ["Bearer .*"]
    }
  },
  "httpResponse": {
    "statusCode": 200,
    "headers": {
      "content-type": [
        "application/json"
      ]
    },
    "body": {
      "type": "JSON",
      "json": "{
        \"jobs\": [
          {
            \"job_id\": 1,
            \"settings\": {
              \"name\": \"name-of-existing-job-1\"
            },
            \"created_time\": 1557997134925,
            \"creator_user_name\": \"creator of name-of-existing-job-1\"
          },
          {
            \"job_id\": 2,
            \"settings\": {
              \"name\": \"name-of-existing-job-2\"
            },
            \"created_time\": 1557997144925,
            \"creator_user_name\": \"creator of name-of-existing-job-2\"
          },
          {
            \"job_id\": 3,
            \"settings\": {
              \"name\": \"name-of-existing-job-3\"
            },
            \"created_time\": 1557995134925,
            \"creator_user_name\": \"creator of name-of-existing-job-3\"
          },
          {
            \"job_id\": 4,
            \"settings\": {
              \"name\": \"name-of-existing-job-4\"
            },
            \"created_time\": 1557996134925,
            \"creator_user_name\": \"creator of name-of-existing-job-4\"
          },
          {
            \"job_id\": 5,
            \"settings\": {
              \"name\": \"name-of-existing-job-5\"
            },
            \"created_time\": 1557996134925,
            \"creator_user_name\": \"name-of-existing-job-5\"
          }

        ]
      }"
    }
  }
}
_EOF_

