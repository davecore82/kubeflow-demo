#!/bin/bash

juju add-model data-store fce-lab
juju set-model-constraints -m data-store zones=kubeflow



juju deploy -m  data-store ./bundles/data-store-bundle.yaml

juju wait -vw -m data-store
