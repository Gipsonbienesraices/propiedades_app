@echo off
echo Subiendo integracion de YouTube a GitHub...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de YouTube...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con integracion de YouTube...
"C:\Program Files\Git\bin\git.exe" commit -m "Add YouTube video integration for properties"
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
echo ¡Integracion de YouTube subida exitosamente!
echo ==========================================
echo.
echo Cambios implementados:
echo - Campo youtube_url en base de datos
echo - Funcion para extraer ID de YouTube
echo - Campo opcional en registrar.html
echo - Campo opcional en editar.html
echo - Reproductor integrado en index.html
echo - Documentacion completa de YouTube
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. La columna youtube_url se agregara automaticamente
echo 2. Podras agregar videos de YouTube a las propiedades
echo 3. Los videos se mostraran como reproductores integrados
echo.
pause