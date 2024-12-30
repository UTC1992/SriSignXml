# Firma electronica Sri con Xades Ecuador

El proyecto es una api creada en FastApi con python, dados los datos de la factura permite generar el archivo xml firmado, enviarlo a recepción y autorización al SRI, en la response obtendrás la clave de acceso del xml, el archivo firmado, y atributos que te dirán si el archivo fue recibido y autorizado. Nota: Es una base que te podría servir para tu proyecto ya que la idea es usarlo como micro-servicio.

Si te sirve regalame una estrella. ⭐️⭐️⭐️⭐️

## Xades
La librería Xades se usa para firmar el xml generado y esta echa en Java, funciona bien con -> jdk version "1.8.0_402". Recomiendo que lo usen y sí lo hacen en docker lo configuren de esa forma.

## Python
La versión de Python con la que se creo es: Python 3.11.3

## Instalación

1. Clonar el repositorio
2. Instalar las librerías: pip install -r requirements.txt
3. Colocar la firma electrónica en la carpeta app y nombrarla signature.p12 (p12 es la extensión del archivo)
4. En el archivo env se encuentra la variable PASSWORD allí debes colocar la clave de tu firma electronica
5. Correr la api con: uvicorn main:app --reload

## Créditos

Este proyecto fue inspirado por https://github.com/cmruizg777/FirmaElectronicaPython/tree/master/db

## Contacto

Para más información, recomendaciones o dudas puedes escribirme a [correo electrónico](mailto:omar.guanoluisa25@gmail.com).
