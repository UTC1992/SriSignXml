import base64
import logging
from zeep import AsyncClient


async def send_xml_to_reception(pathXmlSigned: str, urlToReception: str):
    # get xml from directory
    with open(pathXmlSigned, 'rb') as f:
        xml_signed = f.read()

    # encode xml to base64 and decode in utf-8
    base64_binary_xml = base64.b64encode(xml_signed).decode('utf-8')

    try:
        async with AsyncClient(urlToReception) as client:
            result = await client.service.validarComprobante(base64_binary_xml)

            if result['estado'] == 'RECIBIDA':
                logging.info("Response status: " + result.estado)
                return True
            else:
                logging.warning(result)
                return False

    except Exception as e:
        logging.error('Error to send xml for reception: %s' % str(e))
        return False


async def send_xml_to_authorization(accessKey: str, urlToAuthorization: str):
    try:
        async with AsyncClient(urlToAuthorization) as client:
            result = await client.service.autorizacionComprobante(accessKey)

            status = result.autorizaciones.autorizacion[0].estado

            if status == 'AUTORIZADO' or status == 'EN PROCESO':
                logging.info("Response authorization: ", status)

                xml = result.autorizaciones.autorizacion[0].comprobante
                return {
                    'isValid': True,
                    'status': status,
                    'xml': xml
                }
            else:
                logging.warning(result)
                return {
                    'isValid': False,
                    'status': status,
                    'xml': None
                }
    except Exception as e:
        logging.error('Error to send xml for reception: %s' % str(e))
        return {
            'isValid': False,
            'status': status,
            'xml': None,
            'error': str(e)
        }
