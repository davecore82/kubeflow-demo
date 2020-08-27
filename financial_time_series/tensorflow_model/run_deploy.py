"""Module for deploying a machine learning model to TF serving.

Scripts that performs the steps to deploy a model with TF serving
"""
import argparse
import logging
import sys
import subprocess

from helpers import storage as storage_helper


def parse_arguments(argv):
  """Parse command line arguments
  Args:
      argv (list): list of command line arguments including program name
  Returns:
      The parsed arguments as returned by argparse.ArgumentParser
  """
  parser = argparse.ArgumentParser(description='Preprocessing')

  parser.add_argument('--bucket',
                      type=str,
                      help='RGW bucket where preprocessed data is saved',
                      default='<your-bucket-name>')

  parser.add_argument('--tag',
                      type=str,
                      help='tag of the model',
                      required=True)

  parser.add_argument('--access_key',
                      type=str,
                      help='User access key for RGW',
                      required=True)

  parser.add_argument('--secret_key',
                      type=str,
                      help='User secret key for RGW',
                      required=True)

  parser.add_argument('--endpoint_url',
                      type=str,
                      help='RGW endpoint url',
                      required=True)
  args, _ = parser.parse_known_args(args=argv[1:])

  return args


def run_deploy(argv=None):
  """Runs the retrieval and preprocessing of the data.

  Args:
    args: args that are passed when submitting the training

  """
  args = parse_arguments(sys.argv if argv is None else argv)
  logging.info('start deploying model %s ..', args.tag)

  # get latest active version for TF serving directory
  serving_dir = 'tfserving'
  blobs = storage_helper.list_blobs(args.bucket, args.endpoint_url, 
                                    args.access_key, args.secret_key, 
                                    prefix=serving_dir)
  version = set()
  for blob in blobs:
    version.add(int(blob.key.split('/')[1]))
  if version:
    new_version = max(version)+1
  else:
    new_version = 1

  # copy the files
  logging.info('deploying model %s as model number %s on TF serving', args.tag, new_version)

  # #TODO use upload from storage helper
  storage_helper.copy_objects(args.bucket, args.endpoint_url, 
                              args.access_key, args.secret_key, 
                              'models/{}/'.format(args.tag), 
                              'tfserving/{}/'.format(new_version) )


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  run_deploy()
