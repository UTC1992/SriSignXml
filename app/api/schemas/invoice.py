from decimal import Decimal, InvalidOperation
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


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


class PaymentLine(BaseModel):
    paymentMethodCode: str
    total: str
    term: Optional[str] = None
    termUnit: Optional[str] = None

    @field_validator("paymentMethodCode")
    @classmethod
    def validate_payment_method_code(cls, value: str) -> str:
        code = value.strip()
        if not code:
            raise ValueError("paymentMethodCode is required")
        if not code.isdigit() or len(code) != 2:
            raise ValueError("paymentMethodCode must be a 2-digit numeric code (SRI table 24)")
        return code

    @field_validator("total")
    @classmethod
    def validate_total(cls, value: str) -> str:
        total = value.strip()
        if not total:
            raise ValueError("total is required")
        try:
            decimal_total = Decimal(total)
        except InvalidOperation as error:
            raise ValueError("total must be a valid numeric value") from error
        if decimal_total <= 0:
            raise ValueError("total must be greater than 0")
        return total

    @field_validator("term", "termUnit")
    @classmethod
    def normalize_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @model_validator(mode="after")
    def validate_term_fields(self):
        has_term = self.term is not None
        has_term_unit = self.termUnit is not None
        if has_term != has_term_unit:
            raise ValueError("term and termUnit must be provided together")
        if has_term:
            if not self.term.isdigit() or int(self.term) <= 0:
                raise ValueError("term must be a positive integer")
            if len(self.termUnit) > 10:
                raise ValueError("termUnit must have at most 10 characters")
        return self


class Payment(BaseModel):
    totalWithoutTaxes: str
    totalDiscount: str
    gratuity: str
    totalAmount: str
    currency: str
    payments: List[PaymentLine] = Field(min_length=1)

    @field_validator("payments")
    @classmethod
    def validate_payments_not_empty(cls, value: List[PaymentLine]) -> List[PaymentLine]:
        if not value:
            raise ValueError("payments must contain at least one payment line")
        return value

    @model_validator(mode="after")
    def validate_payment_totals(self):
        try:
            total_amount = Decimal(self.totalAmount.strip())
        except InvalidOperation as error:
            raise ValueError("totalAmount must be a valid numeric value") from error

        payments_total = sum(Decimal(payment.total) for payment in self.payments)
        if payments_total != total_amount:
            raise ValueError(
                f"Sum of payments ({payments_total}) must equal totalAmount ({total_amount})"
            )
        return self


class Invoice(BaseModel):
    documentInfo: DocumentInfo
    customer: Customer
    payment: Payment
    details: List[Detail]
    additionalInfo: List[AdditionalInfo]
    totalsWithTax: List[TotalWithTax]


class RetryInvoiceRequest(BaseModel):
    retryMode: Literal["full", "authorization_only"]
    invoice: Optional[Invoice] = None
    accessKey: Optional[str] = None


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
