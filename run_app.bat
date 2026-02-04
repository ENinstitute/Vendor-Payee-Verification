@echo off
REM Script de Inicialização - Interface Gráfica IBAN Extraction System
REM Chartered Accountants Ireland

echo ========================================
echo  IBAN Extraction System - Web Interface
echo  Chartered Accountants Ireland
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Por favor, execute: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Check if Streamlit is installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Streamlit nao instalado. Instalando dependencias...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    echo Por favor, copie .env.example para .env e configure suas credenciais.
    echo.
    copy .env.example .env
    echo Arquivo .env criado. Configure-o antes de continuar.
    pause
)

echo.
echo [INFO] Iniciando interface web...
echo [INFO] A aplicacao sera aberta em seu navegador padrao
echo [INFO] URL: http://localhost:8501
echo.
echo Pressione Ctrl+C para encerrar o servidor
echo ========================================
echo.

REM Start Streamlit
streamlit run app.py --server.port 8501 --server.address localhost

pause
