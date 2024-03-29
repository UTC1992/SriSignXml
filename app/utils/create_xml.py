import json
import xmltodict
from lxml import etree
from app.models.invoice import Invoice


def jsonToXml(json_str):
    # Convert JSON to Python dictionary
    data = json.loads(json_str)

    # Convert dictionary to XML string
    xml_str = xmltodict.unparse(data)

    return xml_str


def createXml(info: Invoice, accessKeyInvoice: str):
    emissionDateInvoice = str(
        info.documentInfo.dayEmission
    ) + '/' + str(
        info.documentInfo.monthEmission
    ) + '/' + str(
        info.documentInfo.yearEmission)

    try:
        root = etree.Element('factura', attrib={
                             'id': 'comprobante', 'version': '1.0.0'})
        infoTributaria = etree.SubElement(root, 'infoTributaria')
        environment = etree.SubElement(infoTributaria, 'ambiente')
        environment.text = ''.join(info.documentInfo.environment)
        typeEmission = etree.SubElement(infoTributaria, 'tipoEmision')
        typeEmission.text = ''.join(info.documentInfo.typeEmission)
        businessName = etree.SubElement(infoTributaria, 'razonSocial')
        businessName.text = ''.join(info.documentInfo.businessName)
        commercialName = etree.SubElement(infoTributaria, 'nombreComercial')
        commercialName.text = ''.join(info.documentInfo.commercialName)
        ruc = etree.SubElement(infoTributaria, 'ruc')
        ruc.text = ''.join(info.documentInfo.rucBusiness)
        accessKey = etree.SubElement(infoTributaria, 'claveAcceso')
        accessKey.text = ''.join(accessKeyInvoice)
        codDoc = etree.SubElement(infoTributaria, 'codDoc')
        codDoc.text = ''.join(info.documentInfo.codDoc)
        establishment = etree.SubElement(infoTributaria, 'estab')
        establishment.text = ''.join(info.documentInfo.establishment)
        emissionPoint = etree.SubElement(infoTributaria, 'ptoEmi')
        emissionPoint.text = ''.join(info.documentInfo.emissionPoint)
        sequential = etree.SubElement(infoTributaria, 'secuencial')
        sequential.text = ''.join(info.documentInfo.sequential)
        address = etree.SubElement(infoTributaria, 'dirMatriz')
        address.text = ''.join(info.documentInfo.businessAddress)
        # end info tributaria

        infoInvoice = etree.SubElement(root, 'infoFactura')
        emissionDate = etree.SubElement(infoInvoice, 'fechaEmision')
        emissionDate.text = ''.join(emissionDateInvoice)
        dirEstablecimiento = etree.SubElement(
            infoInvoice, 'dirEstablecimiento')
        dirEstablecimiento.text = info.documentInfo.establishmentAddress
        obligatedAccounting = etree.SubElement(
            infoInvoice, 'obligadoContabilidad')
        obligatedAccounting.text = info.documentInfo.obligatedAccounting
        identificationType = etree.SubElement(
            infoInvoice, 'tipoIdentificacionComprador')
        identificationType.text = info.customer.identificationType
        razonSocialComprador = etree.SubElement(
            infoInvoice, 'razonSocialComprador')
        razonSocialComprador.text = info.customer.customerName
        customerDni = etree.SubElement(
            infoInvoice, 'identificacionComprador')
        customerDni.text = info.customer.customerDni
        if info.customer.customerAddress != '':
            customerAddress = etree.SubElement(
                infoInvoice, 'direccionComprador')
            customerAddress.text = info.customer.customerAddress
        totalSinImpuestos = etree.SubElement(infoInvoice, 'totalSinImpuestos')
        totalSinImpuestos.text = info.payment.totalWithoutTaxes
        totalDescuento = etree.SubElement(infoInvoice, 'totalDescuento')
        totalDescuento.text = info.payment.totalDiscount

        totalConImpuestos = etree.SubElement(infoInvoice, 'totalConImpuestos')
        for tax in info.totalsWithTax:
            totalTax = etree.SubElement(totalConImpuestos, 'totalImpuesto')
            totalTaxCode = etree.SubElement(totalTax, 'codigo')
            totalTaxCode.text = tax.taxCode
            percentageCode = etree.SubElement(totalTax, 'codigoPorcentaje')
            percentageCode.text = tax.percentageCode
            taxableBase = etree.SubElement(totalTax, 'baseImponible')
            taxableBase.text = str(tax.taxableBase)
            value = etree.SubElement(totalTax, 'valor')
            value.text = str(tax.taxValue)

        propina = etree.SubElement(infoInvoice, 'propina')
        propina.text = str(info.payment.gratuity)
        importeTotal = etree.SubElement(infoInvoice, 'importeTotal')
        importeTotal.text = info.payment.totalAmount
        moneda = etree.SubElement(infoInvoice, 'moneda')
        moneda.text = info.payment.currency
        pagos = etree.SubElement(infoInvoice, 'pagos')
        pago = etree.SubElement(pagos, 'pago')
        formaPago = etree.SubElement(pago, 'formaPago')
        formaPago.text = info.payment.paymentMethodCode
        total = etree.SubElement(pago, 'total')
        total.text = info.payment.totalPayment

        detalles = etree.SubElement(root, 'detalles')
        # end infoFactura
        for item in info.details:
            detalle = etree.SubElement(detalles, 'detalle')
            codigoPrincipal = etree.SubElement(detalle, 'codigoPrincipal')
            codigoPrincipal.text = item.productCode
            description = etree.SubElement(detalle, 'descripcion')
            description.text = item.description
            cantidad = etree.SubElement(detalle, 'cantidad')
            cantidad.text = str(item.quantity)
            precioUnitario = etree.SubElement(detalle, 'precioUnitario')
            precioUnitario.text = str(item.price)
            descuento = etree.SubElement(detalle, 'descuento')
            descuento.text = str(item.discount)
            precioTotalSinImpuesto = etree.SubElement(
                detalle, 'precioTotalSinImpuesto')
            precioTotalSinImpuesto.text = str(item.subTotal)
            impuestos = etree.SubElement(detalle, 'impuestos')
            impuesto = etree.SubElement(impuestos, 'impuesto')
            codigo = etree.SubElement(impuesto, 'codigo')
            codigo.text = str(item.taxTypeCode)
            codigoPorcentaje = etree.SubElement(impuesto, 'codigoPorcentaje')
            codigoPorcentaje.text = item.percentageCode
            tarifa = etree.SubElement(impuesto, 'tarifa')
            tarifa.text = str(item.rate)
            baseImponible = etree.SubElement(impuesto, 'baseImponible')
            baseImponible.text = str(item.taxableBaseTax)
            valor = etree.SubElement(impuesto, 'valor')
            valor.text = str(item.taxValue)

        infoAdicional = etree.SubElement(root, 'infoAdicional')
        for item in info.additionalInfo:
            campoAdicional = etree.SubElement(
                infoAdicional, 'campoAdicional', attrib={'nombre': item.name})
            campoAdicional.text = item.value

        xml_string = etree.tostring(root, pretty_print=True).decode('utf-8')

        return {
            'xmlFile': root,
            'xmlString': xml_string
        }
    except Exception as e:
        print('Error: ' + str(e))
        return {
            'xmlFile': None,
            'xmlString': None
        }


def saveXml(xml, pathToSave):
    tree = etree.ElementTree(xml)
    contenido_xml = etree.tostring(
        tree, pretty_print=True, encoding="utf-8").decode()
    with open(pathToSave, "w") as archivo:
        archivo.write(contenido_xml)
