@echo off
echo Subiendo correccion de error Jinja selectattr True...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correcciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con correccion de Jinja...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix Jinja template error - replace selectattr with proper conditional loop"
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
echo ¡Error Jinja corregido!
echo ==========================================
echo.
echo Error encontrado:
echo - selectattr('es_principal', True) causaba "No test named True"
echo.
echo Correccion aplicada:
echo - Reemplazado selectattr con loop for condicional
echo - Sintaxis: {% for imagen in imagenes if imagen.es_principal %}
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. El formulario de editar deberia cargar correctamente
echo 2 - No mas error "No test named True"
echo 3 - La imagen principal se mostrara correctamente
echo.
pause