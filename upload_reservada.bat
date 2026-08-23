@echo off
echo Subiendo funcionalidad de estado de reserva...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de reserva...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con funcionalidad de reserva...
"C:\Program Files\Git\bin\git.exe" commit -m "Add reservation status feature - reservada field and RESERVADA label"
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
echo ¡Funcionalidad de reserva agregada!
echo ==========================================
echo.
echo Cambios implementados:
echo - Campo reservada en base de datos
echo - Checkbox en formulario de registro
echo - Checkbox en formulario de edicion
echo - Etiqueta RESERVADA en index.html
echo - Etiqueta RESERVADA en ver_propiedad.html
echo - Migracion automatica para BD existentes
echo.
echo Funcionalidad mantenida:
echo - YouTube Shorts intacto
echo - URLs de imagenes intacto
echo - Secciones tematicas intactas
echo - Todas las funciones existentes
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Campo reservada agregado a BD
echo 2 - Checkbox disponible en formularios
echo 3 - Etiqueta verde RESERVADA visible
echo 4 - Funcionalidad completa
echo.
pause