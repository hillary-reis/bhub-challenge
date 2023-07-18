from uuid import uuid4

from fastapi import APIRouter, Depends, Request, FastAPI
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from starlette import status

from bhub.logger import Logger

from bhub.containers import Container
from bhub.endpoints.customers.schemas import (CustomersCreatePayload, CustomersCreateResponse,
                                              CustomersGetByUuidResponse, CustomersUpdatePayload)
from bhub.endpoints.customers.use_cases.customers_create import CustomersCreateUseCase
from bhub.endpoints.customers.use_cases.customers_delete_by_uuid import CustomersDeleteByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_get_by_uuid import CustomersGetByUuidUseCase
from bhub.endpoints.customers.use_cases.customers_update_by_uuid import CustomersUpdateByUuidUseCase
from bhub.endpoints.exceptions import CustomerAlreadyExistsException, CustomerNotFoundException


router = APIRouter()


@router.post('/v1/customers', tags=['customers'], status_code=status.HTTP_201_CREATED)
@inject
async def customers_create(
    request: Request, schema: CustomersCreatePayload,
    customers_create_use_case: CustomersCreateUseCase = Depends(Provide[Container.customers_create_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> CustomersCreateResponse:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))

        logger.info(f'[{tracking_id}] starting create customers')
        logger.info(f'[{tracking_id}] schema: {schema}')

        return await customers_create_use_case.run(tracking_id=tracking_id, schema=schema)

    except CustomerAlreadyExistsException as exception:
        logger.exception(f'[{tracking_id}] Conflict: {type(exception).__name__}: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while create customer: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while create customer'})


@router.get('/v1/customers/{customer_uuid}', tags=['customers'], status_code=status.HTTP_200_OK)
@inject
async def customers_get_by_uuid(
    request: Request, customer_uuid: str,
    customers_get_by_uuid_use_case: CustomersGetByUuidUseCase = Depends(Provide[
        Container.customers_get_by_uuid_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> CustomersGetByUuidResponse:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))
        logger.info(f'[{tracking_id}] starting get customer {customer_uuid}')

        return await customers_get_by_uuid_use_case.run(tracking_id=tracking_id, customer_uuid=customer_uuid)

    except CustomerNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Customer not found: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while get customer: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while get customer'})


@router.patch('/v1/customers/{customer_uuid}', tags=['customers'], status_code=status.HTTP_200_OK)
@inject
async def customers_update_by_uuid(
    request: Request, customer_uuid: str, schema: CustomersUpdatePayload,
    customers_update_by_uuid_use_case: CustomersUpdateByUuidUseCase = Depends(Provide[
        Container.customers_update_by_uuid_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> dict:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))
        logger.info(f'[{tracking_id}] starting get customer {customer_uuid}')

        await customers_update_by_uuid_use_case.run(tracking_id=tracking_id, customer_uuid=customer_uuid, schema=schema)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Customer successfully updated'})

    except CustomerNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Customer not found: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while update customer: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while update customer'})


@router.delete('/v1/customers/{customer_uuid}', tags=['customers'], status_code=status.HTTP_200_OK)
@inject
async def customers_delete_by_uuid(
    request: Request, customer_uuid: str,
    customers_delete_by_uuid_use_case: CustomersDeleteByUuidUseCase = Depends(Provide[
        Container.customers_delete_by_uuid_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> dict:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))
        logger.info(f'[{tracking_id}] starting get customer {customer_uuid}')

        await customers_delete_by_uuid_use_case.run(tracking_id=tracking_id, customer_uuid=customer_uuid)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Customer successfully deleted'})

    except CustomerNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Customer not found: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while delete customer: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while delete customer'})


def configure(app: FastAPI):
    app.include_router(router)
