import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "omnidocs-bucket")
S3_REGION = os.getenv("S3_REGION", "us-east-1")

# Create S3 client
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=S3_REGION
    )
except Exception as e:
    print(f"Error creating S3 client: {e}")
    s3_client = None