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
    except RuntimeError as e:
        # Error esperado: Java falló al firmar (certificado inválido, XML corrupto, contraseña incorrecta, etc.)
        logging.error('Error al firmar XML: %s' % str(e))
        return False
    except FileNotFoundError as e:
        # Error: JAR de Java no encontrado o certificado .p12 no existe
        logging.error('Archivo no encontrado: %s' % str(e))
        return False
    except Exception as e:
        # Error inesperado: bug en el código
        logging.critical('Error inesperado al firmar XML: %s' % str(e))
        return False
