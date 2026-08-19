@echo off
echo Eliminando boton de Iniciar Sesion del navbar publico...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando cambios de navbar...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con eliminacion de boton login...
"C:\Program Files\Git\bin\git.exe" commit -m "Remove login button from public navbar - keep /login route active"
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
echo ¡Boton de login eliminado del navbar!
echo ==========================================
echo.
echo Cambios implementados:
echo - Eliminado enlace "Iniciar Sesion" del navbar publico
echo - Ruta /login sigue activa en backend
echo - Acceso manual via URL: /login
echo - Navbar solo muestra opciones cuando esta autenticado
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. El publico no vera el boton de login
echo 2. El admin puede acceder via /login manualmente
echo 3. El navbar se mostrara vacio para usuarios no autenticados
echo.
pause