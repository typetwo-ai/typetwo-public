import os
from tqdm import tqdm
from google.cloud import storage


def download_folder(bucket_name, folder_path, local_destination):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)

    for blob in tqdm(blobs):
        if blob.name.endswith('/'):
            continue

        relative_path = blob.name[len(folder_path):]

        local_path = f"{local_destination}/{relative_path}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        blob.download_to_filename(local_path)
