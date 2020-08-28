#!/bin/bash

juju add-model serving kubeflow-k8s --config update-status-hook-interval=30s

BUCKET_NAME=MYBUCKET
S3_ENDPOINT=$(juju run -m k8s --unit ceph-radosgw/0 "unit-get private-address")

juju deploy  cs:~kubeflow-charmers/tf-serving  --storage models=kubernetes,, --config model-name=tfserving --config model-base-path=s3://$BUCKET_NAME/tfserving --config aws-access-key-id=$(cat generated/access_key.txt) --config aws-region=us-east-1 --config aws-secret-access-key=$(cat generated/secret_key.txt) --config s3-endpoint=$S3_ENDPOINT --config s3-verify-ssl="0" --config s3-use-https="0" --resource oci-image=afrikha/tfserving-kafka  --config env-vars="KAFKA_IP=172.16.7.149"

