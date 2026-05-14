# Solución: Variable de Entorno Truncada en Coolify

## El Problema

La variable de entorno `YOUTUBE_COOKIES` está truncada a solo 27 caracteres en lugar de tener el contenido completo del archivo cookies.txt.

## Causas Posibles

1. **Límite de caracteres en el campo de texto de Coolify**
2. **Problema al copiar/pegar el contenido**
3. **Formato del contenido (saltos de línea, tabulaciones)**

## Soluciones

### Solución 1: Usar Base64 (Recomendada)

Esta solución codifica el contenido en base64 para evitar problemas con caracteres especiales y saltos de línea.

#### Paso 1: Codificar cookies.txt en base64

**En PowerShell:**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("D:\Desarrollo\tools\descargar-instagram\cookies.txt"))
```

**En Linux/macOS:**
```bash
base64 -w 0 cookies.txt
```

Esto te dará una cadena larga de caracteres alfanuméricos.

#### Paso 2: Crear variable de entorno en Coolify

1. Ve a tu servicio en Coolify
2. Environment Variables
3. Agrega nueva variable:
   - **Name:** `COOKIES_BASE64`
   - **Value:** (pega la cadena codificada en base64)

#### Paso 3: Actualizar el código

Necesitamos modificar [`app.py`](app.py:1) para decodificar desde base64.

### Solución 2: Usar Archivo en Repositorio Privado

Si Coolify tiene límites en variables de entorno:

1. Haz tu repositorio **privado** en GitHub/GitLab
2. Sube el archivo `cookies.txt` al repositorio
3. Configura Coolify para acceder al repositorio privado con SSH key o token

### Solución 3: Usar Secret de Coolify (si está disponible)

Algunas versiones de Coolify soportan "Secrets" que pueden manejar contenido más grande:

1. Ve a tu servicio en Coolify
2. Busca la sección "Secrets" o "Files"
3. Crea un archivo `cookies.txt` con el contenido completo
4. Monta el archivo en `/app/cookies.txt`

### Solución 4: Dividir en Múltiples Variables

Si el contenido es muy grande, puedes dividirlo:

1. Divide cookies.txt en partes (por ejemplo, 5 partes)
2. Crea variables: `COOKIES_PART_1`, `COOKIES_PART_2`, etc.
3. Modifica el código para unir las partes

## Implementación de Solución 1 (Base64)

### Actualizar app.py

```python
# Check for cookies from environment variable or file
cookies_file = "/app/cookies.txt"
cookies_env = os.environ.get("YOUTUBE_COOKIES", "")
cookies_base64 = os.environ.get("COOKIES_BASE64", "")

logger.info(f"Environment variable YOUTUBE_COOKIES exists: {bool(cookies_env)}")
logger.info(f"Environment variable COOKIES_BASE64 exists: {bool(cookies_base64)}")

# Create cookies file from base64 if provided
if cookies_base64:
    try:
        import base64
        cookies_content = base64.b64decode(cookies_base64).decode('utf-8')
        with open(cookies_file, "w") as f:
            f.write(cookies_content)
        logger.info(f"Created cookies file from base64, size: {len(cookies_content)} bytes")
    except Exception as e:
        logger.error(f"Error creating cookies file from base64: {e}")
# Create cookies file from environment variable if provided
elif cookies_env:
    try:
        with open(cookies_file, "w") as f:
            f.write(cookies_env)
        logger.info(f"Created cookies file from environment variable, size: {len(cookies_env)} bytes")
    except Exception as e:
        logger.error(f"Error creating cookies file: {e}")
```

## Pasos Inmediatos

### Opción A: Implementar Base64 (Recomendada)

1. Ejecuta este comando en PowerShell:
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("D:\Desarrollo\tools\descargar-instagram\cookies.txt")) | Set-Clipboard
```

2. En Coolify:
   - Borra la variable `YOUTUBE_COOKIES`
   - Crea nueva variable `COOKIES_BASE64`
   - Pega el contenido (ya está en el portapapeles)

3. Actualiza el código en [`app.py`](app.py:1) con el código de arriba

4. Haz commit, push y redeploy

### Opción B: Repositorio Privado

1. Haz el repositorio privado en GitHub
2. Agrega cookies.txt al repositorio
3. Configura Coolify con tu SSH key de GitHub
4. Redeploy

## Verificación

Después de implementar cualquiera de las soluciones, los logs deberían mostrar:

```
Environment variable COOKIES_BASE64 exists: True
Created cookies file from base64, size: 2500+ bytes
Cookies file exists: True
Cookies file size: 2500+ bytes
Using cookies file for authentication
```

## ¿Cuál solución prefieres?

- **Base64**: Más segura, funciona con repositorio público
- **Repositorio Privado**: Más simple, pero requiere repositorio privado
- **Secrets/Files**: Mejor si Coolify lo soporta

¿Cuál prefieres implementar?