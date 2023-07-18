from uuid import uuid4

from fastapi import APIRouter, Depends, Request, FastAPI
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from starlette import status

from bhub.logger import Logger

from bhub.containers import Container
from bhub.endpoints.bank_data.schemas import (BankDataCreatePayload, BankDataCreateResponse,
                                              BankDataGetByUuidResponse, BankDataUpdatePayload)
from bhub.endpoints.bank_data.use_cases.bank_data_create import BankDataCreateUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_delete_by_uuid import BankDataDeleteByUuidUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_get_by_uuid import BankDataGetByUuidUseCase
from bhub.endpoints.bank_data.use_cases.bank_data_update_by_uuid import BankDataUpdateByUuidUseCase
from bhub.endpoints.exceptions import (BankDataAlreadyExistsException, BankDataNotFoundException,
                                       CustomerNotFoundException)


router = APIRouter()


@router.post('/v1/bank-data', tags=['bank-data'], status_code=status.HTTP_201_CREATED)
@inject
async def bank_data_create(
    request: Request, schema: BankDataCreatePayload,
    bank_data_create_use_case: BankDataCreateUseCase = Depends(Provide[Container.bank_data_create_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> BankDataCreateResponse:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))

        logger.info(f'[{tracking_id}] starting create bank data')
        logger.info(f'[{tracking_id}] schema: {schema}')

        return await bank_data_create_use_case.run(tracking_id=tracking_id, schema=schema)

    except CustomerNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Customer not found: {type(exception).__name__}: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except BankDataAlreadyExistsException as exception:
        logger.exception(f'[{tracking_id}] Conflict: {type(exception).__name__}: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while create bank data: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while create bank data'})


@router.get('/v1/bank-data/{bank_data_uuid}', tags=['bank-data'], status_code=status.HTTP_200_OK)
@inject
async def bank_data_get_by_uuid(
    request: Request, bank_data_uuid: str,
    bank_data_get_by_uuid_use_case: BankDataGetByUuidUseCase = Depends(Provide[
        Container.bank_data_get_by_uuid_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> BankDataGetByUuidResponse:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))
        logger.info(f'[{tracking_id}] starting get bank data {bank_data_uuid}')

        return await bank_data_get_by_uuid_use_case.run(tracking_id=tracking_id, bank_data_uuid=bank_data_uuid)

    except BankDataNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Bank data not found: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while get bank data: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while get bank data'})


@router.patch('/v1/bank-data/{bank_data_uuid}', tags=['bank-data'], status_code=status.HTTP_200_OK)
@inject
async def bank_data_update_by_uuid(
    request: Request, bank_data_uuid: str, schema: BankDataUpdatePayload,
    bank_data_update_by_uuid_use_case: BankDataUpdateByUuidUseCase = Depends(Provide[
        Container.bank_data_update_by_uuid_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> dict:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))
        logger.info(f'[{tracking_id}] starting get bank data {bank_data_uuid}')

        await bank_data_update_by_uuid_use_case.run(tracking_id=tracking_id, bank_data_uuid=bank_data_uuid,
                                                    schema=schema)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Bank data successfully updated'})

    except BankDataNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Bank data not found: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while update bank data: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while update bank data'})


@router.delete('/v1/bank-data/{bank_data_uuid}', tags=['bank-data'], status_code=status.HTTP_200_OK)
@inject
async def bank_data_delete_by_uuid(
    request: Request, bank_data_uuid: str,
    bank_data_delete_by_uuid_use_case: BankDataDeleteByUuidUseCase = Depends(Provide[
        Container.bank_data_delete_by_uuid_use_case]),
    logger: Logger = Depends(Provide[Container.logger])
) -> dict:
    try:
        tracking_id = request.headers.get('requestId', str(uuid4()))
        logger.info(f'[{tracking_id}] starting get bank data {bank_data_uuid}')

        await bank_data_delete_by_uuid_use_case.run(tracking_id=tracking_id, bank_data_uuid=bank_data_uuid)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Bank data successfully deleted'})

    except BankDataNotFoundException as exception:
        logger.exception(f'[{tracking_id}] Bank data not found: {exception.args[0]}')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'title': exception.args[0]['title'], 'detail': exception.args[0]['detail']})

    except Exception as exception:
        logger.exception(f'[{tracking_id}] Error while delete bank data: {exception.args}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'title': 'Internal error', 'detail': 'Error while delete bank data'})


def configure(app: FastAPI):
    app.include_router(router)
