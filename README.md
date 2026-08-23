# TechService API

API REST para gerenciamento de clientes, equipamentos e ordens de serviço de uma pequena assistência técnica.

> **Status:** MVP concluído e validado para portfólio. O projeto é uma API backend júnior, executada localmente, sem frontend e sem infraestrutura de produção.

---

## 📌 Visão Geral

A **TechService API** é desenvolvida em Python com Django e Django REST Framework (DRF), seguindo uma arquitetura de monólito modular. O MVP cobre o fluxo principal de uma assistência técnica: autenticar um usuário, cadastrar clientes e equipamentos, abrir uma ordem de serviço, registrar seu andamento, consultar a fila e encerrá-la como entregue ou cancelada.

O projeto foi mantido propositalmente pequeno para demonstrar fundamentos importantes de backend: modelagem relacional, validação de entrada, autenticação por token, endpoints REST, documentação OpenAPI e testes automatizados.

## 🎯 O que este projeto demonstra

- Construção de uma API REST com Django e Django REST Framework.
- Relacionamentos entre clientes, equipamentos e ordens de serviço.
- Autenticação com `TokenAuthentication` e proteção das rotas de negócio.
- Validação de payloads, filtros, status HTTP e respostas JSON de erro.
- Documentação interativa com Swagger, Redoc e contrato OpenAPI 3.0.3.
- Testes de API com o banco isolado do Django Test Runner.
- Organização simples em um monólito modular, sem camadas artificiais.

## 🔄 Fluxo principal para demonstração

1. Criar um usuário local e obter um token.
2. Cadastrar um cliente e um equipamento vinculado a ele.
3. Abrir uma ordem de serviço com o problema informado.
4. Atualizar diagnóstico, orçamento e andamento.
5. Consultar a ordem e encerrá-la como `entregue` ou `cancelado`.

Esse fluxo pode ser executado pelos exemplos de `curl` deste README ou diretamente pela interface Swagger.

## 📚 Resumo dos endpoints

| Domínio | Operações principais | Autenticação |
|---|---|---|
| Saúde | `GET /api/health/` | Pública |
| Autenticação | `POST /api/auth/token/` | Pública |
| Clientes | `GET`, `POST /api/customers/`; `GET`, `PATCH /api/customers/{id}/` | Token |
| Equipamentos | `GET`, `POST /api/equipment/`; `GET`, `PATCH /api/equipment/{id}/` | Token |
| Ordens de serviço | `GET`, `POST /api/service-orders/`; `GET`, `PATCH /api/service-orders/{id}/` | Token |

O contrato completo, incluindo schemas, filtros e respostas de erro, está disponível no Swagger e no endpoint `/api/schema/`.

---

## 🚀 Tecnologias e Dependências

- **Python:** 3.13.15
- **Django:** 5.2.17
- **Django REST Framework:** 3.16.1
- **drf-spectacular:** 0.30.0 (OpenAPI 3.0)
- **Ruff:** 0.16.2 (Linter e formatador de código)
- **SQLite:** Banco relacional para desenvolvimento local

---

## 🛠️ Configuração do Ambiente e Instalação

### 1. Clonar ou acessar o repositório

Abra o terminal no diretório raiz do projeto:

```bash
cd TechService
```

### 2. Criar e ativar o ambiente virtual (`venv`)

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

**No Windows:**
```powershell
Copy-Item .env.example .env
```

**No Linux/macOS:**
```bash
cp .env.example .env
```

---

## 🗄️ Banco de Dados e Migrações

Execute as migrações iniciais para estruturar o banco de dados SQLite local:

```bash
python manage.py migrate
```

*(Opcional)* Crie um superusuário administrativo para gerenciar usuários:

```bash
python manage.py createsuperuser
```

## 🔐 Autenticação por Token

Crie um usuário local usando o comando administrativo do Django:

```bash
python manage.py createsuperuser
```

Com a API em execução, obtenha um token enviando o usuário e a senha para a rota pública:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"atendente","password":"sua-senha"}'
```

Resposta esperada:

```json
{
  "token": "0123456789abcdef..."
}
```

Use o token para acessar os endpoints de negócio protegidos:

```text
Authorization: Token <token>
```

As senhas são armazenadas pelo hash padrão do Django e nunca são retornadas pela API. A rota `GET /api/health/` e a rota de obtenção de token permanecem públicas.

---

## 👥 Clientes

As operações de clientes exigem o header `Authorization: Token <token>`.

### Criar cliente

```bash
curl -X POST http://127.0.0.1:8000/api/customers/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria da Silva","phone":"(11) 99999-9999","email":"maria@example.com"}'
```

### Listar clientes

```bash
curl http://127.0.0.1:8000/api/customers/ \
  -H "Authorization: Token <token>"
