import logging
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs each request/response and injects a correlation id.

    - Adds X-Request-ID header to every response
    - Logs method, path, status code, duration (ms), and request id
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            # We'll let exception handlers format the response,
            # but we still want timing/logging here.
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "Unhandled exception | %s %s | %.2fms | request_id=%s",
                request.method,
                request.url.path,
                duration_ms,
                request_id,
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s -> %s | %.2fms | request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )

        response.headers["X-Request-ID"] = request_id
        return response
