@echo off
echo Testando API VacaFacil
echo.

echo Iniciando servidor...
start python test_server.py

echo Aguardando servidor...
timeout /t 3 /nobreak > nul

echo Executando teste...
python test_api.py

echo.
echo Abrir documentacao? (S/N)
set /p choice=
if /i "%choice%"=="S" start http://localhost:8000/docs

echo Teste concluido!
pause