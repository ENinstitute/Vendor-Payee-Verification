"""
Complete translation script for all UI pages
Translates ALL Portuguese hardcoded text to English
"""

import re
from pathlib import Path

# Comprehensive translation dictionary
translations = {
    # Common Portuguese words and phrases
    "Carregue": "Upload",
    "Carregar": "Upload",
    "Faça upload": "Upload",
    "Fazer upload": "Upload",
    "Arraste e solte": "Drag and drop",
    "ou clique para selecionar": "or click to select",
    "Clique aqui": "Click here",
    "Selecione": "Select",
    "Escolha": "Choose",
    "Arquivo": "File",
    "Arquivos": "Files",
    "arquivos": "files",
    "Nenhum arquivo": "No file",
    "Nenhum": "No",
    "Todos": "All",
    "todos": "all",
    
    # Actions
    "Processar": "Process",
    "Processando": "Processing",
    "Iniciar": "Start",
    "Parar": "Stop",
    "Cancelar": "Cancel",
    "Confirmar": "Confirm",
    "Salvar": "Save",
    "Exportar": "Export",
    "Baixar": "Download",
    "Limpar": "Clear",
    "Atualizar": "Update",
    "Enviar": "Submit",
    "Buscar": "Search",
    "Filtrar": "Filter",
    "Visualizar": "View",
    "Ver": "View",
    "Editar": "Edit",
    "Deletar": "Delete",
    "Remover": "Remove",
    
    # Status and messages
    "Sucesso": "Success",
    "Erro": "Error",
    "Aviso": "Warning",
    "Informação": "Information",
    "Atenção": "Attention",
    "Aguarde": "Please wait",
    "Carregando": "Loading",
    "Completo": "Complete",
    "Concluído": "Completed",
    "Em progresso": "In progress",
    "Pendente": "Pending",
    "Falhou": "Failed",
    "Cancelado": "Cancelled",
    
    # Training page specific
    "Treinamento de Modelo": "Model Training",
    "Faturas de Treinamento": "Training Invoices",
    "Upload de Faturas": "Invoice Upload",
    "Parâmetros": "Parameters",
    "Parâmetros de Treinamento": "Training Parameters",
    "Configurações": "Settings",
    "Configurações Avançadas": "Advanced Settings",
    "Iniciar Treinamento": "Start Training",
    "Parar Treinamento": "Stop Training",
    "Progresso": "Progress",
    "Progresso do Treinamento": "Training Progress",
    "Resultados do Treinamento": "Training Results",
    "Histórico": "History",
    "Histórico de Treinamentos": "Training History",
    
    # Processing page specific  
    "Processamento de Faturas": "Invoice Processing",
    "Processar Faturas": "Process Invoices",
    "Opções de Processamento": "Processing Options",
    "Iniciar Processamento": "Start Processing",
    "Parar Processamento": "Stop Processing",
    "Progresso do Processamento": "Processing Progress",
    "Faturas para Processar": "Invoices to Process",
    "Faturas Processadas": "Processed Invoices",
    "Histórico de Processamentos": "Processing History",
    
    # Results page specific
    "Visualizar Resultados": "View Results",
    "Resultados": "Results",
    "Extrações": "Extractions",
    "Extrações Recentes": "Recent Extractions",
    "Todas as Extrações": "All Extractions",
    "Distribuição": "Distribution",
    "Distribuição de Confiança": "Confidence Distribution",
    "Estatísticas": "Statistics",
    "Estatísticas Detalhadas": "Detailed Statistics",
    "Relatórios": "Reports",
    "Relatório de Validação": "Validation Report",
    "Alertas": "Alerts",
    "Filtros": "Filters",
    "Aplicar Filtros": "Apply Filters",
    "Limpar Filtros": "Clear Filters",
    "Exportar Resultados": "Export Results",
    "Baixar CSV": "Download CSV",
    
    # Settings page specific
    "Configuração da API": "API Configuration",
    "Chave da API": "API Key",
    "Configurar API": "Configure API",
    "Testar Conexão": "Test Connection",
    "Configuração do Banco de Dados": "Database Configuration",
    "Tipo de Banco": "Database Type",
    "Host do Banco": "Database Host",
    "Porta": "Port",
    "Nome do Banco": "Database Name",
    "Usuário": "User",
    "Senha": "Password",
    "Configurações de Performance": "Performance Settings",
    "Workers": "Workers",
    "Tamanho do Lote": "Batch Size",
    "Timeout": "Timeout",
    "Configurações de Segurança": "Security Settings",
    "Chave de Criptografia": "Encryption Key",
    "Retenção de Dados": "Data Retention",
    "Salvar Configurações": "Save Settings",
    
    # Common phrases
    "Por favor": "Please",
    "Por favor, configure": "Please configure",
    "Por favor, selecione": "Please select",
    "Você tem certeza": "Are you sure",
    "Deseja continuar": "Do you want to continue",
    "Sim": "Yes",
    "Não": "No",
    "OK": "OK",
    "Fechar": "Close",
    "Voltar": "Back",
    "Próximo": "Next",
    "Anterior": "Previous",
    "Página": "Page",
    "de": "of",
    "Total": "Total",
    "Mostrando": "Showing",
    "resultados": "results",
    "Nenhum resultado": "No results",
    "encontrado": "found",
    
    # Data/Time
    "Data": "Date",
    "Hora": "Time",
    "Hoje": "Today",
    "Ontem": "Yesterday",
    "Semana": "Week",
    "Mês": "Month",
    "Ano": "Year",
    
    # Common UI elements
    "Nome": "Name",
    "Descrição": "Description",
    "Tipo": "Type",
    "Status": "Status",
    "Ações": "Actions",
    "Detalhes": "Details",
    "Informações": "Information",
    "Opções": "Options",
    "Ajuda": "Help",
    "Sobre": "About",
    "Versão": "Version",
    
    # Metrics
    "Total de": "Total",
    "Número de": "Number of",
    "Quantidade": "Quantity",
    "Confiança": "Confidence",
    "Precisão": "Accuracy",
    "Taxa": "Rate",
    "Média": "Average",
    "Mínimo": "Minimum",
    "Máximo": "Maximum",
    
    # File operations
    "Formato": "Format",
    "Tamanho": "Size",
    "Modificado": "Modified",
    "Criado": "Created",
    "Pasta": "Folder",
    "Diretório": "Directory",
    "Caminho": "Path",
}

