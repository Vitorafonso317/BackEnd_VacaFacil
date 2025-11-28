# 📊 Relatórios - Endpoints

**Autenticação:** Requer token JWT

## GET /relatorios/producao/json
**Descrição:** Relatório completo de produção

**Query Params:**
- `data_inicio`: Data inicial (YYYY-MM-DD)
- `data_fim`: Data final (YYYY-MM-DD)

**Response 200:**
```json
{
  "periodo": {
    "inicio": "2024-01-01",
    "fim": "2024-01-31"
  },
  "resumo": {
    "total_producao": 750.50,
    "media_diaria": 25.02,
    "total_registros": 30
  },
  "por_vaca": {
    "1": {
      "vaca_nome": "Mimosa",
      "total": 400.00,
      "registros": 15
    }
  },
  "registros": [...]
}
```

---

## GET /relatorios/financeiro/json
**Descrição:** Relatório completo financeiro

**Query Params:**
- `data_inicio`: Data inicial
- `data_fim`: Data final

**Response 200:**
```json
{
  "periodo": {
    "inicio": "2024-01-01",
    "fim": "2024-01-31"
  },
  "resumo": {
    "total_receitas": 5000.00,
    "total_despesas": 2000.00,
    "saldo": 3000.00,
    "margem": 60.00
  },
  "receitas_por_categoria": {
    "venda_leite": 5000.00
  },
  "despesas_por_categoria": {
    "racao": 1500.00,
    "veterinario": 500.00
  },
  "receitas": [...],
  "despesas": [...]
}
```

---

## GET /relatorios/completo/json
**Descrição:** Relatório completo da fazenda (últimos 30 dias)

**Response 200:**
```json
{
  "periodo": "Últimos 30 dias",
  "rebanho": {
    "total_vacas": 10,
    "vacas_ativas": 8
  },
  "producao": {
    "total": 750.50,
    "media_diaria": 25.02,
    "registros": 30
  },
  "financeiro": {
    "receitas": 5000.00,
    "despesas": 2000.00,
    "saldo": 3000.00
  }
}
```
