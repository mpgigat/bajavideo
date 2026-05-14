# Despliegue en Coolify

Guía paso a paso para desplegar el descargador de videos en Coolify usando Dockerfile.

## Requisitos Previos

- Un servidor VPS con Coolify instalado
- Dominio configurado (ej: videodl.tu-dominio.com)
- Acceso al repositorio Git (GitHub, GitLab, o Bitbucket)

## Pasos de Despliegue

### 1. Preparar el Repositorio

Asegúrate de que tu repositorio contenga:
- `app.py`
- `requirements.txt`
- `Dockerfile`
- `static/index.html`
- `.dockerignore`
- `.gitignore`

### 2. Configurar Coolify

1. **Inicia sesión en tu panel de Coolify**
   ```
   https://coolify.tu-dominio.com
   ```

2. **Crear un nuevo proyecto**
   - Ve a "Projects" → "New Project"
   - Nombra el proyecto: `Video Downloader`

3. **Crear un nuevo servicio**
   - En el proyecto, haz clic en "New Service"
   - Selecciona "Dockerfile"

4. **Configurar el servicio Dockerfile**
   
   **Repository:**
   - Selecciona tu proveedor de Git (GitHub, GitLab, etc.)
   - Selecciona el repositorio
   - Selecciona la rama (generalmente `main` o `master`)
   
   **Dockerfile Path:**
   - Path: `Dockerfile`
   
   **Build Context:**
   - Deja vacío o usa `/` (raíz del repositorio)
   
   **Port Mapping:**
   - Container Port: `5000`
   - Host Port: `30000` (o cualquier puerto disponible)
   
   **Environment Variables:**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=0
   PORT=5000
   ```

5. **Configurar el dominio**
   - Ve a "Domains"
   - Agrega tu subdominio: `videodl.tu-dominio.com`
   - Coolify generará automáticamente el certificado SSL
   - Coolify configurará automáticamente el proxy inverso (Traefik)

6. **Configurar recursos (opcional)**
   - CPU: 0.5 - 1 core
   - RAM: 512MB - 1GB
   - Disk: 5GB (suficiente para archivos temporales)

7. **Desplegar**
   - Haz clic en "Deploy"
   - Espera a que se complete la construcción y despliegue

### 3. Verificar el Despliegue

1. Abre tu navegador y ve a: `https://videodl.tu-dominio.com`
2. Prueba descargar un video de Instagram o YouTube
3. Verifica que el archivo se descargue a tu computadora

## Configuración Avanzada

### Habilitar Auto-Deploy

1. En la configuración del servicio
2. Activa "Auto Deploy on Push"
3. Cada vez que hagas push al repositorio, se desplegará automáticamente

### Configurar Límites de Tamaño

Para evitar que el servidor se llene con archivos temporales:

Edita `docker-compose.yml`:
```yaml
services:
  app:
    # ... configuración existente ...
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

### Configurar Health Check

En Coolify, configura el health check en la configuración del servicio:

**Health Check Settings:**
- **Test:** `CMD-SHELL curl -f http://localhost:5000/ || exit 1`
- **Interval:** 30s
- **Timeout:** 10s
- **Retries:** 3
- **Start Period:** 10s

O alternativamente, puedes agregar el health check al Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1
```

### Configurar Logs

Para ver los logs en tiempo real:
1. Ve al servicio en Coolify
2. Haz clic en "Logs"
3. Verás los logs de la aplicación

## Solución de Problemas

### Error: "Cannot connect to database"

Esta aplicación no usa base de datos, así que este error no debería ocurrir.

### Error: "FFmpeg not found"

El `Dockerfile` ya incluye FFmpeg. Si tienes problemas:
1. Verifica que el contenedor se esté ejecutando
2. Revisa los logs para ver errores de compilación

### Error: "Port already in use"

Asegúrate de que el puerto 5000 no esté en uso en tu servidor.

### Error: "SSL Certificate not working"

1. Verifica que tu dominio apunte a la IP del servidor
2. Espera unos minutos para que se propague el DNS
3. Verifica que el puerto 80 y 443 estén abiertos en el firewall

### Error: "Download failed"

1. Verifica que la URL sea correcta
2. Asegúrate de que el video sea público
3. Revisa los logs en Coolify para más detalles

## Monitoreo

Coolify proporciona:
- **Uso de CPU y RAM**: En el panel del servicio
- **Logs**: En la sección "Logs"
- **Health Checks**: Configurado en `docker-compose.yml`
- **Uptime**: Visible en el panel principal

## Actualización

Para actualizar la aplicación:
1. Haz cambios en tu código
2. Commit y push al repositorio
3. Coolify detectará los cambios automáticamente
4. O haz clic manualmente en "Redeploy"

## Seguridad

- La aplicación usa HTTPS automático
- Los archivos temporales se eliminan automáticamente
- No se guarda información personal
- Considera agregar rate limiting para prevenir abuso

## Costos Estimados

Para un VPS típico:
- **CPU**: 0.5 - 1 core
- **RAM**: 512MB - 1GB
- **Almacenamiento**: 5-10GB
- **Costo mensual**: $5 - $15 (dependiendo del proveedor)

## Soporte

Para más información sobre Coolify:
- Documentación: https://coolify.io/docs
- GitHub: https://github.com/coollabsio/coolify
- Discord: https://discord.gg/coolify