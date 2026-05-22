from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
import traceback


async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
