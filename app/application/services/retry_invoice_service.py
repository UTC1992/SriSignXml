from typing import Mapping, Optional

from app.api.schemas.invoice import Invoice, RetryInvoiceRequest
from app.application.dto.sign_invoice_output import SignInvoiceOutputDto
from app.application.services.sign_invoice_service import execute_sign_invoice
from app.infrastructure.sri.sri_service import send_access_key_to_authorization


async def execute_retry_invoice(
    retry_request: RetryInvoiceRequest,
    config: Mapping[str, Optional[str]],
) -> SignInvoiceOutputDto:
    if retry_request.retryMode == "full":
        if retry_request.invoice is None:
            return SignInvoiceOutputDto(
                is_success=False,
                error_code="invalid_retry_payload",
            )
        return await execute_sign_invoice(
            invoice=retry_request.invoice,
            config=config,
        )

    if retry_request.retryMode == "authorization_only":
        if not retry_request.accessKey:
            return SignInvoiceOutputDto(
                is_success=False,
                error_code="invalid_retry_payload",
            )

        url_authorization = config["URL_AUTHORIZATION"]
        response_authorization = await send_access_key_to_authorization(
            access_key=retry_request.accessKey,
            url_to_authorization=url_authorization,
        )
        is_authorized = response_authorization["isValid"]
        xml_signed_value = response_authorization["xml"]

        if not is_authorized:
            return SignInvoiceOutputDto(
                is_success=False,
                access_key=retry_request.accessKey,
                is_received=True,
                is_authorized=False,
                error_code="authorization_error",
            )

        return SignInvoiceOutputDto(
            is_success=True,
            access_key=retry_request.accessKey,
            is_received=True,
            is_authorized=True,
            xml_signed_value=xml_signed_value,
        )

    return SignInvoiceOutputDto(
        is_success=False,
        error_code="invalid_retry_mode",
    )
