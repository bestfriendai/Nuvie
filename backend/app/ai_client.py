import os
import requests

AI_BASE_URL = os.getenv("AI_BASE_URL")

def get_ai_recommendations(user_id: str, limit: int):
    response = requests.post(
        f"{AI_BASE_URL}/recommend",
        json={
            "user_id": user_id,
            "limit": limit
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()
