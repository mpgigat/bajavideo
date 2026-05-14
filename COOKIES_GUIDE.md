# Cómo Crear cookies.txt para YouTube

## Método 1: Extensión de Chrome (Más Fácil para Windows)

### Paso 1: Instala la extensión

1. Ve a [Chrome Web Store](https://chrome.google.com/webstore)
2. Busca "Get cookies.txt LOCALLY"
3. Instala la extensión

### Paso 2: Exporta cookies

1. Ve a youtube.com e inicia sesión
2. Haz clic en la extensión en la barra de herramientas
3. Haz clic en "Export" o "Download"
4. Guarda el archivo como `cookies.txt`

### Paso 3: Coloca el archivo en el proyecto

Mueve `cookies.txt` a la raíz del proyecto:
```
descargar-instagram/
├── app.py
├── cookies.txt  <-- Este archivo
├── Dockerfile
├── requirements.txt
└── static/
```

### Paso 4: Sube al repositorio

```bash
git add cookies.txt
git commit -m "Add YouTube cookies"
git push
```

### Paso 5: Redeploy en Coolify

1. Ve a tu servicio en Coolify
2. Haz clic en "Redeploy"
3. Espera a que se complete

## Método 2: yt-dlp con Chrome (Solo si el Método 1 falla)

### Para Windows - Cierra Chrome primero

**IMPORTANTE:** Cierra completamente Google Chrome antes de ejecutar este comando.

```bash
# En PowerShell
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=aKM-vAvJhsI"
```

**Si sigue fallando, cierra Chrome y usa Edge:**

```bash
# En PowerShell
yt-dlp --cookies-from-browser edge --cookies cookies.txt "https://www.youtube.com/watch?v=aKM-vAvJhsI"
```

### Para macOS/Linux

```bash
# Cierra Chrome primero
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=aKM-vAvJhsI"
```

**Nota:** Reemplaza `chrome` con tu navegador:
- `chrome` - Google Chrome
- `firefox` - Mozilla Firefox
- `edge` - Microsoft Edge
- `brave` - Brave Browser
- `opera` - Opera

### Paso 3: Copia el archivo al proyecto

Mueve el archivo `cookies.txt` a la raíz de tu proyecto:
```
descargar-instagram/
├── app.py
├── cookies.txt  <-- Este archivo
├── Dockerfile
├── requirements.txt
└── static/
```

### Paso 4: Sube al repositorio

```bash
git add cookies.txt
git commit -m "Add YouTube cookies"
git push
```

### Paso 5: Redeploy en Coolify

1. Ve a tu servicio en Coolify
2. Haz clic en "Redeploy"
3. Espera a que se complete

## Método Alternativo: Extensión de Chrome

### Paso 1: Instala la extensión

1. Ve a [Chrome Web Store](https://chrome.google.com/webstore)
2. Busca "Get cookies.txt LOCALLY"
3. Instala la extensión

### Paso 2: Exporta cookies

1. Ve a youtube.com e inicia sesión
2. Haz clic en la extensión en la barra de herramientas
3. Haz clic en "Export" o "Download"
4. Guarda el archivo como `cookies.txt`

### Paso 3: Coloca el archivo en el proyecto

Mueve `cookies.txt` a la raíz del proyecto y sigue los pasos 4 y 5 del método anterior.

## Importante

- **No compartas tu archivo cookies.txt públicamente** - Contiene tu sesión de YouTube
- **Las cookies expiran** - Necesitarás actualizarlas periódicamente
- **Usa una cuenta separada** - No uses tu cuenta principal de YouTube
- **El archivo se incluye en la imagen Docker** - No se actualiza dinámicamente

## Verificación

Después del redeploy, revisa los logs en Coolify. Deberías ver:
```
Using cookies file for authentication
```

Si ves:
```
No cookies file found, proceeding without authentication
```

El archivo no se copió correctamente. Verifica que:
1. El archivo existe en el repositorio
2. El nombre es exactamente `cookies.txt` (no Cookies.txt ni cookies.txt.txt)
3. El archivo está en la raíz del proyecto

## Actualizar Cookies

Cuando las cookies expiren (aproximadamente 30-60 días):

1. Genera un nuevo archivo `cookies.txt` siguiendo los pasos anteriores
2. Haz commit y push
3. Redeploy en Coolify

## Solución de Problemas

### Error: "cookies.txt not found"
- Verifica que el archivo esté en la raíz del proyecto
- Verifica el nombre exacto del archivo (minúsculas)

### Error: "Cookies expired"
- Genera un nuevo archivo cookies.txt
- Haz redeploy

### Error: "Invalid cookies format"
- Asegúrate de usar yt-dlp o la extensión recomendada
- El formato debe ser Netscape cookie format

## Seguridad

Para mayor seguridad, puedes usar variables de entorno en lugar de un archivo:

1. Codifica el contenido de cookies.txt en base64:
```bash
base64 -w 0 cookies.txt
```

2. Agrega la variable en Coolify:
```
COOKIES_BASE64=contenido_codificado
```

3. Actualiza app.py para decodificar:
```python
import base64

cookies_base64 = os.environ.get("COOKIES_BASE64", "")
if cookies_base64:
    cookies_content = base64.b64decode(cookies_base64).decode('utf-8')
    with open("/app/cookies.txt", "w") as f:
        f.write(cookies_content)
```

Esta opción es más segura pero requiere más configuración.