import uuid

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient # type: ignore
import os

# Use the following Python classes to interact with these resources:
# BlobServiceClient: The BlobServiceClient class allows you to manipulate Azure Storage resources and blob containers.
# ContainerClient: The ContainerClient class allows you to manipulate Azure Storage containers and their blobs.
# BlobClient: The BlobClient class allows you to manipulate Azure Storage blobs.

# 1 - access to the Azure blob service
account_name = os.getenv("ACCOUNT_NAME")
if not account_name:
    raise ValueError("Error - No env var: ACCOUNT_NAME")

account_key = os.getenv("ACCOUNT_KEY")
if not account_key:
    raise ValueError("Error - No env var: ACCOUNT_KEY")

connection_string = (f"DefaultEndpointsProtocol=https;"
                     f"AccountName={account_name};"
                     f"AccountKey={account_key}"
                     "EndpointSuffix=core.windows.net")
service_client = BlobServiceClient.from_connection_string(connection_string)

# 2 - access to the container
container_name = "demo-container"
container_client = service_client.get_container_client(container_name)

if container_client.exists():
    print(f"Container '{container_name}' already exists.")
else:
    try:
        container_client.create_container()
        print(f"Container '{container_name}' created.")
    except ResourceExistsError as exists_error:
        print(f"Container '{container_name}' couldn't be created. Exception: {str(exists_error)}")

# 3 - access to blob client
file_name = "text.txt"
blob_file_name = f"{str(uuid.uuid4())}_{file_name}"
blob_client = container_client.get_blob_client(blob_file_name)

local_file_path = os.path.join(os.getcwd(), file_name)
with open(local_file_path, "rb") as data:
    blob_client.upload_blob(data)

print(f"DONE - File {local_file_path} uploaded to Blob Storage as {blob_file_name}.")