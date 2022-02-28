import time
from typing import Any, Dict

import jwt
from environs import Env

env = Env()
env.read_env()

JWT_SECRET = env.str("JWT_SECRET")
JWT_ALGORITM = env.str("JWT_ALGORITM")


def token_response(token: str) -> dict:
    return {"access_token": token}


def signJWT(user_id: str) -> Dict[str, Any]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITM],
        )
        return decoded_token if decoded_token["expires"] >= time.time() else {}
    except jwt.DecodeError:
        return {}
