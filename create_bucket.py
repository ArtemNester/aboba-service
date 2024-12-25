import json

from minio import Minio
from minio.error import S3Error


def create_bucket_and_upload_file():
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False,
    )

    bucket_name = "memes"
    file_path = "rik-roll.mp4"
    object_name = "rik-roll.mp4"

    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

        # Upload the file
        client.fput_object(bucket_name, object_name, file_path)
        print(
            f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.",
        )

        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                },
            ],
        }
        client.set_bucket_policy(bucket_name, json.dumps(public_policy))
        print(f"Bucket '{bucket_name}' made public.")

    except S3Error as err:
        print(f"Error occurred: {err}")


if __name__ == "__main__":
    create_bucket_and_upload_file()
