from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from bhub.logger import Logger


logger = Logger()


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exception:
            logger.exception(f'An Error occurred during the process: {exception}')
            return JSONResponse(status_code=500, content="A Error occurred during the process, please check the logs")
