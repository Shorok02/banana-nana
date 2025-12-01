# auth/google_verify.py
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "1053522225541-mjtajva9itdoqk9rldeqdscs0171a7bp.apps.googleusercontent.com"

def verify_google_token(token: str):
    try:
        payload = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        return payload["sub"]  # unique Google user ID
    except Exception:
        return None
