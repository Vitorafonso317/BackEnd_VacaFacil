# 🔧 Solução: ModuleNotFoundError: No module named 'app'

## ❌ Erro
```
ModuleNotFoundError: No module named 'app'
```

## ✅ Soluções

### 1. Verificar Diretório Atual
O comando deve ser executado do diretório raiz do projeto:

```bash
# Verificar onde você está
cd

# Deve estar em:
# c:\Users\vitor\OneDrive\Documentos\github\BackEnd_VacaFacil\BackEnd_VacaFacil
```

### 2. Usar o Script Correto

#### Windows:
```bash
# Execute o script de verificação primeiro
verificar.bat

# Depois inicie o servidor
iniciar.bat
```

#### Ou manualmente:
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### 3. Verificar Estrutura

A estrutura deve estar assim:
```
BackEnd_VacaFacil/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── utils/
├── venv/
├── .env
├── requirements.txt
├── iniciar.bat
└── verificar.bat
```

### 4. Reinstalar Dependências (se necessário)

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Reinstalar
pip install -r requirements.txt
```

### 5. Criar Ambiente Virtual (se não existir)

```bash
# Criar venv
python -m venv venv

# Ativar
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## 🚀 Inicialização Correta

### Passo a Passo:

1. **Abrir terminal no diretório correto:**
   ```bash
   cd c:\Users\vitor\OneDrive\Documentos\github\BackEnd_VacaFacil\BackEnd_VacaFacil
   ```

2. **Verificar sistema:**
   ```bash
   verificar.bat
   ```

3. **Iniciar servidor:**
   ```bash
   iniciar.bat
   ```

4. **Acessar:**
   - API: http://localhost:5000
   - Docs: http://localhost:5000/docs
   - Health: http://localhost:5000/health

## 🔍 Verificações Rápidas

### Verificar se está no diretório correto:
```bash
dir app\main.py
```
Se aparecer "Arquivo não encontrado", você está no diretório errado!

### Verificar Python:
```bash
python --version
```
Deve mostrar Python 3.8+

### Verificar uvicorn:
```bash
python -c "import uvicorn; print(uvicorn.__version__)"
```

## 📝 Comandos Úteis

```bash
# Ver estrutura
tree /F app

# Testar importação
python -c "from app.main import app; print('OK')"

# Iniciar em modo debug
uvicorn app.main:app --reload --log-level debug

# Iniciar em porta diferente
uvicorn app.main:app --port 8000 --reload
```

## 🆘 Ainda com Problemas?

1. **Deletar venv e recriar:**
   ```bash
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Verificar PYTHONPATH:**
   ```bash
   echo %PYTHONPATH%
   ```

3. **Executar direto do Python:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## ✅ Teste Final

Após iniciar, teste:
```bash
curl http://localhost:5000/health
```

Deve retornar:
```json
{"status": "healthy"}
```

---

**Problema resolvido!** 🎉
