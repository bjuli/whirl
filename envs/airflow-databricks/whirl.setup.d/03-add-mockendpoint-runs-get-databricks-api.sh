#!/usr/bin/env bash

echo "=============================================="
echo "== Configure Databricks API 'jobs/runs/get' =="
echo "=============================================="

# Mock result for api/2.0/jobs/runs/get endpoint
curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOFPENDING_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/runs/get",
    "headers": {
        "Content-Type": ["application/json"],
        "Authorization": ["Bearer .*"]
    },
    body: {
      "type": "JSON_PATH",
      "jsonPath": "$..run_id"
    }
  },
  "httpResponseTemplate": {
    "template": "s = JSON.parse(request.body.string);
      body = JSON.stringify(
        {
          job_id: 1,
          run_id: (s.run_id || -1),
          number_in_job: 1,
          state: {
            life_cycle_state: 'PENDING',
            state_message: 'Performing pending action'
          },
          run_page_url: '/?o=12345678910#job/1/run/' + s.run_id
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
  },
  "times": {
    "remainingTimes": 2,
    "unlimited": false
  }
}
_EOFPENDING_

curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOFRUNNING_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/runs/get",
    "headers": {
        "Content-Type": ["application/json"],
        "Authorization": ["Bearer .*"]
    },
    body: {
      "type": "JSON_PATH",
      "jsonPath": "$..run_id"
    }
  },
  "httpResponseTemplate": {
    "template": "s = JSON.parse(request.body.string);
      body = JSON.stringify(
        {
          job_id: 1,
          run_id: (s.run_id || -1),
          number_in_job: 1,
          state: {
            life_cycle_state: 'RUNNING',
            state_message: 'Performing running action'
          },
          run_page_url: '/?o=12345678910#job/1/run/' + s.run_id
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
  },
  "times": {
    "remainingTimes": 4,
    "unlimited": false
  }
}
_EOFRUNNING_

curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOFTERMINATING_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/runs/get",
    "headers": {
        "Content-Type": ["application/json"],
        "Authorization": ["Bearer .*"]
    },
    body: {
      "type": "JSON_PATH",
      "jsonPath": "$..run_id"
    }
  },
  "httpResponseTemplate": {
    "template": "s = JSON.parse(request.body.string);
      body = JSON.stringify(
        {
          job_id: 1,
          run_id: (s.run_id || -1),
          number_in_job: 1,
          state: {
            life_cycle_state: 'TERMINATING',
            state_message: 'Performing terminiating action'
          },
          run_page_url: '/?o=12345678910#job/1/run/' + s.run_id
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
  },
  "times": {
    "remainingTimes": 2,
    "unlimited": false
  }
}
_EOFTERMINATING_

curl -v -X PUT "http://mockserver:1080/mockserver/expectation" -d @- <<_EOFTERMINATED_
{
  "httpRequest": {
    "path": "/api/2.0/jobs/runs/get",
    "headers": {
        "Content-Type": ["application/json"],
        "Authorization": ["Bearer .*"]
    },
    body: {
      "type": "JSON_PATH",
      "jsonPath": "$..run_id"
    }
  },
  "httpResponseTemplate": {
    "template": "s = JSON.parse(request.body.string);
      body = JSON.stringify(
        {
          job_id: 1,
          run_id: (s.run_id || -1),
          number_in_job: 1,
          state: {
            life_cycle_state: 'TERMINATED',
            state_message: 'Performed action',
            result_state: 'SUCCESS'
          },
          run_page_url: '/?o=12345678910#job/1/run/' + s.run_id
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
  },
  "times": {
    "unlimited": true
  }
}
_EOFTERMINATED_

