"""
Script to translate UI pages from Portuguese to English
"""

import re
from pathlib import Path

# Translation dictionary
translations = {
    # Headers and titles
    "Sistema de Extração de IBAN": "IBAN Extraction System",
    "Bem-vindo ao": "Welcome to",
    "Painel de Controle": "Control Panel",
    "Dashboard Principal": "Main Dashboard",
    
    # Navigation and sections
    "Início": "Home",
    "Início Rápido": "Quick Start",
    "Treinamento": "Training",
    "Processamento": "Processing",
    "Resultados": "Results",
    "Configurações": "Settings",
    
    # Status
    "Status do Sistema": "System Status",
    "Estatísticas": "Statistics",
    "Estatísticas Rápidas": "Quick Stats",
    "Conectado": "Connected",
    "Não configurado": "Not configured",
    "Ambiente": "Environment",
    
    # Metrics
    "Faturas Treinadas": "Trained Invoices",
    "Faturas Processadas": "Processed Invoices",
    "Confiança Média": "Average Confidence",
    "Taxa de Sucesso": "Success Rate",
    "Extrações Hoje": "Extractions Today",
    "Total de Extrações": "Total Extractions",
    
    # Actions
    "Carregar": "Upload",
    "Carregar Arquivos": "Upload Files",
    "Processar": "Process",
    "Baixar": "Download",
    "Exportar": "Export",
    "Limpar": "Clear",
    "Salvar": "Save",
    "Cancelar": "Cancel",
    "Confirmar": "Confirm",
    "Enviar": "Submit",
    "Buscar": "Search",
    "Filtrar": "Filter",
    
    # Messages
    "Sucesso": "Success",
    "Erro": "Error",
    "Aviso": "Warning",
    "Informação": "Information",
    "Aguarde": "Please wait",
    "Processando": "Processing",
    "Concluído": "Completed",
    "Falhou": "Failed",
    
    # Fields
    "Nome": "Name",
    "Descrição": "Description",
    "Data": "Date",
    "Arquivo": "File",
    "Arquivos": "Files",
    "Pasta": "Folder",
    "Formato": "Format",
    "Tamanho": "Size",
    
    # Training page
    "Treinar Modelo": "Train Model",
    "Carregar Faturas de Treinamento": "Upload Training Invoices",
    "Parâmetros de Treinamento": "Training Parameters",
    "Iniciar Treinamento": "Start Training",
    
    # Processing page
    "Processar Faturas": "Process Invoices",
    "Carregar Faturas": "Upload Invoices",
    "Opções de Processamento": "Processing Options",
    "Iniciar Processamento": "Start Processing",
    
    # Results page
    "Visualizar Resultados": "View Results",
    "Extrações Recentes": "Recent Extractions",
    "Distribuição de Confiança": "Confidence Distribution",
    "Alertas": "Alerts",
    
    # Settings page
    "Configuração da API": "API Configuration",
    "Configuração do Banco de Dados": "Database Configuration",
    "Configurações de Performance": "Performance Settings",
    "Configurações de Segurança": "Security Settings",
    
    # Common phrases
    "Selecione um arquivo": "Select a file",
    "Nenhum arquivo selecionado": "No file selected",
    "Arraste e solte arquivos aqui": "Drag and drop files here",
    "ou clique para selecionar": "or click to select",
    "Por favor, configure": "Please configure",
    "Clique aqui para": "Click here to",
}

def translate_file(filepath):
    """Translate a single file"""
    print(f"Translating {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    for pt, en in translations.items():
        # Case-sensitive replacement for exact matches
        content = content.replace(f'"{pt}"', f'"{en}"')
        content = content.replace(f"'{pt}'", f"'{en}'")
        content = content.replace(f"**{pt}**", f"**{en}**")
        content = content.replace(f"### {pt}", f"### {en}")
        content = content.replace(f"## {pt}", f"## {en}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Translated {filepath}")

def main():
    """Main function"""
    ui_dir = Path("src/ui")
    
    # Translate all UI pages
    ui_files = [
        "main_page.py",
        "training_page.py",
        "processing_page.py",
        "results_page.py",
        "settings_page.py"
    ]
    
    for filename in ui_files:
        filepath = ui_dir / filename
        if filepath.exists():
            translate_file(filepath)
        else:
            print(f"! File not found: {filepath}")
    
    print("\n✅ Translation completed!")

if __name__ == "__main__":
    main()
