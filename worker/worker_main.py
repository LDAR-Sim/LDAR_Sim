"""SQS polling loop — the entry point for the LDAR-Sim worker.

Environment variables required:
    LDAR_SIM_QUEUE_URL      - AWS SQS queue URL
    LDAR_SIM_S3_BUCKET      - S3 bucket name for input files
    LDAR_SIM_API_BASE_URL   - Base URL of the NestJS API (e.g. http://api:3999)
    LDAR_SIM_INTERNAL_TOKEN - Bearer token for the internal NestJS endpoint
    AWS_REGION              - AWS region (default: us-east-1)

Optional:
    LDAR_SIM_POLL_WAIT_SECONDS  - SQS long-poll wait (default: 20)
    LDAR_SIM_MAX_MESSAGES       - Messages per poll (default: 1)
    LDAR_SIM_VISIBILITY_TIMEOUT - SQS visibility timeout in seconds (default: 7200)
"""
import json
import logging
import os
import signal
import sys
import time

import boto3

from job_handler import handle_job

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("worker_main")

_QUEUE_URL = os.environ.get("LDAR_SIM_QUEUE_URL", "")
_REGION = os.environ.get("AWS_REGION", "us-east-1")
_POLL_WAIT = int(os.environ.get("LDAR_SIM_POLL_WAIT_SECONDS", "20"))
_MAX_MESSAGES = int(os.environ.get("LDAR_SIM_MAX_MESSAGES", "1"))
_VISIBILITY_TIMEOUT = int(os.environ.get("LDAR_SIM_VISIBILITY_TIMEOUT", "7200"))

_shutdown_requested = False


def _request_shutdown(signum, frame):
    global _shutdown_requested
    logger.info("Shutdown signal received — will stop after current job")
    _shutdown_requested = True


def _delete_message(sqs, receipt_handle: str) -> None:
    try:
        sqs.delete_message(QueueUrl=_QUEUE_URL, ReceiptHandle=receipt_handle)
        logger.info("Deleted message %s", receipt_handle[:20])
    except Exception as exc:
        logger.error("Failed to delete message: %s", exc)


def poll_once(sqs) -> int:
    """Poll for messages and process them. Returns number processed."""
    resp = sqs.receive_message(
        QueueUrl=_QUEUE_URL,
        MaxNumberOfMessages=_MAX_MESSAGES,
        WaitTimeSeconds=_POLL_WAIT,
        VisibilityTimeout=_VISIBILITY_TIMEOUT,
        MessageAttributeNames=["All"],
    )
    messages = resp.get("Messages", [])
    if not messages:
        return 0

    for msg in messages:
        receipt_handle = msg["ReceiptHandle"]
        try:
            body = json.loads(msg["Body"])
            logger.info("Processing message for run %s", body.get("runId"))
            handle_job(body)
            _delete_message(sqs, receipt_handle)
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in SQS message: %s — deleting", exc)
            _delete_message(sqs, receipt_handle)
        except Exception as exc:
            # Leave message invisible until visibility timeout expires for retry
            logger.error("Job failed — message will become visible again: %s", exc)

    return len(messages)


def run() -> None:
    if not _QUEUE_URL:
        logger.critical("LDAR_SIM_QUEUE_URL is not set — exiting")
        sys.exit(1)

    signal.signal(signal.SIGTERM, _request_shutdown)
    signal.signal(signal.SIGINT, _request_shutdown)

    sqs = boto3.client("sqs", region_name=_REGION)
    logger.info("Worker started — polling %s", _QUEUE_URL)

    while not _shutdown_requested:
        try:
            poll_once(sqs)
        except Exception as exc:
            logger.error("Unexpected poll error: %s — sleeping 5s", exc, exc_info=True)
            time.sleep(5)

    logger.info("Worker shut down cleanly")


if __name__ == "__main__":
    run()
