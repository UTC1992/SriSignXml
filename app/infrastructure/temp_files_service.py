from app.utils.control_temp_file import createTempFile, createTempXmlFile


def create_temp_xml_file(xml: str, file_name: str):
    return createTempXmlFile(xml, file_name)


def create_temp_binary_file(binary_data: bytes, file_name: str):
    return createTempFile(binary_data, file_name)
