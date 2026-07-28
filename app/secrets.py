# app/secrets.py
"""Secure Secret Management System.

Integrates with Google Cloud Secret Manager to inject API keys and credentials
at runtime without hardcoding sensitive strings in code.
"""

import os

from google.cloud import secretmanager

from app.logger import logger


def get_secret(secret_id: str, default: str | None = None) -> str | None:
    """Retrieve a secret version value from Google Cloud Secret Manager or environment.

    Args:
        secret_id: Secret identifier (e.g. 'YFINANCE_API_KEY', 'GEMINI_API_KEY').
        default: Fallback default value if secret is not set.

    Returns:
        Secret string or fallback default value.
    """
    # 1. Check environment variables first
    env_val = os.environ.get(secret_id)
    if env_val:
        return env_val

    # 2. Check GCP Secret Manager if GOOGLE_CLOUD_PROJECT is set
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            payload = response.payload.data.decode("UTF-8")
            logger.info("Retrieved secret from Secret Manager", secret_id=secret_id)
            return payload
        except Exception as err:
            logger.warning("Could not fetch secret from Secret Manager", secret_id=secret_id, error=str(err))

    return default
