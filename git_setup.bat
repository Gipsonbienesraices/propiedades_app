@echo off
echo Configurando Git y subiendo cambios a GitHub...
echo.

cd /d C:\Users\USER\propiedades_app

echo Inicializando repositorio Git...
"C:\Program Files\Git\bin\git.exe" init
if %errorlevel% neq 0 (
    echo Error al inicializar git
    pause
    exit /b 1
)

echo Agregando archivos...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit...
"C:\Program Files\Git\bin\git.exe" commit -m "Add PostgreSQL migration script and Render configuration"
if %errorlevel% neq 0 (
    echo Error al hacer commit
    pause
    exit /b 1
)

echo Renombrando rama a main...
"C:\Program Files\Git\bin\git.exe" branch -M main
if %errorlevel% neq 0 (
    echo Error al renombrar rama
    pause
    exit /b 1
)

echo Conectando a GitHub...
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/Gipsonbienesraices/propiedades_app.git
if %errorlevel% neq 0 (
    echo El remoto ya existe, continuando...
)

echo Subiendo cambios a GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main
if %errorlevel% neq 0 (
    echo Error al subir a GitHub. Verifica tus credenciales.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ¡Cambios subidos exitosamente a GitHub!
echo ==========================================
echo.
echo Render detectará los cambios automáticamente y redeployará.
echo.
pause