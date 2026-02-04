# 🧪 Guia de Teste - Interface Web

## 📋 Pré-requisitos

Antes de testar, certifique-se de que tem:

- ✅ Python 3.10+ instalado
- ✅ Ambiente virtual criado
- ✅ Dependências instaladas
- ✅ Arquivo `.env` configurado

---

## 🚀 Passo a Passo para Testar

### 1. Preparar o Ambiente

```bash
# Navegue até o diretório do projeto
cd C:\Users\nascimentoe\Desktop\iban-extraction-system

# Crie o ambiente virtual (se ainda não existir)
python -m venv venv

# Ative o ambiente virtual
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configurar o Arquivo .env

```bash
# Copie o arquivo de exemplo (se ainda não fez)
copy .env.example .env

# Edite o .env com suas configurações
notepad .env
```

**Configuração mínima necessária:**
```ini
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
DB_TYPE=sqlite
ENV=development
LOG_LEVEL=INFO
```

### 3. Iniciar a Aplicação

**Opção 1: Usando o Script (Recomendado)**
```bash
# Windows PowerShell
.\run_app.bat

# Ou no CMD
run_app.bat
```

**Opção 2: Diretamente com Streamlit**
```bash
streamlit run app.py
```

**Opção 3: Especificando Porta**
```bash
streamlit run app.py --server.port 8501 --server.address localhost
```

### 4. Acessar a Interface

A aplicação abrirá automaticamente no seu navegador padrão.

**Se não abrir automaticamente:**
- Abra manualmente: http://localhost:8501

---

## ✅ Lista de Testes

### Teste 1: Página Inicial

1. ✅ Verificar se a página carrega
2. ✅ Visualizar métricas do sistema
3. ✅ Confirmar status da API e BD na barra lateral
4. ✅ Ler o guia rápido
5. ✅ Verificar links de navegação

**Resultado Esperado:** Dashboard completo com informações do sistema

---

### Teste 2: Página de Configurações

1. ✅ Navegar para **⚙️ Configurações**
2. ✅ Verificar aba **🔑 API**
   - Ver status da API
   - Campo para API key (não precisa inserir se já configurou no .env)
3. ✅ Verificar aba **🗄️ Banco de Dados**
   - Tipo de banco (SQLite ou PostgreSQL)
   - Botão "Inicializar DB" - clicar para testar
4. ✅ Verificar aba **⚡ Processamento**
   - Ajustar sliders
   - Ver configurações de diretórios
5. ✅ Verificar aba **🔒 Segurança**
   - Opções de criptografia
   - Configurações de logs

**Resultado Esperado:** Todas as abas funcionam e exibem configurações

---

### Teste 3: Página de Treinamento (Simulação)

**Nota:** Para teste completo, você precisaria de faturas reais. Vamos simular.

1. ✅ Navegar para **🎓 Treinamento**
2. ✅ Visualizar área de upload
3. ✅ Configurar parâmetros:
   - Limite de confiança: 90%
   - Processamento paralelo: ✅
   - Máx. trabalhadores: 4
4. ✅ Ver seção "Estatísticas Esperadas"
5. ✅ Ver "Histórico de Treinamento"

**Para teste com arquivos:**
- Clique em "Browse files"
- Selecione 2-3 PDFs de teste (qualquer PDF)
- Veja a lista de arquivos
- **NÃO clique em "Iniciar Treinamento" sem API configurada**

**Resultado Esperado:** Interface responsiva, uploads funcionam

---

### Teste 4: Página de Processamento

1. ✅ Navegar para **⚙️ Processamento**
2. ✅ Ver aviso se não houver treinamento
3. ✅ Área de upload de faturas
4. ✅ Configurações:
   - Limite de confiança
   - Gerar relatório: ✅
   - Exportar CSV: ✅
5. ✅ Ver "Histórico Recente" (vazio se não processou ainda)

**Resultado Esperado:** Interface pronta para processar faturas

---

### Teste 5: Página de Resultados

1. ✅ Navegar para **📊 Resultados**
2. ✅ Verificar mensagem se não houver resultados
3. ✅ Ver opções de filtros (desabilitadas se sem dados)

**Se houver arquivos CSV de teste em `data/output/`:**
- Seletor de arquivo funciona
- Estatísticas são exibidas
- Gráficos são renderizados
- Filtros funcionam
- Download funciona

**Resultado Esperado:** Página exibe mensagem adequada (sem dados ou com dados)

---

### Teste 6: Navegação e Responsividade

1. ✅ Clicar em cada item do menu lateral
2. ✅ Verificar transição entre páginas
3. ✅ Testar em diferentes tamanhos de janela
4. ✅ Verificar se métricas da barra lateral atualizam

**Resultado Esperado:** Navegação suave, layout responsivo

---

## 🎯 Teste Completo (End-to-End)

**Apenas se você tiver API Anthropic configurada e faturas de teste:**

### Passo 1: Configurar
1. Vá para Configurações
2. Verifique API status: ✅ Conectado
3. Inicialize o banco de dados

### Passo 2: Treinar (Opcional)
1. Vá para Treinamento
2. Upload de 5-10 PDFs de teste
3. Clique "Iniciar Treinamento"
4. Aguarde conclusão
5. Verifique estatísticas

### Passo 3: Processar
1. Vá para Processamento
2. Upload de 2-3 PDFs
3. Configure opções
4. Clique "Processar Faturas"
5. Aguarde conclusão
6. Baixe o CSV gerado

### Passo 4: Analisar
1. Vá para Resultados
2. Selecione o arquivo processado
3. Visualize estatísticas
4. Use filtros
5. Exporte dados

---

## 🐛 Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
pip install streamlit==1.31.0
```

