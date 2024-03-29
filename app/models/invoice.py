from pydantic import BaseModel
from typing import List


class AdditionalInfo(BaseModel):
    name: str
    value: str

    # def __init__(self, name: str, value: str):
    #     self.name = name
    #     self.value = value


class TotalWithTax(BaseModel):
    taxCode: str
    percentageCode: str
    taxableBase: str
    taxValue: str

    # def __init__(self,
    #              taxCode: str,
    #              percentageCode: str,
    #              taxableBase: str,
    #              taxValue: str,
    #              ):
    #     self.taxCode = taxCode
    #     self.percentageCode = percentageCode
    #     self.taxableBase = taxableBase
    #     self.taxValue = taxValue


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

    # def __init__(self,
    #              productCode: str,
    #              productId: str,
    #              productName: str,
    #              description: str,
    #              quantity: int,
    #              price: str,
    #              discount: str,
    #              subTotal: str,
    #              taxTypeCode: str,
    #              percentageCode: str,
    #              rate: str,
    #              taxableBaseTax: str,
    #              taxValue: str,
    #              product: int):
    #     self.productCode = productCode
    #     self.productId = productId
    #     self.productName = productName
    #     self.description = description
    #     self.quantity = quantity
    #     self.price = price
    #     self.discount = discount
    #     self.subTotal = subTotal
    #     self.taxTypeCode = taxTypeCode
    #     self.percentageCode = percentageCode
    #     self.rate = rate
    #     self.taxableBaseTax = taxableBaseTax
    #     self.taxValue = taxValue
    #     self.product = product


class Customer(BaseModel):
    identificationType: str
    customerName: str
    customerDni: str
    customerAddress: str

    # def __init__(self,
    #              identificationType: str,
    #              customerName: str,
    #              customerDni: str,
    #              customerAddress: str,
    #              ):
    #     self.identificationType = identificationType
    #     self.customerName = customerName
    #     self.customerDni = customerDni
    #     self.customerAddress = customerAddress


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

    # def __init__(
    #         self,
    #         accessKey: str,
    #         businessName: str,
    #         commercialName: str,
    #         businessAddress: str,
    #         dayEmission: str,
    #         monthEmission: str,
    #         yearEmission: str,
    #         codDoc: str,
    #         rucBusiness: str,
    #         environment: str,
    #         typeEmission: str,
    #         establishment: str,
    #         establishmentAddress: str,
    #         emissionPoint: str,
    #         sequential: str,
    #         obligatedAccounting: str,
    # ):
    #     self.accessKey = accessKey
    #     self.businessName = businessName
    #     self.commercialName = commercialName
    #     self.businessAddress = businessAddress
    #     self.dayEmission = dayEmission
    #     self.monthEmission = monthEmission
    #     self.yearEmission = yearEmission
    #     self.codDoc = codDoc
    #     self.rucBusiness = rucBusiness
    #     self.environment = environment
    #     self.establishment = establishment
    #     self.establishmentAddress = establishmentAddress
    #     self.emissionPoint = emissionPoint
    #     self.sequential = sequential
    #     self.typeEmission = typeEmission
    #     self.obligatedAccounting = obligatedAccounting


class Payment(BaseModel):
    totalWithoutTaxes: str
    totalDiscount: str
    gratuity: str
    totalAmount: str
    currency: str
    paymentMethodCode: str
    totalPayment: str

    # def __init__(self,
    #              totalWithoutTaxes: str,
    #              totalDiscount: str,
    #              gratuity: str,
    #              totalAmount: str,
    #              currency: str,
    #              paymentMethodCode: str,
    #              totalPayment: str,
    #              ):
    #     self.totalWithoutTaxes = totalWithoutTaxes
    #     self.totalDiscount = totalDiscount
    #     self.gratuity = gratuity
    #     self.totalAmount = totalAmount
    #     self.currency = currency
    #     self.paymentMethodCode = paymentMethodCode
    #     self.totalPayment = totalPayment


class Invoice(BaseModel):
    documentInfo: DocumentInfo
    customer: Customer
    payment: Payment
    details: List[Detail]
    additionalInfo: List[AdditionalInfo]
    totalsWithTax: List[TotalWithTax]

    # def __init__(self,
    #              documentInfo: DocumentInfo,
    #              customer: Customer,
    #              details: List[Detail],
    #              additionalInfo: List[AdditionalInfo],
    #              totalsWithTax: List[TotalWithTax]):
    #     self.documentInfo = documentInfo,
    #     self.customer = customer
    #     self.details = details
    #     self.additionalInfo = additionalInfo
    #     self.totalsWithTax = totalsWithTax


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
