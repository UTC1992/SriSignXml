import logging
from typing import Optional

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from dotenv import dotenv_values

from app.api.schemas.invoice import Invoice, RetryInvoiceRequest
from app.api.schemas.invoice_sign_responses import (
    InvoiceSignResultBlock,
    build_invoice_sign_problem,
    invoice_sign_problem_response,
)
from app.api.utils.invoice_response_builder import build_response_from_service_result
from app.application.dto.sign_invoice_output import SignInvoiceOutputDto
from app.application.services.retry_invoice_service import execute_retry_invoice
from app.application.services.sign_invoice_service import execute_sign_invoice

router_invoice = APIRouter()
config = {
    **dotenv_values('.env')
}


@router_invoice.post("/invoice/sign", tags=['Invoice'])
async def sign_invoice(invoice: Invoice, request: Request) -> JSONResponse:
    access_key: Optional[str] = None
    is_received: Optional[bool] = None
    is_authorized: Optional[bool] = None
    xml_signed_value: Optional[str] = None
    instance = str(request.url)

    try:
        # Execute application service.
        service_result: SignInvoiceOutputDto = await execute_sign_invoice(
            invoice=invoice,
            config=config,
        )
        return build_response_from_service_result(
            service_result=service_result,
            instance=instance,
        )

    except FileNotFoundError as e:
        return invoice_sign_problem_response(
            build_invoice_sign_problem(
                status_code=404,
                error_code='file_not_found',
                title='Recurso no encontrado',
                detail=(
                    f'Archivo no encontrado: {str(e)}. Verifique que el certificado .p12 '
                    'y el JAR de firma estén en su lugar.'
                ),
                instance=instance,
                result=InvoiceSignResultBlock(
                    access_key=access_key,
                    is_received=is_received,
                    is_authorized=is_authorized,
                    xml_file_signed=xml_signed_value,
                ),
            ))
    except Exception as e:
        logging.critical('Error inesperado en el endpoint /invoice/sign: %s' % str(e))
        return invoice_sign_problem_response(
            build_invoice_sign_problem(
                status_code=500,
                error_code='internal_error',
                title='Error interno del servidor',
                detail='Error interno del servidor. Contacte al administrador.',
                instance=instance,
                result=InvoiceSignResultBlock(
                    access_key=access_key,
                    is_received=is_received,
                    is_authorized=is_authorized,
                    xml_file_signed=xml_signed_value,
                ),
                internal_detail=str(e),
            ))


@router_invoice.post("/invoice/retry", tags=['Invoice'])
async def retry_invoice(retry_request: RetryInvoiceRequest, request: Request) -> JSONResponse:
    access_key: Optional[str] = None
    is_received: Optional[bool] = None
    is_authorized: Optional[bool] = None
    xml_signed_value: Optional[str] = None
    instance = str(request.url)

    try:
        service_result: SignInvoiceOutputDto = await execute_retry_invoice(
            retry_request=retry_request,
            config=config,
        )
        # values to build response in exceptions
        access_key = service_result.access_key
        is_received = service_result.is_received
        is_authorized = service_result.is_authorized
        xml_signed_value = service_result.xml_signed_value
        
        return build_response_from_service_result(
            service_result=service_result,
            instance=instance,
        )
    except FileNotFoundError as e:
        return invoice_sign_problem_response(
            build_invoice_sign_problem(
                status_code=404,
                error_code='file_not_found',
                title='Recurso no encontrado',
                detail=(
                    f'Archivo no encontrado: {str(e)}. Verifique que el certificado .p12 '
                    'y el JAR de firma estén en su lugar.'
                ),
                instance=instance,
                result=InvoiceSignResultBlock(
                    access_key=access_key,
                    is_received=is_received,
                    is_authorized=is_authorized,
                    xml_file_signed=xml_signed_value,
                ),
            ))
    except Exception as e:
        logging.critical('Error inesperado en el endpoint /invoice/retry: %s' % str(e))
        return invoice_sign_problem_response(
            build_invoice_sign_problem(
                status_code=500,
                error_code='internal_error',
                title='Error interno del servidor',
                detail='Error interno del servidor. Contacte al administrador.',
                instance=instance,
                result=InvoiceSignResultBlock(
                    access_key=access_key,
                    is_received=is_received,
                    is_authorized=is_authorized,
                    xml_file_signed=xml_signed_value,
                ),
                internal_detail=str(e),
            ))
