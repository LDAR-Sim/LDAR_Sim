"""Download input files from S3 to a local directory."""
import os
import logging

import boto3

logger = logging.getLogger(__name__)


def download_file(bucket: str, key: str, dest_path: str) -> str:
    """Download a single S3 object to *dest_path* and return the local path."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    s3 = boto3.client("s3")
    logger.info("Downloading s3://%s/%s → %s", bucket, key, dest_path)
    s3.download_file(bucket, key, dest_path)
    return dest_path


def download_input_files(
    bucket: str,
    infrastructure_key: str,
    weather_key: str,
    dest_dir: str,
) -> dict:
    """Download all required input files and return a mapping of role → local path."""
    infrastructure_path = os.path.join(
        dest_dir, os.path.basename(infrastructure_key)
    )
    weather_path = os.path.join(dest_dir, os.path.basename(weather_key))

    download_file(bucket, infrastructure_key, infrastructure_path)
    download_file(bucket, weather_key, weather_path)

    return {
        "infrastructure_file": infrastructure_path,
        "weather_file": weather_path,
    }
