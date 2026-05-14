# Script para codificar cookies.txt en base64
# Ejecutar en PowerShell

$cookiesPath = "D:\Desarrollo\tools\descargar-instagram\cookies.txt"

# Verificar que el archivo existe
if (-not (Test-Path $cookiesPath)) {
    Write-Host "Error: No se encuentra el archivo cookies.txt en: $cookiesPath" -ForegroundColor Red
    exit 1
}

# Leer el archivo y codificar en base64
$base64String = [Convert]::ToBase64String([IO.File]::ReadAllBytes($cookiesPath))

# Mostrar informacion
Write-Host "Archivo: $cookiesPath" -ForegroundColor Green
Write-Host "Tamano original: $([IO.File]::ReadAllBytes($cookiesPath).Length) bytes" -ForegroundColor Green
Write-Host "Tamano base64: $($base64String.Length) caracteres" -ForegroundColor Green
Write-Host ""

# Copiar al portapapeles
$base64String | Set-Clipboard
Write-Host "Contenido codificado en base64 y copiado al portapapeles" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pasos siguientes:" -ForegroundColor Yellow
Write-Host "1. Ve a Coolify - tu servicio - Environment Variables" -ForegroundColor White
Write-Host "2. Borra la variable YOUTUBE_COOKIES" -ForegroundColor White
Write-Host "3. Crea nueva variable:" -ForegroundColor White
Write-Host "   - Name: COOKIES_BASE64" -ForegroundColor White
Write-Host "   - Value: (pega el contenido del portapapeles)" -ForegroundColor White
Write-Host "4. Guarda y haz Redeploy" -ForegroundColor White
Write-Host ""
Write-Host "El contenido codificado esta en tu portapapeles listo para pegar." -ForegroundColor Green
