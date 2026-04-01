import json

from flask import current_app
from minio import Minio


def get_minio_client() -> Minio:
    return Minio(
        endpoint=current_app.config["MINIO_ENDPOINT"],
        access_key=current_app.config["MINIO_ACCESS_KEY"],
        secret_key=current_app.config["MINIO_SECRET_KEY"],
        secure=current_app.config["MINIO_SECURE"],
    )


def ensure_public_bucket() -> None:
    client = get_minio_client()
    bucket_name = current_app.config["MINIO_BUCKET"]

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["s3:GetObject"],
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
            }
        ],
    }
    client.set_bucket_policy(bucket_name, json.dumps(policy))
