import logging
from app.lib.xades.xades import Xades


def sign_xml_file(infoToSignXml: any):
    try:
        xades = Xades()
        xades.sign(
            infoToSignXml.pathXmlToSign,
            infoToSignXml.pathXmlSigned,
            infoToSignXml.pathSignatureP12,
            infoToSignXml.passwordSignature)
        return True
    except Exception as e:
        logging.error('Error to sign xml: %s' % str(e))
