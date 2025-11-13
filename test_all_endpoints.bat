@echo off
echo Testando todos os endpoints da API VacaFacil
echo.

echo Iniciando servidor...
start python test_server.py

echo Aguardando servidor iniciar...
timeout /t 5 /nobreak > nul

echo.
echo Executando testes automatizados...
python test_endpoints_simple.py

echo.
echo Pressione qualquer tecla para abrir documentacao Swagger...
pause > nul

start http://localhost:8000/docs

echo.
echo Testes concluidos!
pause