#!/usr/bin/env bash
echo "================"
echo "== Install JQ =="
echo "================"

sudo apt-get update && \
sudo apt-get install -y jq && \
sudo apt-get clean

echo "=================="
echo "== Configure S3 =="
echo "=================="

pip install awscli awscli-plugin-endpoint

echo -e "$AWS_ACCESS_KEY_ID\n$AWS_SECRET_ACCESS_KEY\n\n" | aws configure
aws configure set plugins.endpoint awscli_plugin_endpoint
aws configure set default.s3.endpoint_url http://${AWS_SERVER}:${AWS_PORT}
aws configure set default.s3api.endpoint_url http://${AWS_SERVER}:${AWS_PORT}

echo "======================"
echo "== Create S3 Bucket =="
echo "======================"
while [[ $(curl -s http://${AWS_SERVER}:${AWS_PORT} | jq '.status') != '"running"' ]]; do
  echo "Waiting for ${AWS_SERVER} to come up..."
  sleep 2;
done

echo "creating bucket"
aws s3api create-bucket --bucket ${DEMO_BUCKET}
