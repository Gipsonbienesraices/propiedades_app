@echo off
echo Verificando archivos en el directorio...
echo.

cd /d C:\Users\USER\propiedades_app

dir /b *.py
echo.
dir /b *.sh
echo.
dir /b *.md
echo.
dir /b *.yaml
echo.
dir /b .env*
echo.

pause