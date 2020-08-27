"""Module that handles downloads and uploads to RGW ceph storage.

Helpers functions to perform uploads and downloads from  RGW ceph storage.
"""
import os
import boto3
from botocore.exceptions import ClientError

def upload_to_storage(bucket, export_path, endpoint_url, access_key, secret_key):
  """Upload files from export path to RGW ceph storage.

  Args:
    bucket (str): RGW Cloud Storage bucket
    export_path (str): export path

  Returns:

  """
  s3 = boto3.client('s3', endpoint_url=endpoint_url ,aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
  s3.create_bucket(Bucket=bucket)
  for root, _, files in os.walk(export_path):
    for file in files:
      path = os.path.join(root, file)
      try:
        s3.upload_file(path, bucket, path)
      except ClientError as e:
        return False

def download_blob(bucket_name, source_blob_name, destination_file_name, endpoint_url, access_key, secret_key):
  """Downloads a blob from the bucket."""
  s3 = boto3.client('s3', endpoint_url=endpoint_url ,aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
  s3.download_file(bucket_name, source_blob_name, destination_file_name)
  
  print('File {} downloaded to {}.'.format(
    source_blob_name,
    destination_file_name))


def list_blobs(bucket_name, endpoint_url, access_key, secret_key, prefix):
  """Lists all the blobs in the bucket."""
  s3 = boto3.resource('s3', endpoint_url=endpoint_url ,aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
  bucket = s3.Bucket(bucket_name)
  return bucket.objects.filter(Prefix=prefix)

def copy_objects(bucket_name, endpoint_url, access_key, secret_key, path, new_path):
  s3 = boto3.resource('s3', endpoint_url=endpoint_url ,aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
  bucket = s3.Bucket(bucket_name)
  
  for obj in bucket.objects.filter(Prefix=path):
    old_source = { 'Bucket': bucket_name,
                   'Key': obj.key}
    # replace the prefix
    new_key = obj.key.replace(path, new_path, 1)
    new_obj = bucket.Object(new_key)
    new_obj.copy(old_source)  
