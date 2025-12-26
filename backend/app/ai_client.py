"""
AI Service Client for Nuvie Backend.

IMPROVEMENTS:
- Fixed function signature to include 'offset' parameter
- Added proper error handling with custom exception
- Added internal token authentication
- Added request_id for tracing
- Added exclude_movie_ids support
- Uses correct endpoint path (/ai/recommend)
"""

import os
import uuid
import logging
from typing import List, Dict, Any, Optional

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

logger = logging.getLogger(__name__)

# Configuration
AI_BASE_URL: str = os.getenv("AI_BASE_URL", "")
AI_INTERNAL_TOKEN: str = os.getenv("AI_INTERNAL_TOKEN", "")
AI_TIMEOUT_SECONDS: int = int(os.getenv("AI_TIMEOUT_SECONDS", "5"))


class AIServiceError(Exception):
    """Custom exception for AI service failures."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def get_ai_recommendations(
    user_id: str,
    limit: int = 20,
    offset: int = 0,
    exclude_movie_ids: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch personalized recommendations from the AI service.

    Args:
        user_id: The user's ID (string, will be converted to int for AI service)
        limit: Maximum number of recommendations (1-50)
        offset: Pagination offset for results
        exclude_movie_ids: Optional list of movie IDs to exclude

    Returns:
        List of recommendation dictionaries containing:
        - movie_id: int
        - score: float
        - rank: int
        - explanation: dict

    Raises:
        AIServiceError: If the AI service is unavailable or returns an error
    """
    if not AI_BASE_URL:
        raise AIServiceError("AI_BASE_URL not configured")

    # Validate and clamp parameters
    limit = max(1, min(limit, 50))
    offset = max(0, offset)

    # Convert user_id to int for AI service (handles UUID strings)
    try:
        # If it's a UUID, hash it to get a numeric ID
        if len(user_id) > 10:
            user_id_int = abs(hash(user_id)) % (10 ** 9)
        else:
            user_id_int = int(user_id)
    except (ValueError, TypeError):
        user_id_int = abs(hash(str(user_id))) % (10 ** 9)

    request_id = str(uuid.uuid4())

    try:
        response = requests.post(
            f"{AI_BASE_URL}/ai/recommend",
            json={
                "request_id": request_id,
                "user_id": user_id_int,
                "limit": limit,
                "offset": offset,
                "exclude_movie_ids": exclude_movie_ids or [],
                "context": {
                    "use_social": True,
                    "seed_movie_ids": [],
                    "locale": "en-US"
                }
            },
            headers={
                "Content-Type": "application/json",
                "X-Internal-Token": AI_INTERNAL_TOKEN,
            },
            timeout=AI_TIMEOUT_SECONDS
        )

        # Handle non-2xx responses
        if response.status_code == 401:
            raise AIServiceError("AI service authentication failed", 401)
        elif response.status_code == 503:
            raise AIServiceError("AI model not ready", 503)
        elif not response.ok:
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                if "detail" in error_data:
                    if isinstance(error_data["detail"], dict):
                        error_detail = error_data["detail"].get("message", str(error_data["detail"]))
                    else:
                        error_detail = str(error_data["detail"])
            except Exception:
                error_detail = response.text[:200] if response.text else "No response body"

            raise AIServiceError(
                f"AI service error: {error_detail}",
                response.status_code
            )

        # Parse response
        data = response.json()
        items = data.get("items", [])

        logger.info(
            f"AI recommendations fetched: request_id={request_id}, "
            f"user_id={user_id}, count={len(items)}, "
            f"latency_ms={data.get('meta', {}).get('latency_ms', 'N/A')}"
        )

        return items

    except Timeout:
        logger.warning(f"AI service timeout: user_id={user_id}")
        raise AIServiceError("AI service timeout", 504)

    except ConnectionError as e:
        logger.error(f"AI service connection error: {e}")
        raise AIServiceError("AI service unavailable", 503)

    except RequestException as e:
        logger.error(f"AI service request error: {e}")
        raise AIServiceError(f"AI service request failed: {str(e)}")

    except AIServiceError:
        raise

    except Exception as e:
        logger.exception(f"Unexpected error calling AI service: {e}")
        raise AIServiceError(f"Unexpected error: {str(e)}")


def get_ai_explanation(
    user_id: str,
    movie_id: int,
) -> Dict[str, Any]:
    """
    Get AI explanation for why a movie was recommended.

    Args:
        user_id: The user's ID
        movie_id: The movie ID to explain

    Returns:
        Explanation dictionary containing:
        - ai_score: int
        - explanation: dict
        - social_signals: dict

    Raises:
        AIServiceError: If the AI service is unavailable or returns an error
    """
    if not AI_BASE_URL:
        raise AIServiceError("AI_BASE_URL not configured")

    try:
        user_id_int = int(user_id) if user_id.isdigit() else abs(hash(user_id)) % (10 ** 9)
    except (ValueError, TypeError):
        user_id_int = abs(hash(str(user_id))) % (10 ** 9)

    request_id = str(uuid.uuid4())

    try:
        response = requests.post(
            f"{AI_BASE_URL}/ai/explain",
            json={
                "request_id": request_id,
                "user_id": user_id_int,
                "movie_id": movie_id,
                "context": {"use_social": True}
            },
            headers={
                "Content-Type": "application/json",
                "X-Internal-Token": AI_INTERNAL_TOKEN,
            },
            timeout=AI_TIMEOUT_SECONDS
        )

        response.raise_for_status()
        return response.json()

    except RequestException as e:
        logger.error(f"AI explanation request error: {e}")
        raise AIServiceError(f"Failed to get explanation: {str(e)}")
