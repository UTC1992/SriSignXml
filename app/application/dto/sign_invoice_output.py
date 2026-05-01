from dataclasses import dataclass
from typing import Optional


@dataclass
class SignInvoiceOutputDto:
    is_success: bool
    access_key: Optional[str] = None
    is_received: Optional[bool] = None
    is_authorized: Optional[bool] = None
    xml_signed_value: Optional[str] = None
    error_code: Optional[str] = None
