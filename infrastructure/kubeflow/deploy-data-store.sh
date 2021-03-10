#!/bin/bash

juju add-model data-store orangebox

juju deploy -m  data-store ./bundles/data-store-bundle.yaml

juju wait -vw -m data-store
