from app.utils.module11 import CheckDigit
from app.models.invoice import DocumentInfo


def createAccessKey(documentInfo: DocumentInfo, randomNumber: int):
    # Info de la invoice
    dateEmission = ''.join(getDateComplete(
        documentInfo.dayEmission, documentInfo.monthEmission, documentInfo.yearEmission))
    codDoc = ''.join(documentInfo.codDoc)  # Doc type Invoice
    rucBusiness = ''.join(documentInfo.rucBusiness)
    environment = ''.join(documentInfo.environment)
    establishment = ''.join(documentInfo.establishment)
    emissionPoint = ''.join(documentInfo.emissionPoint)
    sequential = ''.join(documentInfo.sequential)
    randomNumber = ''.join(randomNumber)
    typeEmission = ''.join(documentInfo.typeEmission)

    # combination of data
    preAccessKey = dateEmission + codDoc + rucBusiness + environment + \
        establishment + emissionPoint + sequential + randomNumber + typeEmission
    # print(len(preAccessKey))
    checkDigit = CheckDigit()
    checkerDigit = str(checkDigit.compute_mod11(preAccessKey))
    # print(checkerDigit)
    # validate when the digit is 10
    if int(checkerDigit) == 10:
        checkerDigit = 1
    if int(checkerDigit) == 11:
        checkerDigit = 0

    # join preAccessKey with checkerDigit
    accessKey = preAccessKey + checkerDigit

    # return accessKey combination
    return accessKey


def getDateComplete(day: str, month: str, year: str):
    return day + month + year
