@echo off
echo Subiendo configuracion exclusiva para YouTube Shorts...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correcciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con configuracion Shorts-only...
"C:\Program Files\Git\bin\git.exe" commit -m "Switch to YouTube Shorts only - remove horizontal video support"
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
echo ¡Configuracion Shorts-only subida!
echo ==========================================
echo.
echo Cambios implementados:
echo - Soporte exclusivo para YouTube Shorts
echo - Eliminado soporte para videos horizontales
echo - Aspect ratio vertical (9:16) en iframes
echo - Enlaces actualizados a /shorts/
echo - Contenedores optimizados para formato vertical
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Solo YouTube Shorts seran reconocidos
echo 2 - Videos apareceran en formato vertical
echo 3 - Enlaces apuntaran a youtube.com/shorts/
echo.
pause