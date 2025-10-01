# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based microservice for generating, signing, and submitting electronic invoices (facturas electrónicas) to Ecuador's SRI (Servicio de Rentas Internas). The service takes invoice data as JSON, generates XML according to SRI specifications, signs it using XAdES digital signatures, and submits it through SRI's SOAP web services.

## Key Requirements

- **Python**: 3.11.3
- **Java**: JDK 1.8 (required for the XAdES signing library `FirmaElectronica.jar`)
- **Digital Signature**: A `.p12` certificate file must be placed in `app/signature.p12`
- **Environment Variables**: Configure `.env` file with `PASSWORD` (certificate password) and SRI web service URLs

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API (default port 8000)
uvicorn main:app --reload

# Access API documentation
http://localhost:8000/docs
```

### Docker Development
```bash
# Build Docker image
docker build -t sri-sign-xml-open-source .

# Run container (port 5003)
docker run -p 5003:5003 sri-sign-xml-open-source

# Run in detached mode with named container
docker run -d -p 5003:5003 --name sri-container sri-sign-xml-open-source

# View logs
docker logs -f sri-container

# Access API documentation
http://localhost:5003/docs
```

## Architecture

### Request Flow
1. **POST /invoice/sign** receives invoice data
2. **Access Key Generation** (`app/utils/create_access_key.py`): Creates 49-digit access key using invoice metadata + random number + module 11 check digit
3. **XML Generation** (`app/utils/create_xml.py`): Builds XML structure using `lxml.etree` according to SRI factura schema
4. **XML Signing** (`app/utils/sign_xml.py` → `app/lib/xades/xades.py`): Calls Java JAR (`FirmaElectronica/FirmaElectronica.jar`) via subprocess to apply XAdES-BES signature
5. **Reception** (`app/utils/send_xml.py:send_xml_to_reception`): Sends base64-encoded signed XML to SRI reception web service using SOAP (zeep library)
6. **Authorization** (`app/utils/send_xml.py:send_xml_to_authorization`): Polls SRI authorization service with access key, retrieves authorized XML

### Core Components

**Models** (`app/models/invoice.py`):
- Pydantic models for request validation: `Invoice`, `DocumentInfo`, `Customer`, `Payment`, `Detail`, `AdditionalInfo`, `TotalWithTax`
- `InfoToSignXml`: Plain class for passing signing parameters

**Routes** (`app/routes/invoice.py`):
- Single endpoint `/invoice/sign` orchestrates the entire workflow
- Uses temporary files for XML processing
- Returns: `accessKey`, `isReceived`, `isAuthorized`, `xmlFileSigned`

**Utils**:
- `create_access_key.py`: Implements SRI access key algorithm with module 11 check digit
- `create_xml.py`: Builds XML using `lxml.etree` (not xmltodict for generation)
- `sign_xml.py`: Wrapper for Java XAdES signing process
- `send_xml.py`: Async SOAP client operations using `zeep.AsyncClient`
- `control_temp_file.py`: Manages temporary files for XML processing
- `module11.py`: Check digit calculation

**XAdES Library** (`app/lib/xades/`):
- `xades.py`: Python wrapper that invokes `FirmaElectronica.jar` via subprocess
- Java JAR located at `app/lib/xades/FirmaElectronica/FirmaElectronica.jar`
- Requires Java 1.8 in PATH

### Environment Configuration

`.env` file (based on `.env.example`):
```
URL_RECEPTION=https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl
URL_AUTHORIZATION=https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl
PASSWORD=<your-certificate-password>
```

URLs shown are for SRI's test environment (`celcer`). Production uses different endpoints.

## Important Notes

- The Java subprocess call in `xades.py` is the critical signing step - ensure Java 1.8 is available
- Temporary files are created during processing and should be cleaned up properly
- SOAP operations are asynchronous (`send_xml_to_reception`, `send_xml_to_authorization`)
- The access key must be exactly 49 digits (48 digits + 1 check digit)
- Docker image uses Alpine Linux with OpenJDK 11 (works despite recommendation for JDK 1.8)