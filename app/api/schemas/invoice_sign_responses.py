"""Respuestas JSON del endpoint de firma (camelCase) y Problem Details RFC 7807."""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from starlette.responses import JSONResponse

PROBLEM_JSON = "application/problem+json"


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class InvoiceSignResultBlock(CamelModel):
    access_key: Optional[str] = None
    is_received: Optional[bool] = None
    is_authorized: Optional[bool] = None
    xml_file_signed: Optional[str] = None


class InvoiceSignSuccessResponse(CamelModel):
    success: bool
    result: InvoiceSignResultBlock


class InvoiceSignProblemDetail(BaseModel):
    """RFC 7807: los miembros registrados van en minúsculas; el resto en camelCase."""

    model_config = ConfigDict(populate_by_name=True)

    problem_type: str = Field(serialization_alias="type")
    title: str
    status: int
    detail: str
    instance: Optional[str] = None
    result: InvoiceSignResultBlock
    error_code: str = Field(serialization_alias="errorCode")
    internal_detail: Optional[str] = Field(default=None, serialization_alias="internalDetail")


def invoice_sign_success_response(
    *,
    access_key: str,
    is_received: bool,
    is_authorized: bool,
    xml_file_signed: Optional[str],
) -> JSONResponse:
    body = InvoiceSignSuccessResponse(
        success=True,
        result=InvoiceSignResultBlock(
            access_key=access_key,
            is_received=is_received,
            is_authorized=is_authorized,
            xml_file_signed=xml_file_signed,
        ),
    )
    return JSONResponse(
        status_code=200,
        media_type="application/json",
        content=body.model_dump(mode="json", by_alias=True),
    )


def invoice_sign_problem_response(problem: InvoiceSignProblemDetail) -> JSONResponse:
    content = problem.model_dump(mode="json", by_alias=True)
    if content.get("internalDetail") is None:
        content.pop("internalDetail", None)
    return JSONResponse(
        status_code=problem.status,
        media_type=PROBLEM_JSON,
        content=content,
    )


def build_invoice_sign_problem(
    *,
    status_code: int,
    error_code: str,
    title: str,
    detail: str,
    instance: Optional[str],
    result: InvoiceSignResultBlock,
    internal_detail: Optional[str] = None,
) -> InvoiceSignProblemDetail:
    return InvoiceSignProblemDetail(
        problem_type=f"urn:srisignxml:problem:{error_code}",
        title=title,
        status=status_code,
        detail=detail,
        instance=instance,
        result=result,
        error_code=error_code,
        internal_detail=internal_detail,
    )
