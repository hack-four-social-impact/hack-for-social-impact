from typing import BinaryIO
import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_JSON = os.getenv("GCS_SERVICE_ACCOUNT_JSON")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

def get_bucket():
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.bucket(BUCKET_NAME)
    return bucket

def upload_file(file: BinaryIO, destination_name: str) -> str:
    """
    Upload a file to Google Cloud Storage

    Args:
        file: A file-like object to upload
        destination_name: The name to give the file in GCS

    Returns:
        str: A signed URL to access the uploaded file
    """
    bucket = get_bucket()
    blob = bucket.blob(destination_name)
    blob.upload_from_file(file)
    
    # Generate a signed URL that expires in 1 hour
    url = blob.generate_signed_url(
        version="v4",
        expiration=3600,  # 1 hour
        method="GET"
    )
    return url
