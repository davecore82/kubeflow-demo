#!/bin/bash
if [ -d "./generated" ]; then
	mkdir generated
fi

juju ssh -m k8s ceph-mon/0 'sudo radosgw-admin user create --uid="ubuntu" --display-name="Ubuntu Ceph"' | tee generated/rgw_user.txt

cat generated/rgw_user.txt | jq '.keys[0].access_key' | sed 's/\"//g' > generated/access_key.txt
cat generated/rgw_user.txt | jq '.keys[0].secret_key' | sed 's/\"//g' > generated/secret_key.txt

