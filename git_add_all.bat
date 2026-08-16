@echo off
echo Agregando todos los archivos nuevos y subiendo a GitHub...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con todos los archivos de migración...
"C:\Program Files\Git\bin\git.exe" commit -m "Add PostgreSQL migration files and Render auto-configuration"
if %errorlevel% neq 0 (
    echo Error al hacer commit
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
echo ¡Todos los cambios subidos exitosamente!
echo ==========================================
echo.
echo Archivos subidos:
echo - migrate.py (script de migración)
echo - start.sh (script de inicio automático)
echo - INSTRUCCIONES_MIGRACION.md (guía de migración)
echo - render.yaml (configuración actualizada)
echo - .env (configuración local)
echo.
echo Render detectará los cambios y redeployará automáticamente.
echo El script start.sh ejecutará la migración automáticamente.
echo.
pause