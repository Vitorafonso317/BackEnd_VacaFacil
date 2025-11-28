@echo off
echo ========================================
echo   VacaFacil Backend - Iniciando...
echo ========================================
echo.

REM Verificar se está no diretório correto
if not exist "app\main.py" (
    echo ERRO: Arquivo app\main.py nao encontrado!
    echo Execute este script do diretorio raiz do projeto.
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo AVISO: Ambiente virtual nao encontrado.
    echo Certifique-se de ter as dependencias instaladas.
    echo.
)

REM Verificar se uvicorn está instalado
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo ERRO: uvicorn nao esta instalado!
    echo Execute: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Iniciando servidor na porta 5000...
echo Acesse: http://localhost:5000
echo Documentacao: http://localhost:5000/docs
echo.
echo Pressione CTRL+C para parar o servidor
echo ========================================
echo.

uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload