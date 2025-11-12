@echo off
echo Iniciando VacaFacil Backend...

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Ambiente virtual ativado
) else (
    echo Ambiente virtual nao encontrado. Criando...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

REM Executar aplicacao
echo Iniciando servidor FastAPI...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause