"""Cloud Tasks enqueue helper for pipeline step execution."""

import json
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def enqueue_step(run_id: str) -> None:
    """Schedule execute_next_step(run_id) on the worker route via Cloud Tasks."""
    from google.cloud import tasks_v2

    settings = get_settings()
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(settings.gcp_project, settings.region, settings.tasks_queue)
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": f"{settings.worker_base_url}/internal/tasks/step",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"run_id": run_id}).encode(),
            "oidc_token": {
                "service_account_email": (
                    f"{settings.gcp_project}@appspot.gserviceaccount.com"
                )
            },
        }
    }
    client.create_task(request={"parent": parent, "task": task})
    logger.info("Enqueued step task for run %s", run_id)
