@echo off
echo ========================================
echo   VacaFacil - Verificacao do Sistema
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python NAO instalado
) else (
    echo [OK] Python instalado
    python --version
)
echo.

REM Verificar estrutura
if exist "app\main.py" (
    echo [OK] Estrutura do projeto correta
) else (
    echo [X] Estrutura incorreta - app\main.py nao encontrado
)
echo.

REM Verificar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    echo [OK] Ambiente virtual encontrado
) else (
    echo [!] Ambiente virtual nao encontrado
    echo     Execute: python -m venv venv
)
echo.

REM Verificar dependencias
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -c "import fastapi, uvicorn, sqlalchemy" 2>nul
    if errorlevel 1 (
        echo [X] Dependencias NAO instaladas
        echo     Execute: pip install -r requirements.txt
    ) else (
        echo [OK] Dependencias principais instaladas
    )
) else (
    echo [!] Nao foi possivel verificar dependencias
)
echo.

REM Verificar banco de dados
if exist "vacafacil.db" (
    echo [OK] Banco de dados encontrado
) else (
    echo [!] Banco de dados sera criado na primeira execucao
)
echo.

REM Verificar .env
if exist ".env" (
    echo [OK] Arquivo .env encontrado
) else (
    echo [!] Arquivo .env nao encontrado
    echo     Copie .env.example para .env
)
echo.

echo ========================================
echo   Verificacao concluida!
echo ========================================
echo.
echo Para iniciar o servidor, execute: iniciar.bat
echo.
pause
