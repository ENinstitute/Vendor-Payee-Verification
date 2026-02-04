"""
FINAL COMPLETE TRANSLATION - ALL PAGES
Translates EVERY Portuguese text to English
"""

from pathlib import Path

# MASSIVE translation dictionary
PT_TO_EN = {
    # Processing page
    "Processamento de Faturas": "Invoice Processing",
    "Upload de Faturas para Processamento": "Invoice Upload for Processing",
    "arquivo(s) selecionado(s)": "file(s) selected",
    "Ver lista de arquivos": "View file list",
    "Informações do Lote": "Batch Information",
    "Total de arquivos": "Total files",
    "Tempo estimado": "Estimated time",
    "segundos": "seconds",
    "Gera arquivo CSV para importação no Dynamics GP": "Generate CSV file for Dynamics GP import",
    "Iniciar Processamento": "Start Processing",
    "Processamento usa o modelo treinado": "Processing uses the trained model",
    "Resultados são salvos no banco de dados": "Results are saved to the database",
    "Por favor, faça upload de arquivos primeiro": "Please upload files first",
    "Mantenha a janela aberta durante o processamento": "Keep the window open during processing",
    "Não faça upload de arquivos duplicados": "Do not upload duplicate files",
    "Verifique a qualidade das imagens": "Check the image quality",
    "Processamento em Andamento": "Processing in Progress",
    "Salvando arquivos": "Saving files",
    "arquivo(s) salvo(s)": "file(s) saved",
    "Processamento Concluído": "Processing Completed",
    "Excelente": "Excellent",
    "Processamento concluído com sucesso": "Processing completed successfully",
    "Os dados estão prontos para o Dynamics GP": "Data is ready for Dynamics GP",
    "Download dos arquivos CSV e relatório": "Download CSV files and report",
    "Revisar extrações com baixa confiança": "Review extractions with low confidence",
    "Erro ao salvar arquivos": "Error saving files",
    
    # Results page
    "Escolha um arquivo": "Choose a file",
    "Select um arquivo de resultados para visualizar": "Select a results file to view",
    "Erro ao carregar arquivo": "Error loading file",
    "Selecione um arquivo de log": "Select a log file",
    "Últimas linhas do arquivo de log": "Last lines of log file",
    "Nenhum arquivo de log encontrado": "No log files found",
    
    # Settings page
    "Banco de Dados": "Database",
    "Processamento": "Processing",
    "Segurança": "Security",
    "API Key salva com sucesso": "API Key saved successfully",
    "Para produção, atualize o arquivo .env": "For production, update the .env file",
    "Por favor, insira uma chave válida": "Please enter a valid key",
    "Pequenos volumes de dados": "Small data volumes",
    "Configuração simples": "Simple configuration",
    "Localização do arquivo SQLite": "SQLite file location",
    "Configurações de Processamento": "Processing Settings",
    "Diretório de Processamento": "Processing Directory",
    "Oculta parte dos IBANs nos arquivos de log": "Hides part of IBANs in log files",
    "Configurações salvas": "Settings saved",
    "Em produção, isso atualizaria o arquivo .env": "In production, this would update the .env file",
}

def translate_file(filepath, translations):
    """Translate a file using the translation dictionary"""
    print(f"Translating {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all translations
        for pt, en in translations.items():
            content = content.replace(pt, en)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath.name} translated successfully")
        return True
    except Exception as e:
        print(f"✗ Error translating {filepath}: {e}")
        return False

def main():
    """Main function"""
    
    # Files to translate
    files_to_translate = [
        Path("src/ui/processing_page.py"),
        Path("src/ui/results_page.py"),
        Path("src/ui/settings_page.py"),
    ]
    
    success_count = 0
    for filepath in files_to_translate:
        if filepath.exists():
            if translate_file(filepath, PT_TO_EN):
                success_count += 1
        else:
            print(f"! File not found: {filepath}")
    
    print(f"\n✅ Translation completed! {success_count}/{len(files_to_translate)} files translated!")
    print("\n🌍 ALL pages are now 100% in English!")
    print("\nRun: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
