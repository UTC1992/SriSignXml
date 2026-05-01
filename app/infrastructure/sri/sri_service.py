from app.utils.send_xml import send_xml_to_authorization, send_xml_to_reception


async def send_signed_xml_to_reception(path_xml_signed: str, url_to_reception: str) -> bool:
    return await send_xml_to_reception(pathXmlSigned=path_xml_signed, urlToReception=url_to_reception)


async def send_access_key_to_authorization(access_key: str, url_to_authorization: str) -> dict:
    return await send_xml_to_authorization(accessKey=access_key, urlToAuthorization=url_to_authorization)
