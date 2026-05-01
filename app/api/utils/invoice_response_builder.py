from starlette.responses import JSONResponse

from app.api.schemas.invoice_sign_responses import (
    InvoiceSignResultBlock,
    build_invoice_sign_problem,
    invoice_sign_problem_response,
    invoice_sign_success_response,
)
from app.application.dto.sign_invoice_output import SignInvoiceOutputDto


def build_response_from_service_result(
    service_result: SignInvoiceOutputDto,
    instance: str,
) -> JSONResponse:
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

    if service_result.error_code == 'invalid_retry_payload':
        return invoice_sign_problem_response(
            build_invoice_sign_problem(
                status_code=400,
                error_code='invalid_retry_payload',
                title='Parámetros inválidos para reintento',
                detail=(
                    'Para retryMode=full debe enviar invoice; para retryMode=authorization_only '
                    'debe enviar accessKey.'
                ),
                instance=instance,
                result=InvoiceSignResultBlock(
                    access_key=access_key,
                    is_received=is_received,
                    is_authorized=is_authorized,
                    xml_file_signed=None,
                ),
            ))

    if service_result.error_code == 'invalid_retry_mode':
        return invoice_sign_problem_response(
            build_invoice_sign_problem(
                status_code=400,
                error_code='invalid_retry_mode',
                title='Modo de reintento inválido',
                detail='retryMode debe ser full o authorization_only.',
                instance=instance,
                result=InvoiceSignResultBlock(
                    access_key=access_key,
                    is_received=is_received,
                    is_authorized=is_authorized,
                    xml_file_signed=None,
                ),
            ))

    raise RuntimeError(f"Unsupported service error code: {service_result.error_code}")
