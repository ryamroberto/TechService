# TechService API

API REST para gerenciamento de clientes, equipamentos e ordens de serviço de uma pequena assistência técnica.

---

## 📌 Visão Geral

A **TechService API** é desenvolvida em Python com Django e Django REST Framework (DRF), seguindo uma arquitetura de monólito modular. Nesta primeira etapa, a API disponibiliza a fundação executável do projeto, autenticação por token e o cadastro protegido de clientes, além da suíte inicial de testes e das instruções de desenvolvimento local. Os demais domínios de negócio serão implementados nas stories subsequentes.

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
