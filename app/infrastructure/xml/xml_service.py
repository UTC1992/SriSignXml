from app.api.schemas.invoice import Invoice
from app.utils.create_xml import createXml


def create_invoice_xml(info: Invoice, access_key_invoice: str) -> dict:
    return createXml(info=info, accessKeyInvoice=access_key_invoice)
