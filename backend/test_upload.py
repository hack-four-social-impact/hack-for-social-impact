import os
from gcs_client import upload_file
from dotenv import load_dotenv

load_dotenv()

# Test file creation
test_content = "Hello, this is a test file"
with open("test.txt", "w") as f:
    f.write(test_content)

# Test upload
try:
    with open("test.txt", "rb") as f:
        url = upload_file(f, "test.txt")
        print(f"File uploaded successfully! Public URL: {url}")
except Exception as e:
    print(f"Error uploading file: {str(e)}")
finally:
    # Clean up test file
    if os.path.exists("test.txt"):
        os.remove("test.txt")
