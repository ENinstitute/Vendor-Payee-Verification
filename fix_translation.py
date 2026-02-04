"""
Comprehensive translation fix - Replaces ALL Portuguese text
"""

import re
from pathlib import Path

def translate_training_page():
    """Translate training_page.py completely"""
    
    pt_to_en = {
        # Headers and titles
        "Treinamento do Modelo": "Model Training",
        "Treinar o Modelo de IA": "Train the AI Model",
        "O treinamento ensina o sistema a reconhecer padrões em faturas e extrair informações de IBAN": "Training teaches the system to recognize patterns in invoices and extract IBAN information",
        "com alta precisão": "with high accuracy",
        "Use aproximadamente": "Use approximately",
        "faturas de exemplo": "sample invoices",
        "para melhores resultados": "for best results",
        
        # File upload section
        "Upload de Faturas de Treinamento": "Training Invoice Upload",
        "Selecione as faturas para treinamento (PDF ou imagens)": "Select invoices for training (PDF or images)",
        "Recomendado": "Recommended",
        "faturas diversas de diferentes fornecedores": "diverse invoices from different vendors",
        "arquivo(s) selecionado(s)": "file(s) selected",
        "Ver lista de arquivos": "View file list",
        
        # Configuration section
        "Configurações": "Settings",
        "Limite de Confiança (%)": "Confidence Threshold (%)",
        "Extractions abaixo deste valor serão marcadas para revisão manual": "Extractions below this value will be marked for manual review",
        "Processamento Paralelo": "Parallel Processing",
        "Processa múltiplas faturas simultaneamente": "Process multiple invoices simultaneously",
        "Máx. Trabalhadores": "Max Workers",
        "Number of processos paralelos": "Number of parallel processes",
        
        # Start training section
        "Iniciar Treinamento": "Start Training",
        "Informação": "Information",
        "Tempo estimado": "Estimated time",
        "minutos para": "minutes for",
        "faturas": "invoices",
        "O processo pode ser interrompido a qualquer momento": "The process can be interrupted at any time",
        "Resultados são salvos automaticamente no banco de dados": "Results are automatically saved to the database",
        "Padrões aprendidos melhoram a precisão do processamento": "Learned patterns improve processing accuracy",
        "Por favor, faça upload de arquivos primeiro": "Please upload files first",
        
        # Statistics section
        "Estatísticas Esperadas": "Expected Statistics",
        "Meta de Sucesso": "Success Target",
        "Rate de sucesso esperada": "Expected success rate",
        "Nível médio de confiança": "Average confidence level",
        "Tempo médio por fatura": "Average time per invoice",
        "Dicas": "Tips",
        "Use faturas de": "Use invoices from",
        "diferentes fornecedores": "different vendors",
        "Inclua": "Include",
        "layouts variados": "varied layouts",
        "Prefira": "Prefer",
        "alta qualidade": "high quality",
        "de imagem": "image",
        "Evite": "Avoid",
        "duplicatas": "duplicates",
        
        # Training history
        "Histórico de Treinamento": "Training History",
        "arquivo(s) no diretório de treinamento": "file(s) in training directory",
        "Limpar Diretório de Treinamento": "Clear Training Directory",
        "Funcionalidade de limpeza será implementada": "Cleanup functionality will be implemented",
        "Clique novamente para confirmar a exclusão": "Click again to confirm deletion",
        "Nenhum arquivo no diretório de treinamento": "No files in training directory",
        "Diretório de treinamento não encontrado": "Training directory not found",
        
        # Processing section
        "Processamento em Andamento": "Processing in Progress",
        "Salvando arquivos": "Saving files",
        "arquivo(s) salvo(s) com sucesso": "file(s) saved successfully",
        "Inicializando banco de dados": "Initializing database",
        "Banco de dados inicializado": "Database initialized",
        "Erro ao inicializar banco de dados": "Error initializing database",
        "Preparando processador": "Preparing processor",
        "Processador inicializado": "Processor initialized",
        "Erro ao inicializar processador": "Error initializing processor",
        "Processando faturas com IA": "Processing invoices with AI",
        "Processando com Claude API": "Processing with Claude API",
        "Treinamento Concluído": "Training Completed",
        
        # Results
        "Total Processado": "Total Processed",
        "Total faturas processadas": "Total invoices processed",
        "Percentual de extrações bem-sucedidas": "Percentage of successful extractions",
        "Falhados": "Failed",
        "Faturas que falharam no processamento": "Invoices that failed processing",
        "Erro durante o treinamento": "Error during training",
        "Erro ao salvar arquivos": "Error saving files",
        
        # Success messages
        "Excelente": "Excellent",
        "O modelo foi treinado com sucesso e está pronto para uso": "The model was successfully trained and is ready to use",
        "Atenção": "Attention",
        "Taxa de sucesso abaixo do esperado": "Success rate below expected",
        "Considere adicionar mais faturas de treinamento": "Consider adding more training invoices",
        "Problema": "Problem",
        "Taxa de sucesso muito baixa": "Success rate too low",
        "Verifique as faturas e tente novamente": "Check the invoices and try again",
        
        # Next steps
        "Próximos Passos": "Next Steps",
        "Modelo treinado com sucesso": "Model successfully trained",
        "Vá para": "Go to",
        "para processar faturas reais": "to process real invoices",
        "Verifique os": "Check the",
        "após o processamento": "after processing",
    }
    
    filepath = Path("src/ui/training_page.py")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pt, en in pt_to_en.items():
        content = content.replace(pt, en)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ training_page.py translated")

def main():
    """Main function"""
    translate_training_page()
    print("\n✅ Translation fix applied!")
    print("Now run: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
