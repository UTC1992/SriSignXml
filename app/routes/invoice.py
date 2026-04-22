import os
import random
import logging
import aiofiles
from typing import Optional

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.models.invoice import Invoice, InfoToSignXml
from app.models.invoice_sign_responses import (
    InvoiceSignResultBlock,
    build_invoice_sign_problem,
    invoice_sign_problem_response,
    invoice_sign_success_response,
)
from app.utils.create_access_key import createAccessKey
from app.utils.create_xml import createXml
from app.utils.sign_xml import sign_xml_file
from app.utils.send_xml import send_xml_to_reception, send_xml_to_authorization
from app.utils.control_temp_file import createTempXmlFile, createTempFile
from dotenv import dotenv_values

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
        # create access key
        random_number = str(random.randint(1, 99999999)).zfill(8)
        access_key = createAccessKey(
            documentInfo=invoice.documentInfo, randomNumber=random_number)

        # generate xml
        xml_data = createXml(info=invoice, accessKeyInvoice=access_key)

        # xml name
        xml_file_name = str(access_key) + '.xml'

        # xml string
        xml_string = xml_data['xmlString']

        # create temp files to create xml
        xml_no_signed = createTempXmlFile(xml_string, xml_file_name)
        xml_signed = createTempXmlFile(xml_string, xml_file_name)

        # get digital signature
        certificate_name = 'signature.p12'
        path_signature = os.path.abspath('app/signature.p12')
        async with aiofiles.open(path_signature, 'rb') as file:
            digital_signature = await file.read()
            certificate_to_sign = createTempFile(
                digital_signature, certificate_name)

        # password of signature
        password_p12 = config['PASSWORD']
        info_to_sign_xml = InfoToSignXml(
            pathXmlToSign=xml_no_signed.name,
            pathXmlSigned=xml_signed.name,
            pathSignatureP12=certificate_to_sign.name,
            passwordSignature=password_p12)

        # sign xml and creating temp file
        is_xml_created = sign_xml_file(info_to_sign_xml)

        if not is_xml_created:
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

        # url for reception and authorization
        url_reception = config["URL_RECEPTION"]
        url_authorization = config["URL_AUTHORIZATION"]

        # send xml for reception
        is_received = await send_xml_to_reception(
            pathXmlSigned=xml_signed.name,
            urlToReception=url_reception,
        )

        if not is_received:
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

        # send xml for authorization
        response_authorization = await send_xml_to_authorization(
            access_key,
            url_authorization,
        )
        is_authorized = response_authorization['isValid']
        xml_signed_value = response_authorization['xml']

        if not is_authorized:
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

        return invoice_sign_success_response(
            access_key=access_key,
            is_received=is_received,
            is_authorized=is_authorized,
            xml_file_signed=xml_signed_value,
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
