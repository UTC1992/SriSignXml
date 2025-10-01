import os
import subprocess
import logging


class Xades(object):
    def sign(self, xml_no_signed_path, xml_signed_path, file_pk12_path, password):
        JAR_PATH = 'FirmaElectronica/FirmaElectronica.jar'
        JAVA_CMD = 'java'
        path_jar_to_sign = os.path.join(os.path.dirname(__file__), JAR_PATH)

        command = [
            JAVA_CMD,
            '-Dfile.encoding=UTF-8',  # Forzar UTF-8 en la JVM para leer/escribir archivos correctamente
            '-jar',
            path_jar_to_sign,
            xml_no_signed_path,
            file_pk12_path,
            password,
            xml_signed_path
        ]

        try:
            # Ejecutar el comando con encoding UTF-8 explícito
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                encoding='utf-8',
                errors='replace'
            )
            logging.info('XML firmado exitosamente')
            return result.stdout.encode('utf-8')
        except subprocess.CalledProcessError as e:
            logging.error('Error al firmar XML - Código: %s' % e.returncode)
            logging.error('Stdout: %s' % e.stdout)
            logging.error('Stderr: %s' % e.stderr)
            raise RuntimeError(f'Error al firmar XML: {e.stderr}')
