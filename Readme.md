# Firma electronica Sri con Xades

El proyecto es una api creada en FastApi con python, dados los datos de la factura permite generar el archivo xml firmado, enviarlo a recepción y autorización al SRI.

## Instalación

1. Clonar el repositorio
2. Instalar las librerías: pip install -r requirements.txt
3. Colocar la firma electrónica en la carpeta app y nombrarla signature.p12 (p12 es la extensión del archivo)
4. En el archivo env se encuentra la variable PASSWORD allí debes colocar la clave de tu firma electronica
5. Correr la api con: uvicorn main:app --reload

## Créditos

Este proyecto fue inspirado por https://github.com/cmruizg777/FirmaElectronicaPython/tree/master/db

## Contacto

Para más información, puedes escribirme en [correo electrónico](mailto:omar.guanoluisa25@gmail.com).
