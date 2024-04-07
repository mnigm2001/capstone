import os, boto3
from dotenv import load_dotenv

def setup_aws_client(service_name='rekognition', region_name='us-east-2'):
    """
    Initializes and returns an AWS client for a given service using credentials from a .env file.
    
    :param service_name: Name of the AWS service for the client.
    :param region_name: AWS region name.
    :return: Initialized AWS service client.
    :raises ValueError: If AWS credentials are not found in the environment.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve AWS credentials from environment variables
    access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not access_key_id or not secret_access_key:
        raise ValueError("AWS credentials not found in environment variables.")

    return boto3.client(service_name, aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key, region_name=region_name)