### Erro: "Port 8501 is already in use"

**Solução:**
```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

### Interface não carrega / Página em branco

**Solução:**
```bash
# Limpar cache do Streamlit
streamlit cache clear

# Ou pressione Ctrl+F5 no navegador
```

### Erro: "ANTHROPIC_API_KEY not configured"

**Solução:**
1. Verifique o arquivo `.env`
2. Certifique-se de que a chave está correta
3. Reinicie a aplicação

### Erro ao fazer upload

**Solução:**
- Verifique o formato (PDF, JPG, PNG, TIFF)
- Reduza o tamanho do arquivo
- Teste com arquivo diferente

---

## 📊 Checklist de Teste Rápido

```
☐ Ambiente virtual ativado
☐ Dependências instaladas
☐ Arquivo .env configurado
☐ Aplicação inicia sem erros
☐ Página inicial carrega
☐ Navegação funciona
☐ Todas as 5 páginas carregam
☐ Upload de arquivos funciona
☐ Configurações são exibidas
☐ Sem erros no console
```

---

## 🎬 Comandos Úteis

```bash
# Verificar instalação do Streamlit
pip show streamlit

# Ver versão do Python
python --version

# Listar dependências instaladas
pip list

# Verificar logs em tempo real (se houver)
type logs\iban_extraction_*.log

# Parar a aplicação
# Pressione Ctrl+C no terminal
```

---

## 📸 Teste Visual

### O que você deve ver:

1. **Barra Lateral Esquerda:**
   - Logo/Título do sistema
   - Menu de navegação (5 opções)
   - Status do sistema
   - Estatísticas rápidas
   - Footer com versão

2. **Área Principal:**
   - Cabeçalho colorido
   - Conteúdo da página selecionada
   - Botões e controles interativos
   - Mensagens de feedback

3. **Cores e Ícones:**
   - Azul: Informações
   - Verde: Sucesso
   - Amarelo: Avisos
   - Vermelho: Erros
   - Ícones emoji em todos os elementos

---

## 💡 Dicas de Teste

1. **Comece Simples:**
   - Teste primeiro sem API configurada
   - Navegue pelas páginas
   - Explore a interface

2. **Depois Avance:**
   - Configure API
   - Teste com arquivos pequenos
   - Experimente funcionalidades

3. **Use DevTools:**
   - Pressione F12 no navegador
   - Veja console para erros
   - Monitore network requests

4. **Terminal:**
   - Mantenha terminal visível
   - Veja logs em tempo real
   - Identifique erros rapidamente

---

## ✅ Teste Bem-Sucedido Quando:

- ✅ Todas as páginas carregam
- ✅ Navegação é fluida
- ✅ Uploads funcionam (aceita/rejeita arquivos corretamente)
- ✅ Configurações são exibidas
- ✅ Métricas e estatísticas aparecem
- ✅ Sem erros no terminal ou console
- ✅ Interface é responsiva
- ✅ Botões e controles respondem

---

## 📞 Precisa de Ajuda?

- **Documentação Completa**: `docs/WEB_INTERFACE_GUIDE.md`
- **README**: `WEB_INTERFACE_README.md`
- **Logs**: `logs/iban_extraction_*.log`

---

## 🎉 Próximos Passos

Após testar com sucesso:

1. ✅ Configure API Anthropic real
2. ✅ Prepare faturas de teste
3. ✅ Execute treinamento completo
4. ✅ Processe faturas reais
5. ✅ Analise resultados
6. ✅ Integre com Dynamics GP

**Boa sorte com os testes! 🚀**
