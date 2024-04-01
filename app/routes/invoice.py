import os
import random
import asyncio
from fastapi import APIRouter
from app.models.invoice import Invoice, InfoToSignXml
from app.utils.create_access_key import createAccessKey
from app.utils.create_xml import createXml
from app.utils.sign_xml import sign_xml_file
from app.utils.send_xml import send_xml_to_reception, send_xml_to_authorization
from app.utils.control_temp_file import createTempXmlFile, createTempFile
from app.utils.get_content_xml_file import get_content_xml_file
from dotenv import dotenv_values

routerInvoice = APIRouter()
config = {
    **dotenv_values('.env')
}


@routerInvoice.post("/invoice/sign", tags=['Invoice'])
async def sign_invoice(invoice: Invoice):
    try:
        # create access key
        randomNumber = str(random.randint(1, 99999999)).zfill(8)
        accessKey = createAccessKey(
            documentInfo=invoice.documentInfo, randomNumber=randomNumber)

        # generate xml
        xmlData = createXml(info=invoice, accessKeyInvoice=accessKey)

        # xml name
        xmlFileName = str(accessKey) + '.xml'

        # xml string
        xmlString = xmlData['xmlString']

        # create temp files to create xml
        xmlNoSigned = createTempXmlFile(xmlString, xmlFileName)
        xmlSigned = createTempXmlFile(xmlString, xmlFileName)

        # get digital signature
        certificateName = 'signature.p12'
        pathSignature = os.path.abspath('app/signature.p12')
        with open(pathSignature, 'rb') as file:
            digitalSignature = file.read()
            certificateToSign = createTempFile(
                digitalSignature, certificateName)

        # password of signature
        passwordP12 = config['PASSWORD']
        infoToSignXml = InfoToSignXml(
            pathXmlToSign=xmlNoSigned.name,
            pathXmlSigned=xmlSigned.name,
            pathSignatureP12=certificateToSign.name,
            passwordSignature=passwordP12)

        # sign xml and creating temp file
        isXmlCreated = sign_xml_file(infoToSignXml)

        # url for reception and authorization
        urlReception = config["URL_RECEPTION"]
        urlAuthorization = config["URL_AUTHORIZATION"]

        # send xml for reception
        isReceived = False
        if isXmlCreated:
            isReceived = await send_xml_to_reception(
                pathXmlSigned=xmlSigned.name,
                urlToReception=urlReception,
            )

        # send xml for authorization
        isAuthorized = False
        xmlSignedValue = None
        if isReceived:
            responseAuthorization = await send_xml_to_authorization(
                accessKey,
                urlAuthorization,
            )
            isAuthorized = responseAuthorization['isValid']
            # get xml signed content
            xmlSignedValue = responseAuthorization['xml']

        return {
            'result': {
                'accessKey': accessKey,
                'isReceived': isReceived,
                'isAuthorized': isAuthorized,
                'xmlFileSigned': xmlSignedValue
            }
        }
    except Exception as e:
        print(e)
        return {'result': None}
