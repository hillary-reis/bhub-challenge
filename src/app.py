import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from bhub.containers import Container
from bhub.docs import custom_openapi
from bhub.middlewares.exception_handler import ExceptionHandlerMiddleware
from bhub.logger import Logger


logger = Logger()


def create_app() -> FastAPI:
    app = FastAPI(openapi_url='/spec')

    app.openapi = custom_openapi
    container = Container()

    from bhub.endpoints.customers import controllers as customers_module
    customers_module.configure(app)

    from bhub.endpoints.bank_data import controllers as bank_data_module
    bank_data_module.configure(app)

    container.wire(modules=[bank_data_module, customers_module])

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                       allow_headers=["*"])
    app.add_middleware(ExceptionHandlerMiddleware)

    app.container = container
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=Config.SERVER_PORT)
