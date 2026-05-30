# Frontend API Contract - Invoice Sign

## Endpoint

- **Method**: `POST`
- **Path**: `/invoice/sign`
- **Success content type**: `application/json`
- **Error content type**: `application/problem+json` (RFC 7807)

## Request Body

```json
{
  "documentInfo": {
    "accessKey": "string",
    "businessName": "string",
    "commercialName": "string",
    "businessAddress": "string",
    "dayEmission": "string",
    "monthEmission": "string",
    "yearEmission": "string",
    "codDoc": "string",
    "rucBusiness": "string",
    "environment": "string",
    "typeEmission": "string",
    "establishment": "string",
    "establishmentAddress": "string",
    "emissionPoint": "string",
    "sequential": "string",
    "obligatedAccounting": "string"
  },
  "customer": {
    "identificationType": "string",
    "customerName": "string",
    "customerDni": "string",
    "customerAddress": "string"
  },
  "payment": {
    "totalWithoutTaxes": "string",
    "totalDiscount": "string",
    "gratuity": "string",
    "totalAmount": "string",
    "currency": "string",
    "payments": [
      {
        "paymentMethodCode": "string",
        "total": "string",
        "term": "string (optional)",
        "termUnit": "string (optional)"
      }
    ]
  },
  "details": [
    {
      "productCode": "string",
      "productName": "string",
      "description": "string",
      "quantity": 1,
      "price": "string",
      "discount": "string",
      "subTotal": "string",
      "taxTypeCode": "string",
      "percentageCode": "string",
      "rate": "string",
      "taxableBaseTax": "string",
      "taxValue": "string"
    }
  ],
  "additionalInfo": [
    {
      "name": "string",
      "value": "string"
    }
  ],
  "totalsWithTax": [
    {
      "taxCode": "string",
      "percentageCode": "string",
      "taxableBase": "string",
      "taxValue": "string"
    }
  ]
}
```

### Payment Rules (SRI-aligned)

- `payment.payments` is required and must contain at least one item.
- `payments[].paymentMethodCode` must be a 2-digit numeric code from SRI table 24.
- `payments[].total` must be numeric and greater than `0`.
- Sum of `payments[].total` must be equal to `payment.totalAmount`.
- `payments[].term` and `payments[].termUnit` are optional, but if one is sent, both are required.

## Success Response

### `200 OK`

```json
{
  "success": true,
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": true,
    "isAuthorized": true,
    "xmlFileSigned": "<factura>...</factura>"
  }
}
```

---

## Retry Endpoint

- **Method**: `POST`
- **Path**: `/invoice/retry`
- **Success content type**: `application/json`
- **Error content type**: `application/problem+json` (RFC 7807)

### Request Body - Full Retry

Use this mode when reception failed and you need to retry the complete flow:
signing -> reception -> authorization.

```json
{
  "retryMode": "full",
  "invoice": {
    "documentInfo": {
      "accessKey": "string",
      "businessName": "string",
      "commercialName": "string",
      "businessAddress": "string",
      "dayEmission": "string",
      "monthEmission": "string",
      "yearEmission": "string",
      "codDoc": "string",
      "rucBusiness": "string",
      "environment": "string",
      "typeEmission": "string",
      "establishment": "string",
      "establishmentAddress": "string",
      "emissionPoint": "string",
      "sequential": "string",
      "obligatedAccounting": "string"
    },
    "customer": {
      "identificationType": "string",
      "customerName": "string",
      "customerDni": "string",
      "customerAddress": "string"
    },
    "payment": {
      "totalWithoutTaxes": "string",
      "totalDiscount": "string",
      "gratuity": "string",
      "totalAmount": "string",
      "currency": "string",
      "payments": [
        {
          "paymentMethodCode": "string",
          "total": "string",
          "term": "string (optional)",
          "termUnit": "string (optional)"
        }
      ]
    },
    "details": [
      {
        "productCode": "string",
        "productName": "string",
        "description": "string",
        "quantity": 1,
        "price": "string",
        "discount": "string",
        "subTotal": "string",
        "taxTypeCode": "string",
        "percentageCode": "string",
        "rate": "string",
        "taxableBaseTax": "string",
        "taxValue": "string"
      }
    ],
    "additionalInfo": [
      {
        "name": "string",
        "value": "string"
      }
    ],
    "totalsWithTax": [
      {
        "taxCode": "string",
        "percentageCode": "string",
        "taxableBase": "string",
        "taxValue": "string"
      }
    ]
  }
}
```

