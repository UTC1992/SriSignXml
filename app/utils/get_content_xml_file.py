def get_content_xml_file(pathFile: str):
    with open(pathFile, 'r') as temp_file:
        return temp_file.read()
