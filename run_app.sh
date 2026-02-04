#!/bin/bash
# Script de Inicialização - Interface Gráfica IBAN Extraction System
# Chartered Accountants Ireland

echo "========================================"
echo " IBAN Extraction System - Web Interface"
echo " Chartered Accountants Ireland"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERRO] Ambiente virtual não encontrado!"
    echo "Por favor, execute: python -m venv venv"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "[INFO] Ativando ambiente virtual..."
source venv/bin/activate

# Check if Streamlit is installed
if ! pip show streamlit > /dev/null 2>&1; then
    echo "[AVISO] Streamlit não instalado. Instalando dependências..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[AVISO] Arquivo .env não encontrado!"
    echo "Por favor, copie .env.example para .env e configure suas credenciais."
    echo ""
    cp .env.example .env
    echo "Arquivo .env criado. Configure-o antes de continuar."
    read -p "Pressione Enter para continuar..."
fi

echo ""
echo "[INFO] Iniciando interface web..."
echo "[INFO] A aplicação será aberta em seu navegador padrão"
echo "[INFO] URL: http://localhost:8501"
echo ""
echo "Pressione Ctrl+C para encerrar o servidor"
echo "========================================"
echo ""

# Start Streamlit
streamlit run app.py --server.port 8501 --server.address localhost
