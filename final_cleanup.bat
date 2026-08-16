@echo off
echo Limpieza final y subida de .gitignore actualizado...
echo.

cd /d C:\Users\USER\propiedades_app

echo Eliminando archivos temporales...
del test_migration.py
del verify_git.bat
del check_files.bat
del force_add_all.bat
del git_add_all.bat
del git_setup.bat

echo Actualizando .gitignore...
"C:\Program Files\Git\bin\git.exe" add .gitignore
"C:\Program Files\Git\bin\git.exe" commit -m "Update .gitignore to exclude temporary scripts"
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ==========================================
echo ¡Limpieza completada y cambios subidos!
echo ==========================================
echo.
echo Archivos importantes en GitHub:
echo - app.py (aplicación principal)
echo - migrate.py (script de migración)
echo - start.sh (script de inicio automático)
echo - render.yaml (configuración de Render)
echo - INSTRUCCIONES_MIGRACION.md (guía completa)
echo - .env.example (plantilla de configuración)
echo - .gitignore (archivos excluidos)
echo.
echo Render detectará los cambios y redeployará.
echo El script start.sh ejecutará migrate.py automáticamente.
echo.
pause