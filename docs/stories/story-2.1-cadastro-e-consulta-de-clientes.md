# Story 2.1: Cadastro e consulta de clientes

> **Status:** Done  
> **Épico:** 2 — Clientes e equipamentos  
> **Executor:** @dev  
> **Quality gate:** @architect  
> **Quality gate tools:** Validação do contrato OpenAPI, testes automatizados de clientes, revisão do modelo relacional  
> **Branch sugerida:** `feature/2.1-cadastro-de-clientes`

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - "Validação do contrato OpenAPI"
  - "Testes automatizados de clientes"
  - "Revisão do modelo relacional"
```

---

## História

**Como** atendente da assistência técnica,  
**quero** cadastrar, consultar, listar e atualizar clientes na API com dados de contato válidos,  
**para** manter o cadastro organizado e permitir o vínculo com equipamentos e futuras ordens de serviço.

### Contexto e valor

Esta é a primeira story do **Épico 2 (Clientes e equipamentos)**. Ela introduz o primeiro domínio de negócio da aplicação através do app `apps/customers/`, implementando a persistência da tabela `customers`, validações de formulário nos serializers, endpoints REST protegidos por autenticação (`TokenAuthentication`) e testes automatizados de ponta a ponta.

**Fonte:** [docs/prd.md — Épico 2 e Story 2.1](../../docs/prd.md#story-21-cadastro-e-consulta-de-clientes)

---

## Critérios de aceite

1. [x] O usuário autenticado deve poder cadastrar um cliente informando obrigatoriamente nome (`name`) e telefone (`phone`).
2. [x] O campo de e-mail (`email`) deve ser opcional, porém validado quanto ao formato quando fornecido.
3. [x] O usuário autenticado deve poder listar todos os clientes cadastrados (`GET /api/customers/`).
4. [x] O usuário autenticado deve poder consultar os detalhes de um cliente específico por seu identificador (`GET /api/customers/{id}/`).
5. [x] O usuário autenticado deve poder atualizar parcialmente os dados de um cliente existente (`PATCH /api/customers/{id}/`).
6. [x] A API deve rejeitar requisições inválidas ou sem campos obrigatórios com status HTTP 400 e mensagens de erro consistentes em formato JSON.
7. [x] A API deve retornar HTTP 404 Not Found caso o cliente solicitado por ID não exista.
8. [x] Todas as operações de clientes devem exigir autenticação por token (HTTP 401 para requisições não autenticadas).
9. [x] A rota e os schemas (`CustomerInput`, `Customer`) devem estar documentados no OpenAPI via `drf-spectacular`.
10. [x] Devem existir testes automatizados cobrindo cadastro com sucesso, validação de e-mail, consulta individual, listagem, atualização parcial, erros de validação e exigência de autenticação.

### Detalhamento técnico dos critérios

- **Modelo relacional:** Tabela `customers` gerenciada pelo Django ORM em `apps/customers/models.py`.
  - `id`: Chave primária inteira autoincrementável.
  - `name`: `models.CharField(max_length=255)` (obrigatório).
  - `phone`: `models.CharField(max_length=50)` (obrigatório).
  - `email`: `models.EmailField(blank=True, null=True)` (opcional, sem restrição de unicidade no MVP).
  - `created_at`: `models.DateTimeField(auto_now_add=True)` (preenchimento automático).
  - `updated_at`: `models.DateTimeField(auto_now=True)` (atualização automática).
- **Endpoints REST (`apps/customers/urls.py`):**
  - `GET /api/customers/`: Lista clientes (HTTP 200 array de `Customer`).
  - `POST /api/customers/`: Cria cliente (HTTP 201 `Customer`).
  - `GET /api/customers/{id}/`: Detalhes do cliente (HTTP 200 `Customer` ou 404 `Error`).
  - `PATCH /api/customers/{id}/`: Atualização parcial (HTTP 200 `Customer`, 400 `Error` ou 404 `Error`).
- **Segurança:** Todas as rotas de clientes exigem cabeçalho `Authorization: Token <token>`.
- **Exclusão:** Não implementar endpoint de exclusão (`DELETE`) nesta story (fora do MVP).

**Fontes:** [docs/architecture.md — Clientes](../../docs/architecture.md#clientes), [docs/architecture.md — Schema do banco de dados](../../docs/architecture.md#schema-do-banco-de-dados), [docs/architecture.md — Especificação REST/OpenAPI](../../docs/architecture.md#especificação-restopenapi)

---

## Pré-condições

- [x] Épico 1 concluído com autenticação por token (`POST /api/auth/token/`) e rota de saúde (`GET /api/health/`).
- [x] Contrato OpenAPI aprovado para os endpoints e schemas de clientes em `docs/architecture.md`.

---

## 🤖 CodeRabbit Integration

> **CodeRabbit Integration**: Disabled
>
> CodeRabbit CLI is not enabled in `core-config.yaml`.
> Quality validation will use manual review process and quality gates.

---

## Tarefas / Subtarefas

- [x] **Criar o app de domínio `apps/customers`** (AC: 1, 3, 8)
  - [x] Criar estrutura do pacote `apps/customers/` (`__init__.py`, `apps.py`).
  - [x] Registrar `"apps.customers"` em `INSTALLED_APPS` no `config/settings.py`.
- [x] **Implementar o modelo de dados `Customer`** (AC: 1, 2)
  - [x] Criar a classe `Customer` em `apps/customers/models.py` com `name`, `phone`, `email`, `created_at` e `updated_at`.
  - [x] Gerar e aplicar a migração inicial com `python manage.py makemigrations` e `python manage.py migrate`.
- [x] **Implementar Serializers e Validações** (AC: 1, 2, 6, 9)
  - [x] Criar serializers de entrada e saída em `apps/customers/serializers.py` validando campos obrigatórios e formato de e-mail.
  - [x] Configurar mapeamento e anotações OpenAPI para os schemas `CustomerInput` e `Customer`.
- [x] **Implementar Views e Roteamento de Clientes** (AC: 3, 4, 5, 7, 8)
  - [x] Criar views de clientes em `apps/customers/views.py` com suporte a listagem, criação, detalhe e atualização parcial (`PATCH`).
  - [x] Configurar rotas em `apps/customers/urls.py` e incluir no `config/urls.py` sob o prefixo `/api/customers/`.
  - [x] Assegurar proteção com `IsAuthenticated` / `TokenAuthentication`.
- [x] **Criar testes automatizados de clientes** (AC: 8, 10)
  - [x] Criar `apps/customers/tests.py` usando `APITestCase`.
  - [x] Testar criação de cliente com sucesso (HTTP 201).
  - [x] Testar criação com dados inválidos / campos ausentes (HTTP 400).
  - [x] Testar listagem e consulta individual (HTTP 200).
  - [x] Testar consulta de ID inexistente (HTTP 404).
  - [x] Testar atualização parcial com `PATCH` (HTTP 200 e HTTP 400).
  - [x] Testar rejeição de acesso sem autenticação (HTTP 401).
- [x] **Documentação e Validação** (AC: 9, 10)
  - [x] Atualizar o `README.md` com exemplos de requisições autenticadas para clientes via `curl`.
  - [x] Validar conformidade com `ruff check .` e `ruff format --check .`.
  - [x] Executar `python manage.py check` e `python manage.py test`.
  - [x] Validar integridade do schema com `python manage.py spectacular --validate`.

---

## Dev Notes

### Contexto da arquitetura

- O domínio de clientes é isolado dentro de `apps/customers/`, mantendo seus modelos, serializers, views, URLs e testes próximos.
  - **Fonte:** [docs/architecture.md — Estrutura de pastas](../../docs/architecture.md#estrutura-de-pastas)
- Acesso ao banco deve ser feito diretamente via Django ORM, sem criar camadas de repositório artificiais.
  - **Fonte:** [docs/architecture.md — Padrões arquiteturais e de design](../../docs/architecture.md#padrões-arquiteturais-e-de-design)
- O e-mail não é único no banco de dados para simplificar o cadastro do MVP, mas deve ser validado pelo serializer se informado.
  - **Fonte:** [docs/architecture.md — Schema do banco de dados](../../docs/architecture.md#schema-do-banco-de-dados)

### Estrutura de arquivos planejada

```text
apps/
├── __init__.py
└── customers/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    └── tests.py
```

---

## File List planejada

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `apps/__init__.py` | Novo | Pacote raiz de aplicações de domínio |
| `apps/customers/__init__.py` | Novo | Inicialização do pacote de clientes |
| `apps/customers/apps.py` | Novo | Configuração da app Django de clientes |
| `apps/customers/migrations/__init__.py` | Novo | Inicialização do pacote de migrações de clientes |
| `apps/customers/migrations/0001_initial.py` | Novo | Migração inicial de criação da tabela `customers` |
| `apps/customers/models.py` | Novo | Modelo de dados Customer e persistência |
| `apps/customers/serializers.py` | Novo | Serialização e validação de entrada de clientes |
| `apps/customers/views.py` | Novo | Endpoints REST de clientes (List, Create, Retrieve, PartialUpdate) |
| `apps/customers/urls.py` | Novo | Roteamento do módulo de clientes |
| `apps/customers/tests.py` | Novo | Testes automatizados com APITestCase |
| `config/settings.py` | Modificado | Registro de `apps.customers` em INSTALLED_APPS |
| `config/urls.py` | Modificado | Inclusão das rotas de clientes no roteador principal |
| `README.md` | Modificado | Instruções e exemplos de uso da API de clientes |

---

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 2026-08-22 | 0.1.0 | Criação inicial do rascunho da Story 2.1 com base no PRD e arquitetura | @sm (River) |
| 2026-08-22 | 0.2.0 | Validated GO (10/10) — Status: Draft → Ready | @po (Pax) |
| 2026-08-22 | 0.3.0 | Desenvolvimento iniciado — Status: Ready → InProgress | @dev (Dex) |
| 2026-08-22 | 0.2.1 | Refinamento pós-validação (GO 9/10): inclusão das migrações no File List | @po (Pax) |
| 2026-08-22 | 0.3.1 | Implementação concluída e validações executadas — Status: InProgress → InReview | @dev (Dex) |
| 2026-08-22 | 1.0.0 | QA Review PASS (100/100) — Status: InReview → Done | @qa (Quinn) |

---

## Dev Agent Record

### Agent Model Used

Codex GPT-5

### Debug Log References

Validações executadas diretamente no terminal. Foi necessário normalizar a mensagem de 404 e ajustar a anotação OpenAPI de segurança para usar o objeto `TokenAuth` aprovado na arquitetura.

### Completion Notes List

- Criado o app `apps.customers` com o modelo `Customer` e tabela `customers`.
- Implementadas validações de nome, telefone e e-mail opcional.
- Implementados endpoints autenticados de listagem, criação, detalhe e atualização parcial.
- Padronizados erros de validação em `{"errors": ...}` e recurso inexistente em `{"detail": "Not found."}`.
- Documentados `CustomerInput`, `Customer` e `TokenAuth` no OpenAPI.
- Criados testes de API para sucesso, falhas, 404, PATCH, autenticação e contrato OpenAPI.
- Atualizado o README com exemplos de uso via `curl`.
- CodeRabbit não executado porque está desabilitado em `.aiox-core/core-config.yaml`.

### File List

| Arquivo | Alteração |
|---|---|
| `apps/__init__.py` | Novo pacote raiz dos domínios |
| `apps/customers/__init__.py` | Novo pacote de clientes |
| `apps/customers/apps.py` | Configuração do app Django |
| `apps/customers/migrations/__init__.py` | Pacote de migrações |
| `apps/customers/migrations/0001_initial.py` | Migração da tabela `customers` |
| `apps/customers/models.py` | Modelo `Customer` |
| `apps/customers/serializers.py` | Serializers de entrada e saída |
| `apps/customers/views.py` | Endpoints protegidos de clientes |
| `apps/customers/urls.py` | Rotas do domínio |
| `apps/customers/tests.py` | Testes automatizados do domínio |
| `config/settings.py` | Registro do app e configuração OpenAPI |
| `config/urls.py` | Inclusão das rotas `/api/customers/` |
| `README.md` | Exemplos de uso da API de clientes |

---

## QA Results

### Review Date: 2026-08-22

### Reviewed By: Quinn (Test Architect)

### Code Quality Assessment

A implementação da Story 2.1 atende a todos os critérios de aceite estabelecidos no PRD e na arquitetura aprovada. O app de domínio `apps.customers` foi criado de forma modular e isolada, com persistência direta via Django ORM no modelo `Customer`. A validação nos serializers trata corretamente campos obrigatórios e e-mail opcional. As rotas REST estão devidamente protegidas por autenticação com token (`TokenAuthentication`).

### Compliance Check

- Coding Standards: ✓ Ruff passou sem erros (`check` e `format --check`).
- Project Structure: ✓ Aplicação modularizada em `apps/customers/` com modelo, serializers, views, URLs, migrações e testes.
- Testing Strategy: ✓ 10 testes dedicados de API com `APITestCase` cobrindo cenários 200, 201, 400, 401 e 404 (totalizando 17 testes na suíte global do projeto).
- All ACs Met: ✓ 10/10 critérios de aceite atendidos e testados.
- OpenAPI Contract: ✓ Schema OpenAPI 3.0.3 validado com sucesso contendo `Customer`, `CustomerInput`, `PatchedCustomerInput` e esquema de segurança `TokenAuth`.

### Security Review

- Todas as rotas de clientes exigem o cabeçalho `Authorization: Token <token>` e retornam 401 Unauthorized quando não autenticadas.
- Validação robusta de entradas para evitar injeção ou dados inconsistentes.
- Nenhuma chave ou credencial hardcoded.

### Gate Status

- Gate: PASS → `docs/qa/gates/2.1-cadastro-e-consulta-de-clientes.yml`
- Score: 100/100
- Decisão: Aprovado sem ressalvas.

### Lifecycle Transition

- PASS: InReview → Done.
