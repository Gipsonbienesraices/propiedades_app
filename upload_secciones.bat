@echo off
echo Subiendo organizacion por secciones tematicas...
echo.

cd /d C:\Users\USER\propiedades_app

echo Agregando todos los archivos de secciones...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error al agregar archivos
    pause
    exit /b 1
)

echo Haciendo commit con secciones tematicas...
"C:\Program Files\Git\bin\git.exe" commit -m "Organize catalog by property type sections (Casas, Terrenos, Departamentos)"
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
echo ¡Organizacion por secciones completada!
echo ==========================================
echo.
echo Cambios implementados:
echo - Backend: Agrupacion de propiedades por tipo
echo - Frontend: Secciones con titulos grandes
echo - Estilos CSS: Titulos con borde azul
echo - Limpieza: Sin alterar BD ni funcionalidad existente
echo.
echo Secciones creadas:
echo - Casas
echo - Terrenos  
echo - Departamentos
echo - Otro (para tipos no especificados)
echo.
echo Render detectara los cambios y redeployara automaticamente.
echo Despues del deploy:
echo 1. Propiedades organizadas por tipo
echo 2 - Titulos grandes antes de cada seccion
echo 3 - Secciones vacias no se muestran
echo 4 - Funcionalidad completa mantenida
echo.
pause