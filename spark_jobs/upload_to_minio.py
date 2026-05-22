from minio import Minio
from minio.error import S3Error
import os

client = Minio(
    endpoint="localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)
bucket_name = "cybersecurity-data"

if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

folders = [
    ("data/raw", "raw"),
    ("data/bronze", "bronze"),
    ("data/silver", "silver"),
    ("data/gold", "gold")
]

def upload_to_minio(local_folder, minio_prefix):
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_folder)
            object_name = f'{minio_prefix}/{relative_path}'.replace("\\", "/")
            # print(f'{local_path}\n{relative_path}\n{object_name}')
            client.fput_object(bucket_name, object_name, local_path)
            print(f"Uploaded: {object_name}")


try:
    for local_folder, minio_prefix in folders:
        if os.path.exists(local_folder):
            upload_to_minio(local_folder, minio_prefix)
        print("Upload to MinIO completed successfully..✅")
except S3Error as e:
    print("MinIO error:", e)