### Request Body - Authorization Only Retry

Use this mode when reception was already successful and only authorization must be retried.

```json
{
  "retryMode": "authorization_only",
  "accessKey": "010420260112345678900011001001000000001123456781"
}
```

### Success Response

`POST /invoice/retry` returns the same success payload as `/invoice/sign`:

```json
{
  "success": true,
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": true,
    "isAuthorized": true,
    "xmlFileSigned": "<factura>...</factura>"
  }
}
```

## Error Responses (RFC 7807)

> Note: `result` values depend on the step where the flow failed. Early failures can return `null`.

### 1) `signing_error` - HTTP `500`

```json
{
  "type": "urn:srisignxml:problem:signing_error",
  "title": "Error al firmar el XML",
  "status": 500,
  "detail": "Error al firmar el XML. Verifique el certificado, contraseña y formato del XML.",
  "instance": "http://localhost:8000/invoice/sign",
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": null,
    "isAuthorized": null,
    "xmlFileSigned": null
  },
  "errorCode": "signing_error"
}
```

### 2) `reception_error` - HTTP `502`

```json
{
  "type": "urn:srisignxml:problem:reception_error",
  "title": "El SRI no recibió el comprobante",
  "status": 502,
  "detail": "El XML fue firmado pero no fue recibido por el SRI. Verifique la conexión y el formato del XML.",
  "instance": "http://localhost:8000/invoice/sign",
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": false,
    "isAuthorized": false,
    "xmlFileSigned": null
  },
  "errorCode": "reception_error"
}
```

### 3) `authorization_error` - HTTP `422`

```json
{
  "type": "urn:srisignxml:problem:authorization_error",
  "title": "El SRI no autorizó el comprobante",
  "status": 422,
  "detail": "El XML fue recibido pero no fue autorizado por el SRI.",
  "instance": "http://localhost:8000/invoice/sign",
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": true,
    "isAuthorized": false,
    "xmlFileSigned": null
  },
  "errorCode": "authorization_error"
}
```

### 4) `file_not_found` - HTTP `404`

```json
{
  "type": "urn:srisignxml:problem:file_not_found",
  "title": "Recurso no encontrado",
  "status": 404,
  "detail": "Archivo no encontrado: [Errno 2] No such file or directory: '...'. Verifique que el certificado .p12 y el JAR de firma estén en su lugar.",
  "instance": "http://localhost:8000/invoice/sign",
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": null,
    "isAuthorized": null,
    "xmlFileSigned": null
  },
  "errorCode": "file_not_found"
}
```

### 5) `internal_error` - HTTP `500`

```json
{
  "type": "urn:srisignxml:problem:internal_error",
  "title": "Error interno del servidor",
  "status": 500,
  "detail": "Error interno del servidor. Contacte al administrador.",
  "instance": "http://localhost:8000/invoice/sign",
  "result": {
    "accessKey": "010420260112345678900011001001000000001123456781",
    "isReceived": null,
    "isAuthorized": null,
    "xmlFileSigned": null
  },
  "errorCode": "internal_error",
  "internalDetail": "string (solo debug, no para UI)"
}
```

### 6) `invalid_retry_payload` - HTTP `400`

```json
{
  "type": "urn:srisignxml:problem:invalid_retry_payload",
  "title": "Parámetros inválidos para reintento",
  "status": 400,
  "detail": "Para retryMode=full debe enviar invoice; para retryMode=authorization_only debe enviar accessKey.",
  "instance": "http://localhost:8000/invoice/retry",
  "result": {
    "accessKey": null,
    "isReceived": null,
    "isAuthorized": null,
    "xmlFileSigned": null
  },
  "errorCode": "invalid_retry_payload"
}
```

### 7) `invalid_retry_mode` - HTTP `400`

```json
{
  "type": "urn:srisignxml:problem:invalid_retry_mode",
  "title": "Modo de reintento inválido",
  "status": 400,
  "detail": "retryMode debe ser full o authorization_only.",
  "instance": "http://localhost:8000/invoice/retry",
  "result": {
    "accessKey": null,
    "isReceived": null,
    "isAuthorized": null,
    "xmlFileSigned": null
  },
  "errorCode": "invalid_retry_mode"
}
```

