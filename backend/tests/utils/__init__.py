import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.models.user import User
from app.core.security import create_access_token

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    if r.status_code != 200:
        raise Exception(f"Login failed: {r.text}")
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers 