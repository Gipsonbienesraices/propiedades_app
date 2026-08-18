@echo off
echo Subiendo correcciones de funcion editar...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correcciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con correcciones de editar...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix editar function with error handling for old data and missing images"
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
echo ¡Correcciones de editar subidas exitosamente!
echo ==========================================
echo.
echo Cambios implementados:
echo - Manejo de errores try/except en editar
echo - Compatibilidad con datos antiguos (columna ruta)
echo - Compatibilidad con propiedades sin imagenes
echo - Manejo de errores en index y ver_propiedad
echo - Placeholder si las URLs de imagenes fallan
echo - Mensajes de error informativos
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. La funcion editar ya no colapsara
echo 2. Funcionara con datos antiguos
echo 3. Funcionara con propiedades sin imagenes
echo.
pause