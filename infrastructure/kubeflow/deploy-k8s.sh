#!/bin/bash


juju add-model k8s fce-lab
juju set-model-constraints -m k8s zones=kubeflow
juju deploy ./k8s-bundle.yaml

juju wait -vw -m k8s

mkdir ~/.kube
juju scp -m k8s kubernetes-master/0:/home/ubuntu/config ~/.kube/config

juju config -m k8s containerd http_proxy=""
juju config -m k8s containerd https_proxy="http://squid.internal:3128"


kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.8.1/manifests/metallb.yaml

kubectl apply -f metallb/config.yaml
