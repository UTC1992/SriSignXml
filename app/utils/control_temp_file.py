import os
import tempfile


def createTempXmlFile(xml, fileName):
    # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=fileName) as temp_file:
        temp_file.write(xml.encode())

    return temp_file


def createTempFile(file, fileName):
    # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=fileName) as temp_file:
        temp_file.write(file)

    return temp_file


def removeTempFile(path: str):
    if os.path.exists(path):
        os.remove(path)
