"""HTTP client for communicating with the NestJS internal API."""
import logging
import os

import requests

logger = logging.getLogger(__name__)

_API_BASE_URL = os.environ.get("LDAR_SIM_API_BASE_URL", "http://localhost:3999")
_API_TOKEN = os.environ.get("LDAR_SIM_INTERNAL_TOKEN", "")


def _headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if _API_TOKEN:
        headers["Authorization"] = f"Bearer {_API_TOKEN}"
    return headers


def patch_run_status(run_id: int, status: str, error_message: str = None) -> None:
    """Update the run status on the NestJS API."""
    url = f"{_API_BASE_URL}/ldar-sim/runs/{run_id}/results"
    # We reuse the results endpoint with a partial payload for status-only updates
    # via a dedicated PATCH approach — but since the plan uses POST for results,
    # we handle status changes via the /results POST with empty result arrays.
    # For a pure status-only update we call a simpler approach:
    payload = {
        "status": status,
    }
    if error_message:
        payload["errorMessage"] = error_message

    try:
        resp = requests.patch(
            f"{_API_BASE_URL}/ldar-sim/runs/{run_id}/status",
            json=payload,
            headers=_headers(),
            timeout=30,
        )
        resp.raise_for_status()
        logger.info("Run %d status updated to %s", run_id, status)
    except requests.RequestException as exc:
        logger.error("Failed to update run %d status: %s", run_id, exc)
        raise


def post_results(run_id: int, results: dict) -> None:
    """POST parsed simulation results to the NestJS API."""
    url = f"{_API_BASE_URL}/ldar-sim/runs/{run_id}/results"
    logger.info(
        "Posting results for run %d: %d timeseries, %d leaks, %d sites",
        run_id,
        len(results.get("timeseries", [])),
        len(results.get("leaks", [])),
        len(results.get("sites", [])),
    )
    try:
        resp = requests.post(
            url,
            json=results,
            headers=_headers(),
            timeout=120,
        )
        resp.raise_for_status()
        logger.info("Results for run %d posted successfully", run_id)
    except requests.RequestException as exc:
        logger.error("Failed to post results for run %d: %s", run_id, exc)
        raise
