@echo off
echo Subiendo correccion de migracion de columna reservada...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de migracion...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con migracion mejorada...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix reservada column migration - run init_db on startup and add fallback method"
if %errorlevel% neq 0 (
    echo No hay cambios o error al hacer commit
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
echo ¡Migracion de columna reservada corregida!
echo ==========================================
echo.
echo Cambios implementados:
echo - init_db() se ejecuta al inicio (no solo local)
echo - Metodo alternativo para PostgreSQL sin IF NOT EXISTS
echo - Verificacion de columna antes de agregar
echo - Debug prints para migracion
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. init_db() se ejecutara al inicio
echo 2 - Columna reservada se agregara si no existe
echo 3 - Metodo alternativo si el primero falla
echo 4 - Logs mostraran estado de migracion
echo.
pause