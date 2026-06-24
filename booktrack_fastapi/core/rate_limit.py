from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import jwt

from booktrack_fastapi.core.settings import Settings

settings = Settings()

def get_user_identifier(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            email = payload.get("sub")
            if email:
                return email
        except Exception:
            pass

    return get_remote_address(request)

limiter = Limiter(
    key_func=get_user_identifier,
    storage_uri=settings.REDIS_URL,
    default_limits=["200/minute"]
)

from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import time

def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    response = JSONResponse(
        {"detail": f"Rate limit exceeded: {exc.detail}"}, status_code=429
    )
    try:
        limiter_instance = request.app.state.limiter
        current_limit = request.state.view_rate_limit
        window_stats = limiter_instance.limiter.get_window_stats(current_limit[0], *current_limit[1])
        reset_in = 1 + window_stats[0]
        response.headers["Retry-After"] = str(max(0, int(reset_in - time.time())))
    except Exception:
        response.headers["Retry-After"] = "60"
        
    return response