```

### Consultar ou atualizar um cliente

```bash
curl http://127.0.0.1:8000/api/customers/1/ \
  -H "Authorization: Token <token>"

curl -X PATCH http://127.0.0.1:8000/api/customers/1/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"phone":"(11) 98888-8888"}'
```

O e-mail é opcional, mas precisa estar em formato válido quando informado. A API não implementa exclusão de clientes no MVP.

---

## 💻 Equipamentos

As operações de equipamentos exigem o header `Authorization: Token <token>` e vinculam cada aparelho a um cliente existente.

### Criar equipamento

```bash
curl -X POST http://127.0.0.1:8000/api/equipment/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "type": "Celular", "brand": "Samsung", "model": "Galaxy A54", "identifier": "IMEI-123456789"}'
```

### Listar equipamentos (todos ou filtrados por cliente)

```bash
# Listar todos os equipamentos
curl http://127.0.0.1:8000/api/equipment/ \
  -H "Authorization: Token <token>"

# Filtrar equipamentos por ID do cliente
curl "http://127.0.0.1:8000/api/equipment/?customer_id=1" \
  -H "Authorization: Token <token>"
```

### Consultar ou atualizar um equipamento

```bash
# Consultar por ID
curl http://127.0.0.1:8000/api/equipment/1/ \
  -H "Authorization: Token <token>"

# Atualizar parcialmente com PATCH
curl -X PATCH http://127.0.0.1:8000/api/equipment/1/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"model": "Galaxy A54 5G", "identifier": "SN-NEW-987"}'
```

O campo `identifier` é opcional. A descrição do problema não pertence ao equipamento (será registrada na ordem de serviço). A API não implementa exclusão de equipamentos no MVP.

---

## 📋 Ordens de Serviço

As operações de ordens de serviço exigem o header `Authorization: Token <token>`. A abertura de ordem vincula um cliente e um equipamento (que deve pertencer ao cliente informado) e registra o problema relatado.

### Abrir ordem de serviço

```bash
curl -X POST http://127.0.0.1:8000/api/service-orders/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "equipment_id": 1,
    "problem_description": "Celular não liga após queda."
  }'
```

**Exemplo de resposta (HTTP 201 Created):**

```json
{
  "id": 1,
  "customer_id": 1,
  "equipment_id": 1,
  "problem_description": "Celular não liga após queda.",
  "status": "recebido",
  "diagnosis": null,
  "estimated_budget": null,
  "notes": null,
  "created_at": "2026-08-22T21:45:00-03:00",
  "updated_at": "2026-08-22T21:45:00-03:00"
}
```

Toda nova ordem de serviço é criada automaticamente com status inicial `recebido`. A API rejeita requisições caso o equipamento informado não pertença ao cliente selecionado (HTTP 400 Bad Request).

### Atualizar ordem de serviço (diagnóstico, orçamento e andamento)

```bash
curl -X PATCH http://127.0.0.1:8000/api/service-orders/1/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "em_diagnostico",
    "diagnosis": "Curto-circuito na placa lógica principal.",
    "estimated_budget": "350.50",
    "notes": "Cliente informou que aparelho molhou na chuva."
  }'
```

**Exemplo de resposta (HTTP 200 OK):**

```json
{
  "id": 1,
  "customer_id": 1,
  "equipment_id": 1,
  "problem_description": "Celular não liga após queda.",
  "status": "em_diagnostico",
  "diagnosis": "Curto-circuito na placa lógica principal.",
  "estimated_budget": "350.50",
  "notes": "Cliente informou que aparelho molhou na chuva.",
  "created_at": "2026-08-22T21:45:00-03:00",
  "updated_at": "2026-08-23T11:55:00-03:00"
}
```

A atualização é parcial e aceita os campos `status`, `diagnosis`, `estimated_budget` e `notes`. Os campos de vínculo (`customer_id`, `equipment_id`) e a descrição do problema (`problem_description`) são imutáveis após a abertura.

### Listar ordens de serviço (com filtros opcionais)

```bash
# Listar todas as ordens (ordenadas pelas mais recentes)
curl http://127.0.0.1:8000/api/service-orders/ \
  -H "Authorization: Token <token>"

