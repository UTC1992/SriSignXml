import os
import tempfile


def createTempXmlFile(xml, fileName):
    # Crea un archivo temporal con encoding UTF-8 explícito
    with tempfile.NamedTemporaryFile(delete=False, suffix=fileName, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(xml)

    return temp_file


def createTempFile(file, fileName):
    # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=fileName) as temp_file:
        temp_file.write(file)

    return temp_file


def removeTempFile(path: str):
    if os.path.exists(path):
        os.remove(path)
