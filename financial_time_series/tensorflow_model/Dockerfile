# Copyright 2018 The Kubeflow Authors All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM tensorflow/tensorflow:1.15.0-py3

# install gcloud
RUN apt-get update && apt-get install -y jq

# install python packages
RUN pip3 install pandas==0.23.4 \
                 elasticsearch==7.7.0 \
                 boto3==1.13.16
COPY . /opt/workdir
WORKDIR /opt/workdir
