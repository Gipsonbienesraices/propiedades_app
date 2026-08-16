@echo off
echo Subiendo cambios de autenticación a GitHub...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de autenticación...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con sistema de autenticación...
"C:\Program Files\Git\bin\git.exe" commit -m "Add authentication system with login/logout and admin protection"
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
echo ¡Sistema de autenticación subido exitosamente!
echo ==========================================
echo.
echo Cambios implementados:
echo - Sistema de login/logout con Flask-Login
echo - Protección de rutas de administración
echo - Botones de edición/eliminación solo para usuarios autenticados
echo - Funciones para editar y eliminar propiedades
echo - Tabla de usuarios en base de datos
echo - Usuario admin por defecto (admin/admin123)
echo.
echo Render detectará los cambios y redeployará automáticamente.
echo Después del deploy, deberás:
echo 1. Iniciar sesión con admin/admin123
echo 2. Cambiar la contraseña por defecto
echo.
pause