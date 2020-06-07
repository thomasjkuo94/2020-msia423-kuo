import os
import boto3
import botocore
import logging

logger = logging.getLogger(__file__)

def downloads3(aws_key, secret_key, s3_bucket, s3_bucket_location, output_path):
    '''Downloads raw data from S3 and outputs it in ocal
    
    Args:
        aws_key (str): aws access key
        secret_key (str): aws secret access key
    	s3_bucket (str): name of s3 bucket
        s3_bucket_location (str): location where raw data is located on s3
        output_path (str): where raw data in s3 is output
    Returns:
        None
    '''
    try:
        session = boto3.Session(aws_access_key_id = aws_key, aws_secret_access_key = secret_key)
        s3_client = session.client('s3')
        logger.info("Connection successfully made to S3 bucket")
    except Exception:
        logger.error("Connection could not be made to S3 bucket")
        raise

    try:
        s3_client.download_file(Bucket = s3_bucket, Key = s3_bucket_location, Filename = output_path)
        logger.info("File: {} downloaded successfully from S3".format(output_path))
    except Exception:
        logger.error("File could not be downloaded from S3, please check credentials and paths.")
        raise

