import logging
from typing import Optional

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from dotenv import dotenv_values

from app.api.schemas.invoice import Invoice
from app.api.schemas.invoice_sign_responses import (
    InvoiceSignResultBlock,
    build_invoice_sign_problem,
    invoice_sign_problem_response,
    invoice_sign_success_response,
)
from app.application.dto.sign_invoice_output import SignInvoiceOutputDto
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
        access_key = service_result.access_key
        is_received = service_result.is_received
        is_authorized = service_result.is_authorized
        xml_signed_value = service_result.xml_signed_value

        if service_result.is_success:
            return invoice_sign_success_response(
                access_key=access_key,
                is_received=is_received,
                is_authorized=is_authorized,
                xml_file_signed=xml_signed_value,
            )

        if service_result.error_code == 'signing_error':
            return invoice_sign_problem_response(
                build_invoice_sign_problem(
                    status_code=500,
                    error_code='signing_error',
                    title='Error al firmar el XML',
                    detail=(
                        'Error al firmar el XML. Verifique el certificado, contraseña y formato del XML.'
                    ),
                    instance=instance,
                    result=InvoiceSignResultBlock(
                        access_key=access_key,
                        is_received=None,
                        is_authorized=None,
                        xml_file_signed=None,
                    ),
                ))

        if service_result.error_code == 'reception_error':
            return invoice_sign_problem_response(
                build_invoice_sign_problem(
                    status_code=502,
                    error_code='reception_error',
                    title='El SRI no recibió el comprobante',
                    detail=(
                        'El XML fue firmado pero no fue recibido por el SRI. Verifique la conexión '
                        'y el formato del XML.'
                    ),
                    instance=instance,
                    result=InvoiceSignResultBlock(
                        access_key=access_key,
                        is_received=False,
                        is_authorized=False,
                        xml_file_signed=None,
                    ),
                ))

        if service_result.error_code == 'authorization_error':
            return invoice_sign_problem_response(
                build_invoice_sign_problem(
                    status_code=422,
                    error_code='authorization_error',
                    title='El SRI no autorizó el comprobante',
                    detail='El XML fue recibido pero no fue autorizado por el SRI.',
                    instance=instance,
                    result=InvoiceSignResultBlock(
                        access_key=access_key,
                        is_received=True,
                        is_authorized=False,
                        xml_file_signed=None,
                    ),
                ))

        raise RuntimeError(f"Unsupported service error code: {service_result.error_code}")

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
