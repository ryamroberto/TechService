# Story 1.2: Autenticação de usuários por token

> **Status:** Done  
> **Épico:** 1 — Fundação da API e autenticação  
> **Executor:** @dev  
> **Quality gate:** @architect  
> **Quality gate tools:** Validação do contrato OpenAPI, testes automatizados de autenticação, revisão de segurança  
> **Branch sugerida:** `feature/1.2-autenticacao-por-token`

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - "Validação do contrato OpenAPI"
  - "Testes automatizados de autenticação"
  - "Revisão de segurança"
```

---

## História

**Como** usuário autorizado da assistência técnica (atendente ou técnico),  
**quero** me autenticar na API enviando usuário e senha para receber um token de acesso,  
**para** acessar com segurança os recursos protegidos de clientes, equipamentos e ordens de serviço.

### Contexto e valor

Esta story conclui a fundação do **Épico 1**, habilitando a infraestrutura de segurança e autenticação baseada em token do Django REST Framework. Ela disponibiliza o endpoint `POST /api/auth/token/`, ativa a persistência de tokens (`authtoken`), define a política padrão de proteção para operações de negócio e documenta a criação de usuários locais para desenvolvimento.

**Fonte:** [docs/prd.md — Épico 1 e Story 1.2](../../docs/prd.md#story-12-autenticação-de-usuários)

---

## Critérios de aceite

1. [x] Deve existir uma forma documentada no README para criar um usuário local de acesso à API.
2. [x] A API deve disponibilizar a rota `POST /api/auth/token/` para obtenção de token de autenticação.
3. [x] Usuários com credenciais válidas devem receber resposta HTTP 200 contendo o token de autenticação no formato JSON.
4. [x] Credenciais inválidas ou incompletas devem ser rejeitadas com status HTTP 400/401 e mensagem de erro em formato JSON consistente.
5. [x] Senhas não podem ser retornadas nas respostas da API nem armazenadas em texto puro no banco de dados.
6. [x] A rota `POST /api/auth/token/` deve estar documentada no schema OpenAPI (`/api/schema/`) conforme o contrato arquitetural (`TokenRequest` e `TokenResponse`).
7. [x] A rota pública de saúde (`GET /api/health/`) deve continuar acessível sem exigência de autenticação.
8. [x] Devem existir testes automatizados cobrindo cenários de sucesso (obtenção de token), falha (credenciais inválidas, campos ausentes) e segurança.

### Detalhamento técnico dos critérios

- **Endpoint de autenticação:** `POST /api/auth/token/` (público para envio de credenciais).
- **Entrada:** JSON com `username` e `password` obrigatórios (`TokenRequest`).
- **Saída de sucesso:** HTTP 200 com JSON `{"token": "<string_do_token>"}` (`TokenResponse`).
- **Saída de erro:** HTTP 400 Bad Request com `detail` ou erros de campo quando inválido/ausente.
- **Autenticação no Django:** Utilizar `rest_framework.authtoken` e `rest_framework.authentication.TokenAuthentication`.
- **Formato de cabeçalho nas requisições autenticadas:** `Authorization: Token <token>`.
- **Model de usuário:** `django.contrib.auth.models.User` padrão (sem criar app `users/` no MVP).

**Fontes:** [docs/architecture.md — Autenticação](../../docs/architecture.md#autenticação--preocupação-transversal), [docs/architecture.md — Especificação REST/OpenAPI](../../docs/architecture.md#especificação-restopenapi), [docs/architecture.md — Segurança](../../docs/architecture.md#segurança)

---

## Pré-condições

- [x] Story 1.1 concluída e integrada com scaffold básico Django/DRF, health check e testes.
- [x] Contrato OpenAPI aprovado para `TokenRequest` e `TokenResponse` em `docs/architecture.md`.

---

## 🤖 CodeRabbit Integration

> **CodeRabbit Integration**: Disabled
>
> CodeRabbit CLI is not enabled in `core-config.yaml`.
> Quality validation will use manual review process and quality gates.

---

## Tarefas / Subtarefas

- [x] **Configurar aplicação de autenticação por token** (AC: 2, 7)
  - [x] Adicionar `"rest_framework.authtoken"` a `INSTALLED_APPS` em `config/settings.py`.
  - [x] Configurar `TokenAuthentication` em `REST_FRAMEWORK` no `config/settings.py`.
  - [x] Garantir que `GET /api/health/` permaneça explicitamente público (`permission_classes = (AllowAny,)`).
  - [x] Executar `python manage.py migrate` para criar a tabela `authtoken_token`.
- [x] **Registrar endpoint de obtenção de token** (AC: 2, 3, 4, 6)
  - [x] Registrar a rota `api/auth/token/` em `config/urls.py` com view pública de emissão de token.
  - [x] Verificar que o endpoint está anotado e mapeado no schema OpenAPI gerado pelo `drf-spectacular`.
- [x] **Criar testes automatizados de autenticação** (AC: 3, 4, 5, 7, 8)
  - [x] Criar classe de testes de autenticação em `config/tests.py` usando `APITestCase`.
  - [x] Testar obtenção de token com usuário e senha válidos (HTTP 200 + token no payload).
  - [x] Testar rejeição com credenciais inválidas (HTTP 400).
  - [x] Testar envio de payload vazio ou campos obrigatórios ausentes (HTTP 400).
  - [x] Validar que senhas nunca são expostas na resposta nem armazenadas em texto puro.
  - [x] Validar que a rota de saúde continua respondendo 200 OK sem token.
- [x] **Atualizar documentação e instruções de uso** (AC: 1, 5)
  - [x] Atualizar `README.md` com instruções de como criar usuário local (`createsuperuser`) e como obter o token via `curl`.
  - [x] Exemplificar o uso do header `Authorization: Token <token>`.
- [x] **Validação de qualidade e linters** (AC: 8)
  - [x] Executar `ruff check .` e `ruff format --check .`.
  - [x] Executar `python manage.py check` e `python manage.py test`.
  - [x] Executar `python manage.py spectacular --validate`.

---

## Dev Notes

### Contexto da arquitetura

- A autenticação é uma preocupação transversal do monólito, implementada com o módulo padrão `rest_framework.authtoken` da DRF.
  - **Fonte:** [docs/architecture.md — Autenticação](../../docs/architecture.md#autenticação--preocupação-transversal)
- Não criar app `users/` ou modelos customizados de usuário; o usuário padrão do Django atende 100% aos requisitos do MVP.
  - **Fonte:** [docs/architecture.md — Estrutura de pastas](../../docs/architecture.md#estrutura-de-pastas)
- As senhas são tratadas exclusivamente pelos mecanismos de hash do Django (`PBKDF2PasswordHasher`) e nunca trafegam em respostas.
  - **Fonte:** [docs/architecture.md — Segurança](../../docs/architecture.md#segurança)

### Estrutura de arquivos

- As configurações de autenticação residem em `config/settings.py`.
- O roteamento do token é adicionado em `config/urls.py`.
- Os testes de autenticação são adicionados em `config/tests.py` junto aos testes de fundação do projeto.

---

## File List planejada

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `config/settings.py` | Modificado | Inclusão de `rest_framework.authtoken` e configuração de autenticação |
| `config/urls.py` | Modificado | Registro do endpoint `POST /api/auth/token/` |
| `config/views.py` | Modificado | Serializers, contrato OpenAPI e view pública de emissão de token |
| `config/tests.py` | Modificado | Adição dos testes automatizados de autenticação |
| `README.md` | Modificado | Instruções de criação de usuário, obtenção de token e uso do header de autenticação |

---

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 2026-08-22 | 0.1.0 | Criação inicial do rascunho da Story 1.2 com base no PRD e arquitetura | @sm (River) |
| 2026-08-22 | 0.2.0 | Validated GO (10/10) — Status: Draft → Ready | @po (Pax) |
| 2026-08-22 | 0.3.0 | Desenvolvimento iniciado — Status: Ready → InProgress | @dev (Dex) |
| 2026-08-22 | 0.3.1 | Implementação concluída e validações executadas — Status: InProgress → InReview | @dev (Dex) |
| 2026-08-22 | 1.0.0 | QA Review PASS (100/100) — Status: InReview → Done | @qa (Quinn) |

---

## Dev Agent Record

### Agent Model Used

Codex GPT-5

### Debug Log References

Validações executadas diretamente no terminal; não houve falha de código persistente. A primeira verificação manual usou o host padrão `testserver` fora do test runner e foi repetida com `localhost`, host permitido pela configuração local.

### Completion Notes List

- Habilitado `rest_framework.authtoken` e `TokenAuthentication` como autenticação padrão.
- Configurado `IsAuthenticated` como permissão padrão para futuras rotas de negócio.
- Mantidas as rotas de health check e emissão de token explicitamente públicas.
- Implementada emissão de token com usuário padrão do Django, validação de entrada e erros JSON consistentes.
- Adicionados serializers explícitos para `TokenRequest`, `TokenResponse` e erros no schema OpenAPI.
- Adicionados testes de sucesso, credenciais inválidas, campos ausentes, hash de senha e health público.
- Atualizado o README com criação de usuário, obtenção de token e header `Authorization`.
- CodeRabbit não executado porque está desabilitado em `.aiox-core/core-config.yaml`.

### File List

| Arquivo | Alteração |
|---|---|
| `config/settings.py` | Autenticação, permissões padrão e segurança OpenAPI |
| `config/urls.py` | Rota `POST /api/auth/token/` |
| `config/views.py` | View, serializers e contrato OpenAPI do token; health público |
| `config/tests.py` | Testes automatizados da autenticação e regressão do health check |
| `README.md` | Instruções de criação de usuário e uso do token |
| `docs/stories/story-1.2-autenticacao-por-token.md` | Checkboxes, registro do desenvolvimento e lista de arquivos |

---

## QA Results

### Review Date: 2026-08-22

### Reviewed By: Quinn (Test Architect)

### Code Quality Assessment

A implementação da Story 1.2 atende perfeitamente a todos os requisitos funcionais e não-funcionais definidos no PRD e na arquitetura aprovada. O endpoint `POST /api/auth/token/` valida as credenciais com segurança, retorna o token no formato especificado, rejeita credenciais inválidas com erros consistentes em JSON e não expõe senhas. A suíte de testes passou com 100% de sucesso.

### Compliance Check

- Coding Standards: ✓ Ruff passou sem erros (`check` e `format --check`).
- Project Structure: ✓ Configurações, rotas, views e testes localizados adequadamente em `config/`.
- Testing Strategy: ✓ 7 testes automatizados com `APITestCase` cobrindo cenários de sucesso, falha, segurança e regressão da rota de saúde.
- All ACs Met: ✓ 8/8 critérios de aceite validados e comprovados.
- OpenAPI Contract: ✓ Schema validado com sucesso pelo drf-spectacular com `TokenRequest`, `TokenResponse`, `Error` e esquema de segurança `TokenAuth`.

### Security Review

- Senhas tratadas exclusivamente com hash seguro (PBKDF2) pelo Django User model.
- Senhas nunca retornadas em respostas JSON e write-only nos serializers.
- Rota de health check permanece pública (`AllowAny`), enquanto a autenticação por token é a política padrão para rotas protegidas.
- Nenhuma chave ou segredo exposto no código ou nos testes.

### Gate Status

- Gate: PASS → `docs/qa/gates/1.2-autenticacao-por-token.yml`
- Score: 100/100
- Decisão: Aprovado sem ressalvas.

### Lifecycle Transition

- PASS: InReview → Done.
