@echo off
echo Subiendo correcciones de YouTube Shorts y editar...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correcciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con correcciones...
"C:\Program Files\Git\bin\git.exe" commit -m "Add YouTube Shorts support and fix editar image loading logic"
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
echo ¡Correcciones subidas exitosamente!
echo ==========================================
echo.
echo Cambios implementados:
echo - Soporte para YouTube Shorts
echo - Mejor manejo de columnas de imagenes
echo - Correccion de logica de separacion de URLs
echo - Debug prints para solucionar errores
echo - Filtros Jinja mejorados en editar.html
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. YouTube Shorts seran reconocidos
echo 2. El formulario de editar deberia funcionar
echo 3 - Los logs mostraran informacion de debug
echo.
pause