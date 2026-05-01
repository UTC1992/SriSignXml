import os
import random
from typing import Mapping, Optional

import aiofiles

from app.api.schemas.invoice import InfoToSignXml, Invoice
from app.application.dto.sign_invoice_output import SignInvoiceOutputDto
from app.infrastructure.signing.signing_service import sign_invoice_xml
from app.infrastructure.sri.sri_service import (
    send_access_key_to_authorization,
    send_signed_xml_to_reception,
)
from app.infrastructure.temp_files_service import (
    create_temp_binary_file,
    create_temp_xml_file,
)
from app.infrastructure.xml.xml_service import create_invoice_xml
from app.utils.create_access_key import createAccessKey


async def execute_sign_invoice(
    invoice: Invoice,
    config: Mapping[str, Optional[str]],
) -> SignInvoiceOutputDto:
    # Create access key.
    random_number = str(random.randint(1, 99999999)).zfill(8)
    access_key = createAccessKey(
        documentInfo=invoice.documentInfo, randomNumber=random_number
    )

    # Generate XML from invoice data.
    xml_data = create_invoice_xml(info=invoice, access_key_invoice=access_key)
    xml_file_name = f"{access_key}.xml"
    xml_string = xml_data["xmlString"]

    # Create temporary files used during signing flow.
    xml_no_signed = create_temp_xml_file(xml_string, xml_file_name)
    xml_signed = create_temp_xml_file(xml_string, xml_file_name)

    certificate_name = "signature.p12"
    path_signature = os.path.abspath("app/signature.p12")
    async with aiofiles.open(path_signature, "rb") as file:
        digital_signature = await file.read()
        certificate_to_sign = create_temp_binary_file(
            digital_signature, certificate_name
        )

    password_p12 = config["PASSWORD"]
    info_to_sign_xml = InfoToSignXml(
        pathXmlToSign=xml_no_signed.name,
        pathXmlSigned=xml_signed.name,
        pathSignatureP12=certificate_to_sign.name,
        passwordSignature=password_p12,
    )

    is_xml_created = sign_invoice_xml(info_to_sign_xml)
    if not is_xml_created:
        return SignInvoiceOutputDto(
            is_success=False,
            access_key=access_key,
            error_code="signing_error",
        )

    url_reception = config["URL_RECEPTION"]
    url_authorization = config["URL_AUTHORIZATION"]

    is_received = await send_signed_xml_to_reception(
        path_xml_signed=xml_signed.name,
        url_to_reception=url_reception,
    )
    if not is_received:
        return SignInvoiceOutputDto(
            is_success=False,
            access_key=access_key,
            is_received=False,
            is_authorized=False,
            error_code="reception_error",
        )

    response_authorization = await send_access_key_to_authorization(
        access_key=access_key,
        url_to_authorization=url_authorization,
    )
    is_authorized = response_authorization["isValid"]
    xml_signed_value = response_authorization["xml"]
    if not is_authorized:
        return SignInvoiceOutputDto(
            is_success=False,
            access_key=access_key,
            is_received=True,
            is_authorized=False,
            error_code="authorization_error",
        )

    return SignInvoiceOutputDto(
        is_success=True,
        access_key=access_key,
        is_received=is_received,
        is_authorized=is_authorized,
        xml_signed_value=xml_signed_value,
    )
