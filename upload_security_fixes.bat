@echo off
echo Subiendo correcciones de seguridad y fixes de imágenes a GitHub...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de seguridad y fixes...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con correcciones de seguridad y fixes...
"C:\Program Files\Git\bin\git.exe" commit -m "Fix image folder creation and add secure password change functionality"
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
echo - Carpeta imagenes_propiedades se crea automaticamente
echo - Credenciales ocultas en login.html
echo - Sistema seguro para cambiar contrasena
echo - Nueva plantilla cambiar_password.html
echo - Boton Cambiar Contrasena en navegacion
echo - Documentacion actualizada
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Inicia sesion con admin/admin123
echo 2. Click en Cambiar Contrasena inmediatamente
echo 3. Prueba subir una propiedad con imagenes
echo.
pause