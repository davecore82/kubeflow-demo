#!/bin/bash -eu
snap install juju --classic --channel 2.7/stable
snap install juju-lint --classic
snap install juju-wait --classic
snap install juju-crashdump --classic
snap install kubectl --classic
snap install jq
apt update
apt install -y sshuttle python3-pip s3cmd
pip3 install elasticsearch
pip3 install kfp --upgrade
export PATH=$PATH:~/.local/bin
