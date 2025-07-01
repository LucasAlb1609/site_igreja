# Instruções Rápidas - Teste do Sistema

## 🚀 Como Testar em 5 Minutos

### 1. Iniciar o Sistema
```bash
cd site_igreja
python manage.py runserver
```

### 2. Testar Cadastro
- Acesse: http://localhost:8000/usuarios/cadastro/
- Preencha pelo menos: nome de usuário, nome completo, e-mail, senha
- Clique em "Cadastrar"

### 3. Login como Admin
- Acesse: http://localhost:8000/usuarios/login/
- Usuário: `admin`
- Senha: `admin123`

### 4. Aprovar Cadastro
- No dashboard, clique em "Usuários Pendentes"
- Selecione o papel (Membro/Congregado)
- Clique em "Aprovar"

### 5. Testar Login do Usuário
- Faça logout
- Tente login com o usuário aprovado

## 📋 Credenciais de Teste

**Admin/Secretário:**
- Usuário: `admin`
- Senha: `admin123`

**Usuário Teste (já cadastrado):**
- Usuário: `joao_silva`
- E-mail: `joao.silva@email.com`
- Status: Pendente (precisa ser aprovado)

## 🔗 Links Importantes

- Cadastro: http://localhost:8000/usuarios/cadastro/
- Login: http://localhost:8000/usuarios/login/
- Dashboard: http://localhost:8000/usuarios/dashboard/
- Admin Django: http://localhost:8000/admin/

## ✅ O que Funciona

- ✅ Cadastro completo com todos os campos da ficha
- ✅ Sistema de aprovação por secretários
- ✅ Dashboard com estatísticas
- ✅ Diferentes papéis (Admin, Secretário, Membro, Congregado)
- ✅ Login/Logout
- ✅ Interface responsiva

## 📞 Próximo Passo

Teste o sistema e confirme se está funcionando conforme esperado. 
Quando estiver satisfeito, podemos prosseguir para o próximo ponto do organograma!

