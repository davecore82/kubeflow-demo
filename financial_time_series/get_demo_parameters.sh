#!/bin/bash

printf "#### Elasticsearch endpoint #### \n"
juju run -m data-store --unit elasticsearch/0 "unit-get private-address"

printf "#### RadosGW endpoint #### \n"

printf "http://$(juju run -m k8s --unit ceph-radosgw/0 "unit-get private-address") \n"

printf "#### S3 Access key #### \n"

cat ../infrastructure/kubeflow/generated/access_key.txt 

printf "#### S3 secret key #### \n"

cat ../infrastructure/kubeflow/generated/secret_key.txt

printf "\n"
