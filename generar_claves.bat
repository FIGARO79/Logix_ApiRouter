@echo off
REM Script para generar claves secretas seguras para produccion

echo ========================================
echo Generador de Claves Seguras
echo ========================================
echo.
echo Generando claves aleatorias seguras...
echo.

python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
echo.
python -c "import secrets; print('UPDATE_PASSWORD=' + secrets.token_urlsafe(24))"

echo.
echo ========================================
echo Copia estas lineas a tu archivo .env
echo ========================================
echo.
echo IMPORTANTE:
echo - NO uses estas claves en desarrollo local
echo - Guarda estas claves en un lugar seguro
echo - Nunca compartas estas claves publicamente
echo - Cambia las claves regularmente
echo.
pause
