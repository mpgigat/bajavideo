# Solución al Error de YouTube "Sign in to confirm you're not a bot"

YouTube ha aumentado sus medidas de seguridad y ahora detecta tráfico automatizado. Aquí tienes varias soluciones:

## Solución 1: Configuración Actual (Recomendada Primero)

Ya he actualizado la aplicación con las siguientes mejoras:

### Cambios en [`app.py`](app.py:46):
- User-Agent de Chrome para simular tráfico real
- Cliente de YouTube Android (menos restricciones)
- Más reintentos para fragmentos
- Timeout extendido

### Cambios en [`Dockerfile`](Dockerfile:1):
- Node.js instalado para runtime de JavaScript
- Curl para health checks

### Cambios en [`requirements.txt`](requirements.txt:1):
- yt-dlp versión 2024.1.1 o superior (más actualizado)

**Paso 1:** Haz commit y push de los cambios
```bash
git add .
git commit -m "Fix YouTube bot detection"
git push
```

**Paso 2:** En Coolify, haz clic en "Redeploy"

## Solución 2: Usar Cookies (Si la Solución 1 no funciona)

Si YouTube sigue bloqueando, necesitas usar cookies de tu cuenta de YouTube.

### Paso 1: Exportar Cookies desde tu navegador

**Opción A: Usar extensión de Chrome**
1. Instala la extensión "Get cookies.txt LOCALLY" en Chrome
2. Ve a youtube.com e inicia sesión
3. Haz clic en la extensión y exporta las cookies
4. Guarda el archivo como `cookies.txt`

**Opción B: Usar yt-dlp directamente**
```bash
# En tu computadora local
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "URL_DEL_VIDEO"
```

### Paso 2: Subir cookies.txt al repositorio

1. Crea un archivo `cookies.txt` en la raíz del proyecto
2. **IMPORTANTE:** No incluyas información sensible en commits públicos
3. Agrega el archivo al repositorio

### Paso 3: Actualizar [`app.py`](app.py:59)

Descomenta la línea:
```python
"cookiefile": "/app/cookies.txt",
```

### Paso 4: Actualizar [`Dockerfile`](Dockerfile:1)

Agrega:
```dockerfile
# Copy cookies file (if exists)
COPY cookies.txt /app/cookies.txt 2>/dev/null || true
```

## Solución 3: Usar un Proxy (Último Recurso)

Si nada funciona, puedes usar un proxy para cambiar tu IP.

### Actualizar [`app.py`](app.py:46):

```python
ydl_opts = {
    # ... otras opciones ...
    "proxy": "http://user:password@proxy-server:port",
}
```

## Solución 4: Usar API de YouTube (Alternativa)

Considera usar la API oficial de YouTube si necesitas descargar muchos videos:
- [YouTube Data API](https://developers.google.com/youtube/v3)
- Requiere API key y cuota limitada

## Recomendaciones

1. **Prueba primero la Solución 1** - Debería funcionar para la mayoría de videos
2. **Si falla, usa Solución 2** - Cookies son más confiables
3. **Para producción**, considera rotar cookies o usar múltiples cuentas
4. **Monitorea los errores** - YouTube cambia sus medidas frecuentemente

## Variables de Entorno para Cookies

Para mayor seguridad, puedes usar cookies como variable de entorno:

### En Coolify:
```
YOUTUBE_COOKIES=cookie1=value1; cookie2=value2; ...
```

### En [`app.py`](app.py:46):
```python
import os

# Obtener cookies de variable de entorno
cookies_env = os.environ.get("YOUTUBE_COOKIES", "")

if cookies_env:
    ydl_opts["cookiefile"] = "/app/cookies.txt"
    # Crear archivo de cookies desde variable de entorno
    with open("/app/cookies.txt", "w") as f:
        f.write(cookies_env)
```

## Verificación

Después de implementar cualquier solución:

1. Haz redeploy en Coolify
2. Prueba con un video de YouTube
3. Revisa los logs en Coolify
4. Si sigue fallando, prueba con un video diferente (algunos tienen más restricciones)

## Notas Importantes

- YouTube cambia sus medidas de seguridad frecuentemente
- Las cookies expiran después de un tiempo
- No compartas cookies de tu cuenta personal públicamente
- Considera usar una cuenta separada solo para descargas
- El abuso puede llevar a bloqueo de IP

## Recursos

- [yt-dlp Wiki - Cookies](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
- [yt-dlp Wiki - YouTube Cookies](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies)
- [Coolify Documentation](https://coolify.io/docs)