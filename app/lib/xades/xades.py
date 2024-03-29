import os
import subprocess
import logging


class Xades(object):
    def sign(self, xml_no_signed_path, xml_signed_path, file_pk12_path, password):
        JAR_PATH = 'FirmaElectronica/FirmaElectronica.jar'
        JAVA_CMD = 'java'
        path_jar_to_sign = os.path.join(os.path.dirname(__file__), JAR_PATH)
        try:
            command = [
                JAVA_CMD,
                '-jar',
                path_jar_to_sign,
                xml_no_signed_path,
                file_pk12_path,
                password,
                xml_signed_path
            ]
            subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            returnCode = e.returncode
            output = e.output
            logging.error('Llamada a proceso JAVA codigo: %s' % returnCode)
            logging.error('Error: %s' % output)

        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        res = p.communicate()
        return res[0]
