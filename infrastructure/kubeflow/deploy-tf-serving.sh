#!/bin/bash

juju add-model serving kubeflow-k8s --config update-status-hook-interval=30s

juju deploy  ./tf-serving --storage models=kubernetes,, --config model-name=tfserving --config model-base-path=s3://BUCKET2/tfserving --config aws-access-key-id=$(cat generated/access_key.txt) --config aws-region=us-east-1 --config aws-secret-access-key=$(cat generated/secret_key.txt) --config s3-endpoint=172.16.7.75 --config s3-verify-ssl="0" --config s3-use-https="0" --resource oci-image=afrikha/tfserving-kafka

