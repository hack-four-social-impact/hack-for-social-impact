from typing import BinaryIO
import os
from dotenv import load_dotenv

load_dotenv()

# Try to import Google Cloud Storage, make it optional
try:
    from google.cloud import storage

    GCS_AVAILABLE = True
except ImportError:
    print("Warning: Google Cloud Storage not available. File upload will be disabled.")
    storage = None
    GCS_AVAILABLE = False

SERVICE_ACCOUNT_JSON = os.getenv("GCS_SERVICE_ACCOUNT_JSON")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


def is_gcs_available() -> bool:
    """Check if Google Cloud Storage is available and configured."""
    return bool(GCS_AVAILABLE and SERVICE_ACCOUNT_JSON and BUCKET_NAME)


def get_bucket():
    if not GCS_AVAILABLE or not storage:
        raise ImportError("Google Cloud Storage is not available")
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
    if not GCS_AVAILABLE:
        raise ImportError("Google Cloud Storage is not available. Please install google-cloud-storage package.")

    bucket = get_bucket()
    blob = bucket.blob(destination_name)
    blob.upload_from_file(file)

    # Generate a signed URL that expires in 1 hour
    url = blob.generate_signed_url(version="v4", expiration=3600, method="GET")  # 1 hour
    return url

def list_files():
    """
    List all files in the Google Cloud Storage bucket

    Returns:
        list: A list of dictionaries containing file information:
            - name: The name of the file
            - size: Size in bytes
            - updated: Last modified timestamp
            - url: Signed URL to access the file
    """
    bucket = get_bucket()
    blobs = bucket.list_blobs()
    
    files = []
    for blob in blobs:
        url = blob.generate_signed_url(
            version="v4",
            expiration=3600,  # 1 hour
            method="GET"
        )
        
        files.append({
            "name": blob.name,
            "size": blob.size,
            "updated": blob.updated.isoformat(),
            "content_type": blob.content_type,
            "url": url
        })
    
    return files
