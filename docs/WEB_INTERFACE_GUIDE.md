# Guia da Interface Web - Sistema de Extração de IBAN

## 📖 Índice

- [Visão Geral](#visão-geral)
- [Instalação e Configuração](#instalação-e-configuração)
- [Iniciando a Interface](#iniciando-a-interface)
- [Páginas e Funcionalidades](#páginas-e-funcionalidades)
- [Fluxo de Trabalho Recomendado](#fluxo-de-trabalho-recomendado)
- [Perguntas Frequentes](#perguntas-frequentes)
- [Resolução de Problemas](#resolução-de-problemas)

---

## 🎯 Visão Geral

A interface web do Sistema de Extração de IBAN foi desenvolvida com **Streamlit** para oferecer uma experiência intuitiva e user-friendly. 

### Características Principais:

- ✅ **Interface Moderna**: Design limpo e intuitivo
- ✅ **Drag & Drop**: Upload fácil de faturas
- ✅ **Visualização em Tempo Real**: Acompanhe o processamento
- ✅ **Estatísticas Detalhadas**: Gráficos e métricas
- ✅ **Download Direto**: Baixe resultados com um clique
- ✅ **Configuração Visual**: Ajuste parâmetros sem editar código

---

## 🚀 Instalação e Configuração

### Pré-requisitos

1. **Python 3.10+** instalado
2. **Ambiente virtual** configurado
3. **Dependências** instaladas

### Passo 1: Instalar Dependências

Se ainda não instalou o Streamlit:

```bash
pip install -r requirements.txt
```

### Passo 2: Configurar Variáveis de Ambiente

Copie e configure o arquivo `.env`:

```bash
copy .env.example .env  # Windows
# ou
cp .env.example .env    # Linux/Mac
```

Edite o arquivo `.env` e configure:

```ini
# API Anthropic (Obrigatório)
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Banco de Dados (SQLite para desenvolvimento)
DB_TYPE=sqlite

# Aplicação
ENV=development
LOG_LEVEL=INFO
```

---

## 🎮 Iniciando a Interface

### Windows

Execute o script de inicialização:

```bash
run_app.bat
```

### Linux/Mac

```bash
chmod +x run_app.sh
./run_app.sh
```

### Manualmente

```bash
# Ative o ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Inicie o Streamlit
streamlit run app.py
```

### Acesso

A interface será aberta automaticamente em seu navegador:

```
http://localhost:8501
```

---

## 📱 Páginas e Funcionalidades

### 1. 🏠 Página Inicial (Home)

**Objetivo:** Dashboard geral do sistema

**Funcionalidades:**
- Visão geral do sistema
- Status de configuração (API, Banco de Dados)
- Estatísticas rápidas
- Guia de início rápido
- Últimas atividades

**Como usar:**
1. Verifique o status do sistema na barra lateral
2. Leia o guia rápido para entender o fluxo
3. Navegue para outras páginas conforme necessário

---

### 2. 🎓 Treinamento

**Objetivo:** Treinar o modelo de IA com faturas de exemplo

**Funcionalidades:**
- Upload de múltiplas faturas (100 recomendado)
- Configuração de limite de confiança
- Processamento paralelo ajustável
- Acompanhamento de progresso em tempo real
- Estatísticas de treinamento

**Como usar:**

1. **Upload de Faturas:**
   - Clique em "Browse files" ou arraste arquivos
   - Formatos aceitos: PDF, JPG, JPEG, PNG, TIFF
   - Recomendado: 100 faturas de diferentes fornecedores

2. **Configurar Parâmetros:**
   - **Limite de Confiança**: 90% (padrão)
   - **Processamento Paralelo**: Ativado
   - **Máx. Trabalhadores**: 4 (ajuste conforme CPU)

3. **Iniciar Treinamento:**
   - Clique em "▶️ Iniciar Treinamento"
   - Aguarde o processamento (5-10 minutos)
   - Visualize resultados e métricas

**Dicas:**
- Use faturas de layouts variados
- Inclua diferentes fornecedores
- Prefira imagens de alta qualidade
- Evite duplicatas

---

### 3. ⚙️ Processamento

**Objetivo:** Processar faturas reais e extrair IBANs

**Funcionalidades:**
- Upload de faturas de produção
- Configuração de limite de confiança
- Geração de relatório de validação
- Exportação para CSV
- Download direto dos resultados
- Histórico de processamentos

**Como usar:**

1. **Upload de Faturas:**
   - Selecione as faturas para processar
   - Visualize lista de arquivos selecionados
   - Verifique informações do lote

2. **Configurar Opções:**
   - **Limite de Confiança**: 90%
   - **Gerar Relatório**: ✅ Ativado
   - **Exportar CSV**: ✅ Ativado

3. **Processar:**
   - Clique em "▶️ Processar Faturas"
   - Acompanhe progresso
   - Baixe os arquivos gerados

**Arquivos Gerados:**
- `iban_extractions_YYYYMMDD_HHMMSS.csv` - Dados extraídos
- `validation_report_YYYYMMDD_HHMMSS.csv` - Relatório de validação

---

### 4. 📊 Resultados

**Objetivo:** Analisar e visualizar resultados

**Funcionalidades:**
- Seleção de arquivos de resultados
- Estatísticas gerais (taxa de sucesso, confiança média)
- Distribuição de confiança (gráfico)
- Filtros avançados (por confiança, busca)
- Exportação de dados filtrados
- Alertas de baixa confiança
- Visualização de logs

**Como usar:**

1. **Selecionar Arquivo:**
   - Escolha um arquivo de resultados
   - Visualize informações básicas

2. **Analisar Estatísticas:**
   - Veja métricas gerais
   - Analise distribuição de confiança
   - Identifique problemas

3. **Filtrar Dados:**
   - Use filtros por confiança
   - Busque por IBAN ou vendor_id
   - Ajuste quantidade de linhas exibidas

4. **Exportar:**
   - Baixe dados filtrados
   - Exporte para revisão manual

**Alertas:**
- ⚠️ Extrações com confiança < 70% requerem revisão manual

---

### 5. ⚙️ Configurações

**Objetivo:** Gerenciar configurações do sistema

**Funcionalidades:**

#### 🔑 API
- Configurar chave Anthropic
- Selecionar modelo de IA
- Testar conexão

#### 🗄️ Banco de Dados
- Escolher tipo (SQLite/PostgreSQL)
- Configurar conexão
- Inicializar/limpar database

#### ⚡ Processamento
- Ajustar workers e batch size
- Configurar limites de confiança
- Definir diretórios

#### 🔒 Segurança
- Habilitar criptografia
- Configurar logs e auditoria
- Gerenciar alertas
- Verificar conformidade GDPR

**Como usar:**
1. Navegue pelas abas
2. Ajuste configurações desejadas
3. Clique em "💾 Salvar Todas"

---

## 🔄 Fluxo de Trabalho Recomendado

### Para Primeiro Uso:

```
1. 🏠 Início
   └─> Verificar configuração do sistema
   
2. ⚙️ Configurações
   └─> Configurar API Anthropic
   └─> Configurar banco de dados
   
3. 🎓 Treinamento
   └─> Upload 100 faturas de exemplo
   └─> Iniciar treinamento
   └─> Aguardar conclusão
   
4. ⚙️ Processamento
   └─> Upload faturas reais
   └─> Processar
   └─> Baixar resultados
   
5. 📊 Resultados
   └─> Analisar extrações
   └─> Revisar baixa confiança
   └─> Exportar dados finais
```

### Para Uso Regular:

```
1. ⚙️ Processamento
   └─> Upload novas faturas
   └─> Processar
   
2. 📊 Resultados
   └─> Verificar extrações
   └─> Exportar CSV
   
3. 💾 Dynamics GP
   └─> Importar CSV
```

---

## ❓ Perguntas Frequentes

### 1. A interface não abre no navegador

**Solução:**
- Abra manualmente: `http://localhost:8501`
- Verifique se porta 8501 está disponível
- Tente outra porta: `streamlit run app.py --server.port 8502`

### 2. Erro ao fazer upload de arquivos

**Causas comuns:**
- Arquivo muito grande (limite: 200MB)
- Formato não suportado
- Arquivo corrompido

**Solução:**
- Verifique o formato (PDF, JPG, PNG, TIFF)
- Reduza o tamanho do arquivo
- Teste com outro arquivo

### 3. Processamento muito lento

**Otimizações:**
- Aumente o número de workers (Configurações > Processamento)
- Use modelo mais rápido (Haiku em vez de Sonnet)
- Reduza batch size
- Verifique conexão com a API

### 4. Extrações com baixa confiança

**Causas:**
- Qualidade ruim da imagem
- Layout de fatura não comum
- Falta de treinamento adequado

**Solução:**
- Aumente qualidade das imagens
- Treine com mais faturas variadas
- Revise manualmente os casos

### 5. Como atualizar a API key?

1. Vá para **Configurações > API**
2. Digite a nova chave
3. Clique em "💾 Salvar API Key"
4. Reinicie a aplicação

---

## 🔧 Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### Erro: "ANTHROPIC_API_KEY not configured"

1. Verifique arquivo `.env`
2. Configure a chave:
   ```ini
   ANTHROPIC_API_KEY=sk-ant-your-key
   ```
3. Reinicie a aplicação

### Interface fica em branco

1. Limpe o cache do navegador
2. Pressione Ctrl+F5 para recarregar
3. Tente outro navegador

### Erro de conexão com banco de dados

**SQLite:**
- Verifique permissões do diretório `data/`
- Crie diretório se não existir

**PostgreSQL:**
- Verifique credenciais em Configurações
- Teste conexão
- Verifique se PostgreSQL está rodando

---

## 📞 Suporte

### Documentação Adicional

- **README.md**: Documentação completa do sistema
- **QUICKSTART.md**: Guia rápido de instalação
- **API Documentation**: Detalhes técnicos

### Contato

- **Email**: eduardo.nascimento@charteredaccountants.ie
- **Issues**: GitHub Issues
- **Equipe**: Ver README.md para contatos

---

## 🎉 Recursos Avançados

### Atalhos de Teclado

- **Ctrl + R**: Recarregar página
- **Ctrl + Shift + R**: Limpar cache e recarregar
- **Ctrl + S**: Salvar configurações (onde aplicável)

### Dicas de Performance

1. **Processamento em Lote:**
   - Use lotes de 50-100 faturas
   - Evite lotes muito grandes (>200)

2. **Qualidade vs Velocidade:**
   - Sonnet: Melhor balanço ⭐
   - Opus: Máxima precisão, mais lento
   - Haiku: Mais rápido, menor precisão

3. **Uso de CPU:**
   - Workers = Número de núcleos - 1
   - Máximo recomendado: 8 workers

---

**Desenvolvido com ❤️ por Chartered Accountants Ireland IT Team**

*Versão 1.0.0 | © 2025*
