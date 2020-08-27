#!/usr/bin/env python3
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import kfp.dsl as dsl


class Preprocess(dsl.ContainerOp):

  def __init__(self, name, bucket, cutoff_year, es_address, endpoint_url, access_key, secret_key):
    super(Preprocess, self).__init__(
      name=name,
      # image needs to be a compile-time string
      image='afrikha/financial-time-series-demo:latest',
      command=['python3', 'run_preprocess.py'],
      arguments=[
        '--bucket', bucket,
        '--es_address', es_address,
        '--cutoff_year', cutoff_year,
        '--kfp',
        '--endpoint_url', endpoint_url,
        '--access_key', access_key,
        '--secret_key', secret_key

      ],
      file_outputs={'store_path': '/store_path.txt'}
    )


class Train(dsl.ContainerOp):

  def __init__(self, name, store_path, tag, bucket, model, es_address, endpoint_url, access_key, secret_key):
    super(Train, self).__init__(
      name=name,
      # image needs to be a compile-time string
      image='afrikha/financial-time-series-demo:latest',
      command=['python3', 'run_train.py'],
      arguments=[
        '--tag', tag,
        '--store_path', store_path,
        '--es_address', es_address,
        '--bucket', bucket,
        '--model', model,
        '--kfp',
        '--endpoint_url', endpoint_url,
        '--access_key', access_key,
        '--secret_key', secret_key
      ],
      file_outputs={'mlpipeline_metrics': '/mlpipeline-metrics.json',
                    'accuracy': '/tmp/accuracy'}
    )


class Deploy(dsl.ContainerOp):

  def __init__(self, name, tag, bucket, endpoint_url, access_key, secret_key):
    super(Deploy, self).__init__(
      name=name,
      # image needs to be a compile-time string
      image='afrikha/financial-time-series-demo:latest',
      command=['python3', 'run_deploy.py'],
      arguments=[
        '--tag', tag,
        '--bucket', bucket,
        '--endpoint_url', endpoint_url,
        '--access_key', access_key,
        '--secret_key', secret_key
      ],
    )


@dsl.pipeline(
  name='financial time series',
  description='Train Financial Time Series'
)
def preprocess_train_deploy(
        bucket: str = '<bucket>',
        cutoff_year: str = '2010',
        tag: str = '4',
        model: str = 'DeepModel',
        es_address: str = '<es_address>',
        endpoint_url: str = '<endpoint_url>',
        access_key: str = '<access_key>',
        secret_key: str = '<secret_key>'
):
  """Pipeline to train financial time series model"""
  preprocess_op = Preprocess('preprocess', bucket, cutoff_year, es_address, endpoint_url, access_key, secret_key)
  #pylint: disable=unused-variable
  train_op = Train('train', preprocess_op.output, tag,
                   bucket, model, es_address, endpoint_url, access_key, secret_key)
  with dsl.Condition(train_op.outputs['accuracy'] > 0.5):
    deploy_op = Deploy('deploy', tag, bucket,  endpoint_url, access_key, secret_key)


if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(preprocess_train_deploy, __file__ + '.tar.gz')
