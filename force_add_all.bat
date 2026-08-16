@echo off
echo Forzando agregar todos los archivos y subiendo a GitHub...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos incluyendo los nuevos...
"C:\Program Files\Git\bin\git.exe" add -A
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Verificando estado...
"C:\Program Files\Git\bin\git.exe" status

echo.
echo Haciendo commit con todos los archivos de migración y configuración...
"C:\Program Files\Git\bin\git.exe" commit -m "Complete migration setup: migrate.py, start.sh, INSTRUCCIONES_MIGRACION.md, render.yaml, .env.example"
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
echo ¡Todos los cambios subidos exitosamente!
echo ==========================================
echo.
pause