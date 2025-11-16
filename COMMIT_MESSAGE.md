feat: Configurar backend VacaFácil com SQLite e integração frontend

- Configurar banco de dados SQLite para desenvolvimento
- Corrigir relacionamentos entre modelos (User, Subscription, etc)
- Substituir passlib por bcrypt direto para compatibilidade
- Configurar CORS para aceitar todas as origens em desenvolvimento
- Importar todos os modelos no main.py para criação automática de tabelas
- Adicionar logs detalhados no endpoint de registro para debug
- Criar arquivo iniciar.bat para facilitar inicialização do servidor
- Testar todos os 27 endpoints da API com sucesso

Endpoints funcionando:
✅ Autenticação (register, login)
✅ Usuários (CRUD completo)
✅ Vacas (CRUD completo)
✅ Produção (registro e listagem)
✅ Reprodução (registro e listagem)
✅ Financeiro (receitas e despesas)
✅ Marketplace (anúncios)
✅ Assinaturas (planos e status)
✅ Machine Learning (insights e predições)

Fixes: #issue_number
