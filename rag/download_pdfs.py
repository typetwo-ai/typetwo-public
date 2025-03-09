import os

import google.auth
from google.cloud import storage

os.environ["GOOGLE_CLOUD_PROJECT"] = "project-1-450712"

credentials, project = google.auth.default()


def download_folder(bucket_name, folder_name, local_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_name)

    for blob in blobs:
        if blob.name.endswith('/'):
            continue

        relative_path = blob.name[len(folder_name):]

        local_file_path = f"{local_path}/{relative_path}"
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        blob.download_to_filename(local_file_path)
        print(f"Downloaded {blob.name} to {local_file_path}")


# Usage
download_folder('literature-resources-bucket', 'Journal of Medicinal Chemistry/', './data/')
