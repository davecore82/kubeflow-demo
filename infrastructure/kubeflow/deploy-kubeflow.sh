#!/bin/bash
juju add-k8s kubeflow-k8s
juju add-model kubeflow kubeflow-k8s --config update-status-hook-interval=30s

juju deploy cs:~kubeflow-charmers/bundle/kubeflow-lite-6 --overlay ./bundles/config-overlay.yaml

sleep 5


juju wait  -wv -m kubeflow

kubectl apply -f pipeline-patch.yaml

SvcIP=`kubectl get svc/ambassador -o json -n kubeflow | jq '.status.loadBalancer.ingress[0].ip' | tr -d '"' `
juju config dex-auth public-url=http://$SvcIP.xip.io:80
juju config oidc-gatekeeper public-url=http://$SvcIP.xip.io:80
juju config ambassador juju-external-hostname=$SvcIP.xip.io
juju expose ambassador