# Filtrar por cliente
curl "http://127.0.0.1:8000/api/service-orders/?customer_id=1" \
  -H "Authorization: Token <token>"

# Filtrar por status
curl "http://127.0.0.1:8000/api/service-orders/?status=em_conserto" \
  -H "Authorization: Token <token>"

# Combinar filtros de cliente e status
curl "http://127.0.0.1:8000/api/service-orders/?customer_id=1&status=entregue" \
  -H "Authorization: Token <token>"
```

### Consultar ordem de serviço por ID

```bash
curl http://127.0.0.1:8000/api/service-orders/1/ \
  -H "Authorization: Token <token>"
```

### Encerrar ordem de serviço

Para encerrar uma ordem, envie um `PATCH` definindo o `status` como `entregue` ou `cancelado`:

```bash
# Marcar como entregue ao cliente
curl -X PATCH http://127.0.0.1:8000/api/service-orders/1/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"status":"entregue"}'

# Cancelar atendimento com justificativa nas observações
curl -X PATCH http://127.0.0.1:8000/api/service-orders/1/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "cancelado",
    "notes": "Cliente optou por não aprovar o orçamento."
  }'
```

Ordens encerradas (`entregue` ou `cancelado`) permanecem registradas e disponíveis para consulta detalhada e listagem.

---

## ▶️ Executando a API

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A API estará acessível em: `http://127.0.0.1:8000/`

---

## 🩺 Verificação de Saúde (*Health Check*)

A rota de saúde é pública e permite verificar a disponibilidade da API:

- **Método:** `GET`
- **URL:** `http://127.0.0.1:8000/api/health/`

### Exemplo de requisição:

```bash
curl -X GET http://127.0.0.1:8000/api/health/
```

### Exemplo de resposta (HTTP 200 OK):

```json
{
  "status": "ok",
  "service": "TechService API"
}
```

---

## 📖 Documentação Interativa (Swagger & Redoc)

Com o servidor em execução, acesse:

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/swagger/`
- **Redoc:** `http://127.0.0.1:8000/api/docs/redoc/`
- **Schema OpenAPI (YAML/JSON):** `http://127.0.0.1:8000/api/schema/`

---

## 🧪 Execução dos Testes Automatizados

Para executar toda a suíte de testes com o Django Test Runner:

```bash
python manage.py test
```

---

## 🔍 Qualidade de Código e Linting

O projeto utiliza **Ruff** para análise estática e formatação:

```bash
# Verificar problemas de código e estilo
ruff check .

# Formatar o código automaticamente
ruff format .
```

## ✅ Validação do MVP

Validações executadas no projeto:

- `python manage.py test` — 62 testes aprovados.
- `python manage.py check` — nenhum problema identificado.
- `python manage.py makemigrations --check --dry-run` — nenhuma migration pendente.
- `python manage.py spectacular --validate` — contrato OpenAPI válido.
- `python -m ruff check .` — sem problemas de lint.
- `python -m ruff format --check .` — arquivos formatados.

## 🚧 Limites atuais

Este é um MVP de portfólio executado localmente. Não fazem parte do escopo atual: frontend, pagamentos, estoque, notificações, anexos, histórico detalhado de status, permissões por papel, multiempresa, filas, Docker obrigatório, CI/CD e deploy público.

Antes de usar a API em produção, seria necessário configurar HTTPS, `DEBUG=False`, uma chave secreta forte, cookies seguros, banco PostgreSQL, backups, monitoramento e controle de acesso adequado ao negócio.

## 💼 Contexto para portfólio e freelas

Este projeto representa uma solução inicial que pode ser adaptada para pequenas assistências técnicas. Ele não pretende ser um SaaS pronto para produção; seu objetivo é demonstrar capacidade de transformar um problema operacional em uma API testada, documentada e explicável.

### Possíveis evoluções comerciais

- Publicar a API em uma plataforma simples com PostgreSQL.
- Criar uma interface web consumindo o contrato OpenAPI existente.
- Adicionar usuários, papéis e isolamento por empresa.
- Incluir notificações, anexos e histórico quando houver requisitos reais.

Essas evoluções devem entrar somente quando houver necessidade de um cliente, mantendo o MVP atual simples e compreensível.
