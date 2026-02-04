# 🌐 Interface Web - Sistema de Extração de IBAN

## 🎯 Visão Geral

Interface gráfica web moderna e intuitiva para o **Sistema de Extração de IBAN com IA**, desenvolvida com Streamlit para facilitar a interação do usuário com todas as funcionalidades do sistema.

---

## ✨ Características

- 🎨 **Design Moderno**: Interface limpa e profissional
- 📤 **Upload Drag & Drop**: Arraste e solte arquivos facilmente
- 📊 **Visualização em Tempo Real**: Acompanhe o processamento ao vivo
- 📈 **Gráficos Interativos**: Estatísticas e métricas visuais
- 🔄 **Feedback Instantâneo**: Mensagens claras de sucesso/erro
- ⚙️ **Configuração Visual**: Ajuste parâmetros sem editar código
- 📥 **Download Direto**: Baixe resultados com um clique

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

Edite o arquivo `.env`:

```ini
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Iniciar Interface

**Windows:**
```bash
run_app.bat
```

**Linux/Mac:**
```bash
chmod +x run_app.sh
./run_app.sh
```

**Manual:**
```bash
streamlit run app.py
```

### 4. Acessar

Abra no navegador: http://localhost:8501

---

## 📱 Páginas Disponíveis

### 🏠 Início
- Dashboard geral do sistema
- Status de configuração
- Estatísticas rápidas
- Guia de uso

### 🎓 Treinamento
- Upload de faturas de exemplo
- Configuração de parâmetros
- Acompanhamento de progresso
- Resultados do treinamento

### ⚙️ Processamento
- Upload de faturas para processar
- Configuração de opções
- Processamento em lote
- Download de resultados (CSV)

### 📊 Resultados
- Visualização de extrações
- Estatísticas detalhadas
- Gráficos de distribuição
- Filtros e busca
- Exportação de dados

### ⚙️ Configurações
- Configuração de API Anthropic
- Gestão de banco de dados
- Ajuste de performance
- Segurança e GDPR

---

## 🎓 Como Usar

### Primeiro Uso

1. **Configure o Sistema**
   - Vá para Configurações
   - Adicione sua API Key da Anthropic
   - Configure o banco de dados

2. **Treine o Modelo**
   - Vá para Treinamento
   - Faça upload de ~100 faturas variadas
   - Clique em "Iniciar Treinamento"
   - Aguarde 5-10 minutos

3. **Processe Faturas**
   - Vá para Processamento
   - Faça upload das faturas reais
   - Clique em "Processar Faturas"
   - Baixe o CSV gerado

4. **Analise Resultados**
   - Vá para Resultados
   - Visualize estatísticas
   - Revise extrações de baixa confiança
   - Exporte dados filtrados

### Uso Regular

```
Upload → Processar → Baixar CSV → Importar no Dynamics GP
```

---

## 📋 Estrutura de Arquivos

```
iban-extraction-system/
├── app.py                      # Aplicação principal Streamlit
├── run_app.bat                 # Script Windows
├── run_app.sh                  # Script Linux/Mac
├── src/
│   └── ui/                     # Módulos da interface
│       ├── __init__.py
│       ├── main_page.py        # Página inicial
│       ├── training_page.py    # Página de treinamento
│       ├── processing_page.py  # Página de processamento
│       ├── results_page.py     # Página de resultados
│       └── settings_page.py    # Página de configurações
└── docs/
    └── WEB_INTERFACE_GUIDE.md  # Guia detalhado
```

---

## 🎨 Capturas de Tela

### Dashboard Principal
- Visão geral com métricas
- Status do sistema
- Guia rápido integrado

### Treinamento
- Upload múltiplo de arquivos
- Barra de progresso em tempo real
- Resultados com estatísticas

### Processamento
- Interface intuitiva de upload
- Configurações ajustáveis
- Download direto de CSV

### Resultados
- Tabelas interativas
- Gráficos de distribuição
- Filtros avançados

---

## ⚙️ Configurações Recomendadas

### Para Desenvolvimento
```ini
ENV=development
DB_TYPE=sqlite
MAX_WORKERS=4
BATCH_SIZE=50
```

### Para Produção
```ini
ENV=production
DB_TYPE=postgresql
MAX_WORKERS=8
BATCH_SIZE=100
```

---

## 🔧 Resolução de Problemas

### Interface não abre

```bash
# Verifique se o Streamlit está instalado
pip show streamlit

# Reinstale se necessário
pip install streamlit==1.31.0
```

### Erro ao fazer upload

- Verifique o formato do arquivo (PDF, JPG, PNG, TIFF)
- Confirme que o arquivo não está corrompido
- Reduza o tamanho se for muito grande (>200MB)

### Processamento lento

- Aumente workers em Configurações > Processamento
- Use modelo Haiku para velocidade
- Reduza batch size

---

## 📚 Documentação Completa

- **Guia Detalhado**: `docs/WEB_INTERFACE_GUIDE.md`
- **README Principal**: `README.md`
- **Início Rápido**: `docs/QUICKSTART.md`

---

## 🎯 Recursos Principais

| Recurso | Descrição | Status |
|---------|-----------|--------|
| Upload de Arquivos | Drag & Drop múltiplos arquivos | ✅ |
| Treinamento | Treinar modelo com faturas | ✅ |
| Processamento | Extrair IBANs em lote | ✅ |
| Visualização | Gráficos e estatísticas | ✅ |
| Exportação | Download CSV/relatórios | ✅ |
| Configurações | Gerenciar via interface | ✅ |
| Logs | Visualizar logs do sistema | ✅ |

---

## 💡 Dicas de Uso

1. **Qualidade das Imagens**
   - Use PDFs originais quando possível
   - Evite scans de baixa qualidade
   - Prefira 300 DPI ou superior

2. **Treinamento**
   - Use faturas de diferentes fornecedores
   - Inclua layouts variados
   - Mínimo 50, recomendado 100 faturas

3. **Performance**
   - Ajuste workers conforme sua CPU
   - Use lotes de 50-100 arquivos
   - Monitore uso de memória

4. **Segurança**
   - Nunca compartilhe sua API key
   - Use HTTPS em produção
   - Habilite criptografia no banco

---

## 🆘 Suporte

### Contatos

- **Eduardo Nascimento** - Solutions Architect
- **Email**: eduardo.nascimento@charteredaccountants.ie
- **GitHub**: Issues no repositório

### Links Úteis

- [Documentação Streamlit](https://docs.streamlit.io/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Chartered Accountants Ireland](https://www.charteredaccountants.ie/)

---

## 📝 Licença

Copyright © 2025 Chartered Accountants Ireland  
All rights reserved.

---

## 🎉 Agradecimentos

Desenvolvido com ❤️ pela equipe de TI da Chartered Accountants Ireland.

**Versão**: 1.0.0  
**Data**: Fevereiro 2025  
**Tecnologias**: Python 3.10+, Streamlit 1.31.0, Anthropic Claude API

---

**🚀 Pronto para começar? Execute `run_app.bat` (Windows) ou `./run_app.sh` (Linux/Mac)!**
