# Descargador de Videos (Instagram/YouTube)

Aplicación web para descargar videos de Instagram y YouTube directamente al navegador del usuario. Los archivos no se guardan permanentemente en el servidor.

## Características

- ✅ Descarga videos de Instagram y YouTube
- ✅ Los archivos se envían directamente al navegador del usuario
- ✅ Los archivos temporales se eliminan automáticamente después de la descarga
- ✅ No se guarda nada permanentemente en el servidor
- ✅ Interfaz web simple y moderna

## Requisitos

- Python 3.11+
- FFmpeg (para procesamiento de video)

## Instalación Local

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd descargar-instagram
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Instalar FFmpeg:
   - **Windows**: Descargar de [ffmpeg.org](https://ffmpeg.org/download.html) y agregar al PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

5. Ejecutar:
```bash
python app.py
```

6. Abrir en el navegador: `http://localhost:5000`

## Despliegue con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
docker-compose up -d
```

### Opción 2: Docker manual

```bash
# Construir imagen
docker build -t instagram-downloader .

# Ejecutar contenedor
docker run -d -p 5000:5000 --name downloader instagram-downloader
```

## Despliegue en la Nube

### Render.com

1. Crear cuenta en [render.com](https://render.com)
2. Crear nuevo "Web Service"
3. Conectar repositorio Git
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment Variables: `PYTHON_VERSION=3.11.0`

### Railway.app

1. Instalar Railway CLI: `npm install -g @railway/cli`
2. Iniciar sesión: `railway login`
3. Inicializar proyecto: `railway init`
4. Desplegar: `railway up`

### Vercel

1. Instalar Vercel CLI: `npm install -g vercel`
2. Desplegar: `vercel`

## Variables de Entorno (Opcionales)

- `FLASK_ENV`: `production` o `development`
- `FLASK_DEBUG`: `0` o `1`
- `PORT`: Puerto de la aplicación (default: 5000)

## Estructura del Proyecto

```
.
├── app.py              # Aplicación Flask principal
├── static/
│   └── index.html      # Interfaz de usuario
├── requirements.txt    # Dependencias de Python
├── Dockerfile          # Configuración de Docker
├── docker-compose.yml  # Composición de servicios Docker
└── README.md          # Este archivo
```

## Notas Importantes

- Los archivos se descargan temporalmente en `/tmp/instagram_downloader` y se eliminan automáticamente
- El servidor solo actúa como intermediario, no almacena videos
- Para videos de cuentas privadas, necesitarás configurar cookies en `app.py`

## Solución de Problemas

### Error: "No supported JavaScript runtime"
Instalar Node.js o usar la opción `--js-runtimes` en yt-dlp.

### Error: "FFmpeg not found"
Asegúrate de que FFmpeg esté instalado y en el PATH del sistema.

### Error: "Download failed"
Verifica que la URL sea correcta y que el video sea público.

## Licencia

Este proyecto es solo para uso educativo y personal. Respeta los términos de servicio de Instagram y YouTube.
