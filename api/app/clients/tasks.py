"""Cloud Tasks enqueue helper for pipeline step execution."""

import json
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def enqueue_step(run_id: str) -> None:
    """Schedule execute_next_step(run_id) on the worker route via Cloud Tasks."""
    from google.cloud import tasks_v2

    from app.routes.internal_tasks import step_url, task_service_account

    settings = get_settings()
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(settings.gcp_project, settings.region, settings.tasks_queue)
    url = step_url()
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"run_id": run_id}).encode(),
            # The worker verifies this token: audience must be the exact URL and
            # the email must be this service account (app.routes.internal_tasks).
            "oidc_token": {"service_account_email": task_service_account(), "audience": url},
        }
    }
    client.create_task(request={"parent": parent, "task": task})
    logger.info("Enqueued step task for run %s", run_id)
