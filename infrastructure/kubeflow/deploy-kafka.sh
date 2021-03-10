#!/bin/bash

juju add-model kafka orangebox

#juju deploy -m  kafka ./bundles/kafka-bundle.yaml --overlay ./secrets/config-overlay.yaml
juju deploy -m  kafka ./bundles/kafka-bundle.yaml 

juju wait -vw -m kafka

juju run-action kafka/0 create-topic topic=request \
 partitions=1 replication=1

juju run-action kafka/0 create-topic topic=response \
 partitions=1 replication=1
