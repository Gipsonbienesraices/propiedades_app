@echo off
echo Subiendo correcciones de debugging para editar...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de correcciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con debugging detallado...
"C:\Program Files\Git\bin\git.exe" commit -m "Add detailed debugging to editar function to identify error source"
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
echo ¡Debugging detallado subido!
echo ==========================================
echo.
echo Cambios implementados:
echo - Prints detallados en cada paso de editar
echo - Print de propiedad obtenida
echo - Print de imagenes obtenidas y procesadas
echo - Print de cada fila de imagen
echo - Print antes de renderizar editar.html
echo - Traceback completo en excepciones
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Intenta editar la propiedad nueva
echo 2. Revisa los logs de Render para ver los prints
echo 3. Los logs mostraran exactamente donde falla
echo 4 - Con esa informacion podremos corregir el error
echo.
pause