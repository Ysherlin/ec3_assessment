import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app.errors")


def _get_request_id(request: Request) -> Optional[str]:
    return getattr(getattr(request, "state", None), "request_id", None)


def _error_payload(
    *,
    message: str,
    request_id: Optional[str],
    details: Any = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "error": message,
        "request_id": request_id,
    }
    if details is not None:
        payload["details"] = details
    return payload


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers so:
    - errors return consistent JSON
    - we avoid plain-text 500s
    - database errors don't leak internals
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = _get_request_id(request)
        # StarletteHTTPException.detail may be string or object
        logger.warning(
            "HTTPException %s | path=%s | request_id=%s | detail=%s",
            exc.status_code,
            request.url.path,
            request_id,
            exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(
                message="Request failed",
                request_id=request_id,
                details=exc.detail,
            ),
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        request_id = _get_request_id(request)
        logger.exception(
            "Database error | path=%s | request_id=%s",
            request.url.path,
            request_id,
        )
        # Don't leak DB internals to clients
        return JSONResponse(
            status_code=500,
            content=_error_payload(
                message="Database error",
                request_id=request_id,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        request_id = _get_request_id(request)
        logger.exception(
            "Unhandled error | path=%s | request_id=%s",
            request.url.path,
            request_id,
        )
        return JSONResponse(
            status_code=500,
            content=_error_payload(
                message="Internal server error",
                request_id=request_id,
            ),
        )
