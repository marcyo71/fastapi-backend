import time
import logging
import traceback
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("backend")

# -----------------------------------
# REQUEST LOGGING MIDDLEWARE
# -----------------------------------
class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000

        logger.info(
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} | {duration:.2f} ms"
        )

        return response


# -----------------------------------
# ERROR HANDLER MIDDLEWARE
# -----------------------------------
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            error_trace = traceback.format_exc()
            logger.error(f"Unhandled error: {exc}\n{error_trace}")

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "detail": str(exc)
                }
            )
