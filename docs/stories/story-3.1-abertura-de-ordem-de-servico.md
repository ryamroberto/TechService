# Story 3.1: Abertura de ordem de serviço

> **Status:** Ready for Review  
> **Épico:** 3 — Ordens de serviço e acompanhamento  
> **Executor:** @dev  
> **Quality gate:** @architect  
> **Quality gate tools:** Validação do contrato OpenAPI, testes automatizados de abertura, revisão da consistência cliente-equipamento  
> **Branch sugerida:** `feature/3.1-abertura-de-ordem-de-servico`

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - "Validação do contrato OpenAPI"
  - "Testes automatizados de abertura"
  - "Revisão da consistência cliente-equipamento"
```

---

## História

**Como** atendente da assistência técnica,  
**quero** abrir uma ordem de serviço para um equipamento,  
**para** registrar a solicitação de conserto do cliente.

### Contexto e valor

Esta é a primeira story do **Épico 3 (Ordens de serviço e acompanhamento)**. Ela conecta os cadastros concluídos nos Épicos 1 e 2 ao fluxo principal da assistência técnica: receber um equipamento e registrar o problema relatado pelo cliente.

A ordem deve manter referências explícitas ao cliente e ao equipamento. Como regra de integridade, o equipamento informado precisa pertencer ao cliente informado na mesma requisição.

Esta story cobre somente a abertura da ordem. Atualização de status, diagnóstico, orçamento e observações será tratada na Story 3.2; consulta e encerramento serão tratados na Story 3.3.

**Fontes:** [docs/prd.md — Épico 3 e Story 3.1](../../docs/prd.md#story-31-abertura-de-ordem-de-serviço), [docs/architecture.md — Ordem de serviço](../../docs/architecture.md#ordem-de-serviço), [docs/architecture/schema-service-orders.md](../../docs/architecture/schema-service-orders.md)

---

## Critérios de aceite

1. [x] Um usuário autenticado deve conseguir criar uma ordem de serviço por `POST /api/service-orders/`.
2. [x] A criação deve exigir `customer_id`, `equipment_id` e `problem_description`.
3. [x] `customer_id` deve referenciar um cliente existente.
4. [x] `equipment_id` deve referenciar um equipamento existente.
5. [x] A API deve rejeitar a criação quando o equipamento não pertencer ao cliente informado, retornando HTTP 400 em JSON.
6. [x] `problem_description` deve ser obrigatória e não pode ser vazia ou inválida.
7. [x] Toda ordem criada deve receber automaticamente o status técnico `recebido`, retornado na resposta, sem iniciar nesta story o fluxo de atualização de status.
8. [x] Quando a criação for válida, a API deve retornar HTTP 201 com a ordem persistida, incluindo identificador, referências, problema, status e timestamps.
9. [x] Quando o cliente, o equipamento ou a descrição forem inválidos, a API deve retornar HTTP 400 em formato de erro consistente e não deve persistir a ordem.
10. [x] A rota de criação deve exigir `Authorization: Token <token>` e retornar HTTP 401 para requisições não autenticadas.
11. [x] O contrato OpenAPI deve documentar `POST /api/service-orders/`, `ServiceOrderInput`, `ServiceOrder`, `ServiceOrderStatus` e a segurança `TokenAuth`.
12. [x] Devem existir testes automatizados de criação válida, validações, consistência entre cliente/equipamento e autenticação.

### Detalhamento técnico dos critérios

- **Modelo relacional:** criar `ServiceOrder` no app `apps/service_orders/`, com FK obrigatória para `Customer` (`on_delete=models.PROTECT`) e FK obrigatória para `Equipment` (`on_delete=models.PROTECT`), conforme parecer do `@data-engineer`.
- **Campos da ordem:**
  - `customer_id`: referência obrigatória a `customers.id` (`on_delete=models.PROTECT`).
  - `equipment_id`: referência obrigatória a `equipment.id` (`on_delete=models.PROTECT`).
  - `problem_description`: descrição obrigatória do problema relatado.
  - `status`: inicia automaticamente em `recebido` (`choices=ServiceOrderStatus.choices`).
  - `diagnosis`: opcional, previsto para o andamento do conserto.
  - `estimated_budget`: opcional e não negativo (`CheckConstraint >= 0`), previsto para o andamento do conserto.
  - `notes`: opcional, previsto para o andamento do conserto.
  - `created_at`: data de abertura preenchida automaticamente.
  - `updated_at`: data da última alteração preenchida automaticamente.
- **Endpoint desta story:** `POST /api/service-orders/`, protegido por `TokenAuth`, retornando HTTP 201 ou HTTP 400/401 conforme o contrato.
- **Validação do relacionamento:** validar nos serializers que `equipment.customer_id == customer_id` antes de salvar. Não usar trigger ou regra SQL específica para isso no MVP.
- **Status:** usar o valor técnico `recebido`, conforme o enum do contrato. Não implementar atualização de status, diagnóstico, orçamento ou observações nesta story.
- **Persistência:** usar o Django ORM diretamente e gerar migration versionada.
- **Exclusões e consultas:** não implementar `DELETE`, listagem, consulta individual ou atualização nesta story; essas responsabilidades ficam nas stories posteriores do Épico 3.
- **Decisões de schema:** validadas pelo `@data-engineer` em `docs/architecture/schema-service-orders.md` (`on_delete=models.PROTECT`, índices `so_status_idx`, `so_customer_status_idx`, `so_created_at_desc_idx` e constraints de validação).

**Fontes:** [docs/architecture.md — Especificação REST/OpenAPI](../../docs/architecture.md#especificação-restopenapi), [docs/architecture.md — Schema do banco de dados](../../docs/architecture.md#schema-do-banco-de-dados), [docs/architecture/schema-service-orders.md](../../docs/architecture/schema-service-orders.md)

---

## Pré-condições

- [x] Épico 1 concluído com autenticação por token (`POST /api/auth/token/`) e proteção das rotas de negócio.
- [x] Épico 2 concluído com os modelos e endpoints de `Customer` e `Equipment`.
- [x] O contrato OpenAPI de ordens de serviço em `docs/architecture.md` está disponível como fonte de referência.
- [x] O `@data-engineer` validou os detalhes de schema, `on_delete` (`PROTECT`), índices, migration e constraints antes da implementação do modelo ([docs/architecture/schema-service-orders.md](../../docs/architecture/schema-service-orders.md)).

---

## Integração com CodeRabbit

> **Integração com CodeRabbit: desabilitada**
>
> O CLI do CodeRabbit não está habilitado em `core-config.yaml`.
> A validação de qualidade será feita por revisão manual e pelos quality gates definidos nesta story.
> Para habilitar, defina `coderabbit_integration.enabled: true` em `core-config.yaml`.

---

## Tarefas / Subtarefas

- [x] **Criar o app de domínio `apps/service_orders`** (AC: 1, 10)
  - [x] Criar `__init__.py`, `admin.py`, `apps.py` e `migrations/__init__.py`.
  - [x] Registrar `apps.service_orders` em `INSTALLED_APPS` no `config/settings.py`.
- [x] **Validar o modelo e os relacionamentos** (AC: 2, 3, 4, 5, 7)
  - [x] Revisar com o `@data-engineer` os detalhes de FK, `on_delete`, índices, constraints e migration ([docs/architecture/schema-service-orders.md](../../docs/architecture/schema-service-orders.md)).
  - [x] Criar o modelo `ServiceOrder` com os campos definidos na arquitetura.
  - [x] Configurar status inicial `recebido` sem implementar o fluxo de atualização desta story.
  - [x] Gerar e aplicar a migration inicial com `python manage.py makemigrations` e `python manage.py migrate`.
- [x] **Implementar serializers e validações** (AC: 2, 3, 4, 5, 6, 9, 11)
  - [x] Validar IDs existentes de cliente e equipamento.
  - [x] Validar que o equipamento pertence ao cliente informado.
  - [x] Validar `problem_description` obrigatória antes da persistência.
  - [x] Configurar os schemas `ServiceOrderInput`, `ServiceOrder` e `ServiceOrderStatus` no OpenAPI.
- [x] **Implementar criação e roteamento** (AC: 1, 7, 8, 10, 11)
  - [x] Implementar somente `POST /api/service-orders/` nesta story.
  - [x] Incluir a rota em `config/urls.py` sob o prefixo `/api/service-orders/`.
  - [x] Proteger a operação com `TokenAuthentication` e `IsAuthenticated`.
  - [x] Retornar HTTP 201 com o status inicial `recebido` quando a ordem for criada.
- [x] **Criar testes automatizados** (AC: 5, 6, 8, 9, 10, 12)
  - [x] Usar `APITestCase` e o banco de testes do Django.
  - [x] Testar criação válida com cliente e equipamento relacionados.
  - [x] Testar cliente inexistente, equipamento inexistente e descrição ausente/vazia.
  - [x] Testar equipamento pertencente a outro cliente.
  - [x] Testar status inicial `recebido` e resposta HTTP 201.
  - [x] Testar ausência de persistência quando a validação falhar.
  - [x] Testar requisição sem token retornando HTTP 401.
- [x] **Documentação e validação** (AC: 11, 12)
  - [x] Atualizar o `README.md` com exemplo autenticado de abertura de ordem, seguindo o padrão das stories anteriores.
  - [x] Executar `python manage.py check` e `python manage.py test`.
  - [x] Validar o contrato com `python manage.py spectacular --validate`.
  - [x] Executar `ruff check .` e `ruff format --check .`.

---

## Dev Notes

### Contexto da arquitetura

- O domínio de ordens de serviço deve ficar isolado em `apps/service_orders/`, seguindo o mesmo padrão modular dos apps `customers` e `equipment`.
- Uma ordem pertence a um cliente e referencia um equipamento; a aplicação deve confirmar que os dois relacionamentos são consistentes antes de gravar.
- As operações de ordens de serviço são protegidas por token. Nesta story, somente a criação será implementada.
- O status técnico inicial é `recebido`. Os valores previstos no contrato são `recebido`, `em_diagnostico`, `aguardando_aprovacao`, `em_conserto`, `pronto`, `entregue` e `cancelado`.
- Não criar camada de repository, service ou use case; usar o ORM e serializers diretamente, salvo decisão concreta validada pela arquitetura.
- Não adicionar frontend, filas, microsserviços, integrações externas, pagamentos, notificações ou regras de autorização por papel.

**Fontes:** [docs/architecture.md — Domínios e responsabilidades](../../docs/architecture.md#domínios-e-responsabilidades), [docs/architecture.md — Relacionamentos e regras](../../docs/architecture.md#relacionamentos-e-regras), [docs/architecture.md — Padrões arquiteturais e de design](../../docs/architecture.md#padrões-arquiteturais-e-de-design)

### Contexto das stories anteriores

- A Story 2.1 disponibiliza `Customer`.
- A Story 2.2 disponibiliza `Equipment` e seu vínculo com `Customer`.
- A implementação deve reutilizar esses modelos e manter os padrões existentes de autenticação, erros JSON, testes, OpenAPI e documentação.
- Não alterar o escopo das stories anteriores nem antecipar as regras de atualização da Story 3.2.

### Estrutura de arquivos planejada

```text
apps/
└── service_orders/
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
config/
├── settings.py
└── urls.py
README.md
```

### Testes

- Usar `APITestCase` do Django REST Framework.
- Usar o banco criado e destruído automaticamente pelo Django Test Runner; não depender do banco local ou de dados reais.
- Cobrir o caminho feliz e os principais erros: HTTP 201, 400 e 401.
- Criar previamente dois clientes e equipamentos em testes de relacionamento, incluindo um equipamento pertencente ao cliente diferente do selecionado.
- Confirmar que uma ordem inválida não fica persistida.
- Não criar testes end-to-end de frontend; o MVP é backend-only.

**Fonte:** [docs/architecture.md — Estratégia de testes](../../docs/architecture.md#estratégia-de-testes)

---

## Lista de arquivos planejada

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `apps/service_orders/__init__.py` | Novo | Inicialização do pacote de ordens de serviço |
| `apps/service_orders/apps.py` | Novo | Configuração da app Django de ordens |
| `apps/service_orders/admin.py` | Novo | Configuração do domínio no admin, conforme padrão da estrutura |
| `apps/service_orders/migrations/__init__.py` | Novo | Inicialização do pacote de migrations |
| `apps/service_orders/migrations/0001_initial.py` | Novo | Migration inicial da tabela `service_orders` |
| `apps/service_orders/models.py` | Novo | Modelo `ServiceOrder` e relacionamentos |
| `apps/service_orders/serializers.py` | Novo | Validação e serialização da abertura da ordem |
| `apps/service_orders/views.py` | Novo | Endpoint protegido de criação |
| `apps/service_orders/urls.py` | Novo | Rota `/api/service-orders/` |
| `apps/service_orders/tests.py` | Novo | Testes automatizados da abertura |
| `config/settings.py` | Modificado | Registro de `apps.service_orders` |
| `config/urls.py` | Modificado | Inclusão da rota de ordens de serviço |
| `README.md` | Modificado | Exemplo de abertura autenticada de ordem |

---

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 2026-08-22 | 0.1.0 | Criação inicial do rascunho da Story 3.1 com base no PRD e na arquitetura aprovada | @sm (River) |
| 2026-08-22 | 0.1.1 | Validation NO-GO — revisão de schema do @data-engineer pendente antes da implementação | @po (Pax) |
| 2026-08-22 | 0.2.0 | Revisão e validação formal de schema, on_delete (PROTECT), índices, constraints e migrations pelo @data-engineer (Dara) — Status atualizado para Ready | @data-engineer (Dara) |
| 2026-08-22 | 0.3.0 | Validated GO (9/10) — Status permanece Ready após revisão do schema | @po (Pax) |
| 2026-08-22 | 1.0.0 | Implementação completa do domínio apps/service_orders, modelo, validações, testes, OpenAPI e docs — Status atualizado para Ready for Review | @dev (Dex) |

---

## Dev Agent Record

### Agent Model Used

Gemini 3.7 Flash

### Debug Log References

- `python manage.py makemigrations service_orders` gerou a migration inicial `0001_initial.py`.
- `python manage.py migrate` aplicou com sucesso a migration `service_orders.0001_initial`.
- `python manage.py test` executou 39 testes automatizados com 100% de aprovação (10 testes específicos da Story 3.1).
- `python manage.py spectacular --validate` confirmou conformidade com a especificação OpenAPI 3.0.
- `python -m ruff check .` e `python -m ruff format --check .` passaram com 0 erros e 55 arquivos formatados.

### Completion Notes List

- Criado o app de domínio `apps/service_orders` registrado em `INSTALLED_APPS`.
- Criado o modelo `ServiceOrder` com FKs `Customer` e `Equipment` com `on_delete=models.PROTECT`, constraints de integridade para orçamento e status, e índices (`so_status_idx`, `so_customer_status_idx`, `so_created_at_desc_idx`).
- Implementado serializer de validação `ServiceOrderInputSerializer` com validação de pertencimento do equipamento ao cliente informado e obrigatoriedade da descrição.
- Implementado serializer de apresentação `ServiceOrderSerializer` com status inicial `recebido`.
- Implementada view protegida `ServiceOrderCreateView` e rota `POST /api/service-orders/` com autenticação por token (`TokenAuthentication` e `IsAuthenticated`).
- Implementada suíte completa de testes automatizados com `APITestCase` cobrindo cenários válidos, inválidos, consistência de relacionamento, ausência de token e representação em string.
- Atualizado `README.md` com exemplo de chamada autenticada via cURL e documentação de resposta.

### File List

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `apps/service_orders/__init__.py` | Novo | Inicialização do pacote de ordens de serviço |
| `apps/service_orders/apps.py` | Novo | Configuração da app Django de ordens |
| `apps/service_orders/admin.py` | Novo | Configuração do modelo no admin |
| `apps/service_orders/migrations/__init__.py` | Novo | Inicialização do pacote de migrations |
| `apps/service_orders/migrations/0001_initial.py` | Novo | Migration inicial da tabela `service_orders` |
| `apps/service_orders/models.py` | Novo | Modelo `ServiceOrder` e relacionamentos |
| `apps/service_orders/serializers.py` | Novo | Validação e serialização da abertura da ordem |
| `apps/service_orders/views.py` | Novo | Endpoint protegido de criação |
| `apps/service_orders/urls.py` | Novo | Rota `/api/service-orders/` |
| `apps/service_orders/tests.py` | Novo | Testes automatizados da abertura |
| `config/settings.py` | Modificado | Registro de `apps.service_orders` |
| `config/urls.py` | Modificado | Inclusão da rota de ordens de serviço |
| `README.md` | Modificado | Documentação e exemplo autenticado da API |
| `docs/stories/story-3.1-abertura-de-ordem-de-servico.md` | Modificado | Atualização de tarefas, status e Dev Agent Record |

---

## QA Results

_A ser preenchido pelo agente de QA após a implementação._
