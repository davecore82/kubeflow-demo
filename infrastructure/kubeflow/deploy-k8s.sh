#!/bin/bash


juju add-model k8s orangebox
juju deploy ./bundles/k8s-bundle.yaml

juju wait -vw -m k8s

mkdir ~/.kube
juju scp -m k8s kubernetes-master/0:/home/ubuntu/config ~/.kube/config

kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.8.1/manifests/metallb.yaml

kubectl apply -f metallb/config.yaml
