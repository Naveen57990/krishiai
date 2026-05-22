from fastapi import Request
from loguru import logger
import time


async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} {response.status_code} {process_time:.0f}ms")
    response.headers["X-Process-Time-MS"] = str(int(process_time))
    return response
