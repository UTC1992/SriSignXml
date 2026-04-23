from pydantic import BaseModel
from typing import List


class AdditionalInfo(BaseModel):
    name: str
    value: str


class TotalWithTax(BaseModel):
    taxCode: str
    percentageCode: str
    taxableBase: str
    taxValue: str


class Detail(BaseModel):
    productCode: str
    productName: str
    description: str
    quantity: int
    price: str
    discount: str
    subTotal: str
    taxTypeCode: str
    percentageCode: str
    rate: str
    taxableBaseTax: str
    taxValue: str


class Customer(BaseModel):
    identificationType: str
    customerName: str
    customerDni: str
    customerAddress: str


class DocumentInfo(BaseModel):
    accessKey: str
    businessName: str
    commercialName: str
    businessAddress: str
    dayEmission: str
    monthEmission: str
    yearEmission: str
    codDoc: str
    rucBusiness: str
    environment: str
    typeEmission: str
    establishment: str
    establishmentAddress: str
    emissionPoint: str
    sequential: str
    obligatedAccounting: str


class Payment(BaseModel):
    totalWithoutTaxes: str
    totalDiscount: str
    gratuity: str
    totalAmount: str
    currency: str
    paymentMethodCode: str
    totalPayment: str


class Invoice(BaseModel):
    documentInfo: DocumentInfo
    customer: Customer
    payment: Payment
    details: List[Detail]
    additionalInfo: List[AdditionalInfo]
    totalsWithTax: List[TotalWithTax]


class InfoToSignXml:
    def __init__(
            self,
            pathXmlToSign: str,
            pathXmlSigned: str,
            pathSignatureP12: str,
            passwordSignature: str
    ):
        self.pathXmlToSign = pathXmlToSign
        self.pathXmlSigned = pathXmlSigned
        self.passwordSignature = passwordSignature
        self.pathSignatureP12 = pathSignatureP12