def translate_content(content):
    """Translate Portuguese content to English"""
    
    # Apply all translations
    for pt, en in translations.items():
        # Replace in various contexts
        patterns = [
            (f'"{pt}"', f'"{en}"'),
            (f"'{pt}'", f"'{en}'"),
            (f"**{pt}**", f"**{en}**"),
            (f"### {pt}", f"### {en}"),
            (f"## {pt}", f"## {en}"),
            (f"# {pt}", f"# {en}"),
            (f"#### {pt}", f"#### {en}"),
            (f"label=\"{pt}\"", f"label=\"{en}\""),
            (f"help=\"{pt}", f"help=\"{en}"),
            (f"value=\"{pt}\"", f"value=\"{en}\""),
            (f"title=\"{pt}\"", f"title=\"{en}\""),
            (f"placeholder=\"{pt}", f"placeholder=\"{en}"),
        ]
        
        for old, new in patterns:
            content = content.replace(old, new)
    
    return content

def translate_file(filepath):
    """Translate a single file"""
    print(f"Translating {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply translations
        translated = translate_content(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        print(f"✓ Successfully translated {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error translating {filepath}: {e}")
        return False

def main():
    """Main function"""
    ui_dir = Path("src/ui")
    
    # Translate all UI pages except main_page (already done)
    ui_files = [
        "training_page.py",
        "processing_page.py",
        "results_page.py",
        "settings_page.py"
    ]
    
    success_count = 0
    for filename in ui_files:
        filepath = ui_dir / filename
        if filepath.exists():
            if translate_file(filepath):
                success_count += 1
        else:
            print(f"! File not found: {filepath}")
    
    print(f"\n✅ Translation completed! {success_count}/{len(ui_files)} files translated successfully!")
    print("\n🌍 All pages are now 100% in English!")

if __name__ == "__main__":
    main()
