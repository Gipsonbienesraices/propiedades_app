@echo off
echo Subiendo cambio de sistema de imagenes a URLs externas...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos del cambio a URLs...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con cambio a sistema de URLs externas...
"C:\Program Files\Git\bin\git.exe" commit -m "Replace file upload with external URLs for images (Render compatibility)"
if %errorlevel% neq 0 (
    echo No hay cambios nuevos o error al hacer commit
    pause
    exit /b 1
)

echo Subiendo cambios a GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main
if %errorlevel% neq 0 (
    echo Error al subir a GitHub
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ¡Cambio a URLs externas subido exitosamente!
echo ==========================================
echo.
echo Cambios implementados:
echo - Sistema de imagenes cambiado a URLs externas
echo - Eliminada subida de archivos (Render borra archivos)
echo - Campo URL de imagen principal
echo - Campo URLs de galeria (separadas por comas)
echo - Migracion automatica de base de datos
echo - Imagenes cargadas desde URLs externas
echo - Manejo de errores con imagenes placeholder
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. La migracion actualizara la tabla imagenes
echo 2. Podras ingresar URLs de imagenes externas
echo 3. Las imagenes se cargaran desde URLs externas
echo 4. Ya no habra errores de archivos borrados
echo.
pause