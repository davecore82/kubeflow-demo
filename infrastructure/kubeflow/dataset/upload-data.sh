#!/bin/bash
elasticsearch_ip=$(juju run -m data-store  --unit elasticsearch/0 'unit-get private-address')

python3 import.py $elasticsearch_ip