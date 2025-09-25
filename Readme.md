# Firma electronica Sri con Xades Ecuador

El proyecto es una api creada en FastApi con python, dados los datos de la factura permite generar el archivo xml firmado, enviarlo a recepción y autorización al SRI, en la response obtendrás la clave de acceso del xml, el archivo firmado, y atributos que te dirán si el archivo fue recibido y autorizado. Nota: Es una base que te podría servir para tu proyecto ya que la idea es usarlo como micro-servicio.

Si te sirve regalame una estrella. ⭐️⭐️⭐️⭐️

## Xades
La librería Xades se usa para firmar el xml generado y esta echa en Java, funciona bien con -> jdk version "1.8.0_402". Recomiendo que lo usen y sí lo hacen en docker lo configuren de esa forma.

## Python
La versión de Python con la que se creo es: Python 3.11.3

## Instalación Local

1. Clonar el repositorio
2. Instalar las librerías: pip install -r requirements.txt
3. Colocar la firma electrónica en la carpeta app y nombrarla signature.p12 (p12 es la extensión del archivo)
4. En el archivo env se encuentra la variable PASSWORD allí debes colocar la clave de tu firma electronica
5. Correr la api con: uvicorn main:app --reload

## Ejecución con Docker (Sin Instalación Local)

Este proyecto incluye un Dockerfile que permite ejecutarlo en un contenedor Docker sin necesidad de instalar Python, Java u otras dependencias en tu sistema local (Windows, Mac o Linux). El contenedor incluye automáticamente Java 11 para la librería Xades.

### Requisitos
- Docker instalado en tu sistema.

### Pasos
1. Clonar el repositorio.
2. Colocar la firma electrónica en la carpeta `app` y nombrarla `signature.p12`.
3. Configurar el archivo `.env` con la clave de tu firma electrónica en la variable `PASSWORD`.
4. Construir la imagen Docker:
   ```
   docker build -t sri-sign-xml-open-source .
   ```
5. Ejecutar el contenedor:
   ```
   docker run -p 5003:5003 sri-sign-xml-open-source
   ```
6. Acceder a la API en `http://localhost:5003`.
7. Para interactuar con la API, abre Swagger UI en tu navegador: `http://localhost:5003/docs`.

### Ver Logs
- Para ver logs en tiempo real: `docker logs -f <nombre_del_contenedor>` (reemplaza con el nombre asignado).
- Si ejecutas en modo detached: `docker run -d -p 5003:5003 --name sri-container sri-sign-xml-open-source`

### Cambios Recientes
- Puerto actualizado a 5003 para evitar conflictos.
- Agregado `httpx` a `requirements.txt` para compatibilidad con operaciones asíncronas de zeep.

## Créditos

Este proyecto fue inspirado por https://github.com/cmruizg777/FirmaElectronicaPython/tree/master/db

## Contacto

Para más información, recomendaciones o dudas puedes escribirme a [correo electrónico](mailto:omar.guanoluisa25@gmail.com).
