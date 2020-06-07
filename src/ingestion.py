import os
import gzip
import requests
import logging
import boto3
from botocore.exceptions import ClientError

def fetch_zipfile(url):
    '''Downloads a file and writes it to current directory
    
    Args:
        url (str): the url to the file to be downloaded
    Returns:
        None
    '''
    filename = url.split("/")[-1]
    
    with open(filename, "wb") as f:
        r = requests.get(url)
        f.write(r.content)

def gunzip(source_filepath, dest_filepath, block_size=65536):
    '''Unzips a gzipped file

    Args:
        source_filepath (str): the filepath of the gzipped file
        dest_filepath (str): the filepath of the unzipped file
        block_size (int): blocks to read
    Returns:
        None
    '''
    with gzip.open(source_filepath, 'rb') as s_file, open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)
        d_file.write(block)

def upload_file_s3(file_name, bucket, aws_access_key, aws_secret_key, s3_object_name = None):
    '''Uploads a file to an S3 bucket
    Args:
        file_name (str): the file name of the file to upload into S3
        bucket (str): the bucket name of the file to upload into S3
        aws_access_key: s3 access key related to specified credentials
        aws_secret_key: s3 secret access key related to specified credentials
        s3_object_name (str): the S3 object name to upload into s3
    '''
    session = boto3.Session(aws_access_key_id = aws_access_key, aws_secret_access_key = aws_secret_key)
    s3_client = session.client('s3')

    #Use the file_name as the s3_object_name if not specified
    if s3_object_name is None:
        s3_object_name = file_name

    #upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, s3_object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True






