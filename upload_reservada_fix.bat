@echo off
echo Subiendo correccion de campo reservada en editar...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correccion...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con correccion de reservada...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix reservada field handling in editar function with debug output"
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
echo ¡Correccion de reservada subida!
echo ==========================================
echo.
echo Cambios implementados:
echo - Debug prints para checkbox reservada
echo - Manejo de errores en SQL UPDATE
echo - Verificacion de lectura del checkbox
echo - Debug del valor booleano
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Los logs mostraran valores del checkbox
echo 2 - Podemos identificar el error exacto
echo 3 - La actualizacion deberia funcionar
echo.
pause