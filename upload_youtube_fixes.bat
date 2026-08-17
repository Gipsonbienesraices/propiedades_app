@echo off
echo Subiendo correcciones de visualizacion de YouTube y detalles...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correcciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con correcciones de YouTube y detalles...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix YouTube video display and add property details page"
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
echo ¡Correcciones subidas exitosamente!
echo ==========================================
echo.
echo Cambios implementados:
echo - Mejor visualizacion de videos de YouTube
echo - Boton Ver en YouTube para movil
echo - Nueva ruta para ver detalles individuales
echo - Plantilla ver_propiedad.html completa
echo - Tarjetas clickeables para ver detalles
echo - Efecto hover en tarjetas
echo - Iconos de Bootstrap mejorados
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Los videos de YouTube se mostraran correctamente
echo 2. Podras hacer clic en las tarjetas para ver detalles
echo 3. Tendra una pagina dedicada para cada propiedad
echo 4. Los botones de YouTube funcionaran en movil
echo.
pause