# TechService API

API REST para gerenciamento de clientes, equipamentos e ordens de serviço de uma pequena assistência técnica.

---

## 📌 Visão Geral

A **TechService API** é desenvolvida em Python com Django e Django REST Framework (DRF), seguindo uma arquitetura de monólito modular. Nesta primeira etapa (Épico 1), a API disponibiliza a fundação executável do projeto, a rota pública de verificação de integridade (*health check*), autenticação por token, a suíte inicial de testes e as instruções de desenvolvimento local. Os domínios de negócio serão implementados nas stories subsequentes.

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
