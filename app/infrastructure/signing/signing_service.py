from app.api.schemas.invoice import InfoToSignXml
from app.utils.sign_xml import sign_xml_file


def sign_invoice_xml(info_to_sign_xml: InfoToSignXml) -> bool:
    return sign_xml_file(info_to_sign_xml)
