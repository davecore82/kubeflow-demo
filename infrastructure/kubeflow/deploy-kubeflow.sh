#!/bin/bash
juju add-k8s kubeflow-k8s
juju add-model kubeflow kubeflow-k8s --config update-status-hook-interval=30s

# kubeflow-lite rev 39 has been recommended to avoid jupyter-controller bug
# https://github.com/canonical/bundle-kubeflow/issues/335
juju deploy cs:~kubeflow-charmers/bundle/kubeflow-lite-39

sleep 5


juju wait  -wv -m kubeflow

# i don't think we need this anymore
#kubectl apply -f pipeline-patch.yaml

# some things have changed (ambassador has been removed)
SvcIP=`kubectl get svc/istio-ingressgateway -o json -n kubeflow | jq '.status.loadBalancer.ingress[0].ip' | tr -d '"' `
juju config dex-auth public-url=http://$SvcIP.xip.io
juju config oidc-gatekeeper public-url=http://$SvcIP.xip.io

kubectl patch role -n kubeflow istio-ingressgateway-operator -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-operator"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'

juju config dex-auth static-username=admin
juju config dex-auth static-password=AxWiJjk2hu4fFga7

#Access the dashboard
#for remote deployments, or running on a virtual machine, creating a SOCKS proxy is required to access the dashboard. This can be done as follows:
#Logout from the current session with the exit command
#
#Re-establish connection to the machine using ssh with SOCKS proxy enabled through the -D 9999 parameter. As in the example below:
#
#ssh -D 9999 ubuntu@<machine_public_ip>
#On your computer, go to Settings > Network > Network Proxy, and enable SOCKS proxy pointing to: 127.0.0.1:9999
#
#On a new browser window, access the link given in the previous step, appended by .xip.io, for example: http://10.64.140.43.xip.io


