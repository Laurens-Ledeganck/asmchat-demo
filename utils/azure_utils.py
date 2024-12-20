import os
import requests
from azure.storage.blob import BlobServiceClient

def list_files_in_directory(directory: str) -> None:
    """Log the list of files in the given directory."""
    if os.path.exists(directory):
        print(f"Files in directory '{directory}':")
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                print(f" - {os.path.join(root, file_name)}")
    else:
        print(f"\n\nDirectory '{directory}' does not exist.\n\n")

def download_files_from_azure(blob_service_client: BlobServiceClient, container_name: str, local_dir: str) -> None:
    """Download files from an Azure Blob Storage container to a local directory."""
    try:
        print(f"\n\nDownloading files from Azure container '{container_name}' to '{local_dir}':\n")
        container_client = blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        for blob in blobs:
            blob_client = container_client.get_blob_client(blob)
            local_file_path = os.path.join(local_dir, blob.name)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, 'wb') as file:
                file.write(blob_client.download_blob().readall())
            print(f"Blob '{blob.name}' downloaded")
        print("")
        list_files_in_directory(local_dir)  # List files after download
        print("")
    except Exception as e:
        raise Exception(f"\n\nError downloading files from Azure: {e}\n")

def upload_parsed_data_to_azure(blob_service_client: BlobServiceClient, container_name: str, local_dir: str) -> None:
    """Upload parsed data from the local directory to Azure Blob Storage."""
    try:
        print(f"\n\nUploading parsed data from '{local_dir}' to Azure container '{container_name}:'\n")
        container_client = blob_service_client.get_container_client(container_name)
        for root, dirs, files in os.walk(local_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                blob_name = os.path.relpath(file_path, local_dir)
                blob_client = container_client.get_blob_client(blob_name)
                with open(file_path, 'rb') as file:
                    blob_client.upload_blob(file, overwrite=True)
                print(f"File '{file_path}' uploaded as blob '{blob_name}'")
        print("\n\n")
    except Exception as e:
        raise Exception(f"\n\nError uploading parsed data to Azure: {e}\n\n")