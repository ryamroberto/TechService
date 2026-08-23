# Story 3.3: Consulta e encerramento da ordem

> **Status:** Done
> **Épico:** 3 — Ordens de serviço e acompanhamento
> **Executor:** @dev
> **Quality gate:** @architect
> **Quality gate tools:** Testes de listagem e filtros, validação do contrato OpenAPI e testes de encerramento
> **Branch sugerida:** `feature/3.3-consulta-e-encerramento-da-ordem`

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - "Testes automatizados de listagem e filtros"
  - "Validação do contrato OpenAPI"
  - "Testes de consulta detalhada e encerramento"
```

---

## História

**Como** atendente da assistência técnica,  
**quero** consultar e encerrar ordens de serviço,  
**para** acompanhar os atendimentos e saber quais consertos foram finalizados.

### Contexto e valor

Esta é a terceira e última story do **Épico 3 (Ordens de serviço e acompanhamento)**. As Stories 3.1 e 3.2 já permitem abrir uma ordem e atualizar seu andamento. Agora o atendente precisa consultar a fila de ordens, localizar atendimentos por cliente ou status, visualizar os dados completos e marcar uma ordem como entregue ou cancelada.

O encerramento deve reutilizar a atualização parcial já definida na Story 3.2, alterando o campo `status` para `entregue` ou `cancelado`. Esta story não cria um endpoint de ação separado nem uma matriz de transição de status.

**Fontes:** [docs/prd.md — Épico 3 e Story 3.3](../../docs/prd.md#story-33-consulta-e-encerramento-da-ordem), [docs/architecture.md — Componentes: Ordens de serviço](../../docs/architecture.md#ordens-de-serviço), [docs/architecture.md — Especificação REST/OpenAPI](../../docs/architecture.md#especificação-restopenapi), [docs/architecture/schema-service-orders.md](../architecture/schema-service-orders.md)

---

## Critérios de aceite

1. [ ] Um usuário autenticado deve conseguir listar ordens de serviço por `GET /api/service-orders/`, recebendo HTTP 200 e uma lista JSON.
2. [ ] A listagem deve aceitar o parâmetro opcional `customer_id` para filtrar ordens de um cliente.
3. [ ] A listagem deve aceitar o parâmetro opcional `status` para filtrar ordens por um status válido do enum `ServiceOrderStatus`.
4. [ ] A API deve permitir combinar os filtros `customer_id` e `status` na mesma consulta.
5. [ ] A listagem sem filtros deve retornar as ordens existentes sem excluir ordens com status `entregue` ou `cancelado`.
6. [ ] Um usuário autenticado deve conseguir consultar uma ordem existente por `GET /api/service-orders/{id}/`, recebendo HTTP 200.
7. [ ] A consulta de uma ordem inexistente deve retornar HTTP 404 em JSON com o formato de erro adotado pela API.
8. [ ] A resposta da listagem e da consulta detalhada deve incluir, conforme o schema `ServiceOrder`, identificador, referências de cliente e equipamento, descrição do problema, status, diagnóstico, orçamento, observações e timestamps.
9. [ ] Um usuário autenticado deve conseguir encerrar uma ordem existente usando `PATCH /api/service-orders/{id}/` com `status: "entregue"` ou `status: "cancelado"`, recebendo HTTP 200 com a ordem atualizada.
10. [ ] Ordens encerradas devem continuar disponíveis para consulta detalhada e listagem, preservando os demais dados registrados.
11. [ ] Todas as operações desta story devem exigir `Authorization: Token <token>` e retornar HTTP 401 quando o token não for fornecido ou for inválido.
12. [ ] Devem existir testes automatizados cobrindo listagem, filtros, consulta detalhada, ordens inexistentes, encerramento, permanência de ordens encerradas e autenticação.

### Limites explícitos

- Não implementar histórico detalhado de alterações de status.
- Não criar endpoint separado como `POST /close/` ou `POST /cancel/`; o encerramento usa o `PATCH` existente da Story 3.2.
- Não criar matriz de transição de status, pois o PRD não define a sequência obrigatória entre os estados.
- Não implementar exclusão de ordens, paginação, busca textual, ordenação configurável ou exportação.
- Não adicionar notificações, pagamentos, estoque, anexos, permissões por papel ou integrações externas.
- Não criar frontend, novos serviços, repositórios, filas ou camadas artificiais.

---

## Pré-condições

- [x] Épico 1 concluído com autenticação por token e proteção das rotas de negócio.
- [x] Épico 2 concluído com os modelos e endpoints de clientes e equipamentos.
- [x] Story 3.1 concluída com o modelo `ServiceOrder` e a criação autenticada de ordens.
- [x] Story 3.2 concluída com a atualização parcial autenticada de ordens.
- [x] O contrato REST/OpenAPI aprovado define `GET /api/service-orders/`, `GET /api/service-orders/{id}/` e o `PATCH` de atualização.

---

## 🤖 CodeRabbit Integration

> **CodeRabbit Integration**: Disabled
>
> **Integração com CodeRabbit: desabilitada**
>
> O CLI do CodeRabbit não está habilitado em `core-config.yaml`.
> A validação de qualidade será feita por revisão manual e pelos quality gates definidos nesta story.
> Para habilitar, defina `coderabbit_integration.enabled: true` em `core-config.yaml`.

### Análise do tipo de story

- **Tipo principal:** API.
- **Tipo secundário:** nenhum.
- **Complexidade:** Média — adiciona listagem, filtros e consulta no app existente, além de cobrir o encerramento pelo PATCH já disponível.
- **Agentes principais:** @dev para implementação; @architect para o quality gate do contrato; @qa para validação dos critérios e dos testes.
- **Apoio:** @devops somente para versionamento e Pull Request após o gate de QA.

---

## Tarefas / Subtarefas

- [x] **Implementar listagem de ordens** (AC: 1, 5, 8)
  - [x] Adicionar `GET /api/service-orders/` no app `apps/service_orders/`.
  - [x] Retornar lista JSON usando a representação `ServiceOrder` já definida.
  - [x] Manter a ordenação padrão do modelo por `-created_at` e `-id`, conforme a arquitetura.
- [x] **Implementar filtros simples** (AC: 2, 3, 4)
  - [x] Filtrar por `customer_id` quando o parâmetro for informado.
  - [x] Filtrar por `status` quando o parâmetro for informado.
  - [x] Rejeitar status de filtro que não pertença ao enum permitido, usando resposta JSON HTTP 400 conforme o padrão da API.
- [x] **Implementar consulta detalhada** (AC: 6, 7, 8, 10)
  - [x] Adicionar ou manter `GET /api/service-orders/{id}/` no roteamento do domínio.
  - [x] Retornar HTTP 200 para ordem existente e HTTP 404 para identificador inexistente.
  - [x] Garantir que ordens `entregue` e `cancelado` permaneçam consultáveis.
- [x] **Implementar encerramento pelo PATCH existente** (AC: 9, 10)
  - [x] Reutilizar a operação `PATCH /api/service-orders/{id}/` da Story 3.2.
  - [x] Cobrir os valores `entregue` e `cancelado` sem criar nova regra de transição.
  - [x] Preservar diagnóstico, orçamento, observações, cliente e equipamento ao alterar somente o status.
- [x] **Preservar autenticação e erros** (AC: 1, 6, 9, 11)
  - [x] Exigir `TokenAuthentication` e `IsAuthenticated` nas operações de negócio.
  - [x] Manter respostas JSON com `detail` e/ou `errors`, conforme o caso.
- [x] **Atualizar o contrato e a documentação** (AC: 1, 2, 3, 6, 9)
  - [x] Documentar listagem, parâmetros `customer_id` e `status`, consulta detalhada e respostas HTTP no OpenAPI.
  - [x] Atualizar o README com exemplos autenticados de listagem, filtro, consulta e encerramento, seguindo o padrão existente.
- [x] **Criar testes automatizados** (AC: 1–12)
  - [x] Usar `APITestCase` e o banco de testes do Django.
  - [x] Testar listagem sem filtros, filtro por cliente, filtro por status e combinação dos filtros.
  - [x] Testar consulta existente e ordem inexistente.
  - [x] Testar encerramento como `entregue` e `cancelado`.
  - [x] Confirmar que ordens encerradas continuam na listagem e na consulta detalhada.
  - [x] Testar ausência de token e status de filtro inválido.
  - [x] Validar o contrato OpenAPI para as rotas e parâmetros da story.
- [x] **Validar a entrega** (AC: 12)
  - [x] Executar `python manage.py check`.
  - [x] Executar `python manage.py test`.
  - [x] Executar `python manage.py makemigrations --check --dry-run`.
  - [x] Executar `python manage.py spectacular --validate`.
  - [x] Executar `python -m ruff check .` e `python -m ruff format --check .`.

---

## Dev Notes

### Contexto das stories anteriores

- A Story 3.1 criou o domínio `apps/service_orders/`, o modelo `ServiceOrder` e a criação autenticada de ordens.
- A Story 3.2 adicionou o `PATCH /api/service-orders/{id}/` para atualização parcial de status, diagnóstico, orçamento e observações.
- Esta story deve reutilizar os padrões existentes de autenticação, erros JSON, testes, OpenAPI e documentação, sem alterar o escopo das stories anteriores.

### Modelo e regras de dados

- O modelo `ServiceOrder` possui `id`, `customer_id`, `equipment_id`, `problem_description`, `status`, `diagnosis`, `estimated_budget`, `notes`, `created_at` e `updated_at`. [Fonte: docs/architecture.md#ordem-de-serviço]
- Os valores de status permitidos são `recebido`, `em_diagnostico`, `aguardando_aprovacao`, `em_conserto`, `pronto`, `entregue` e `cancelado`. [Fonte: docs/architecture/schema-service-orders.md#3-blueprint-do-modelo-django]
- A ordenação padrão das ordens é decrescente por `created_at` e `id`. [Fonte: docs/architecture/schema-service-orders.md#3-blueprint-do-modelo-django]
- Os índices `so_status_idx` e `so_customer_status_idx` existem para apoiar consultas por status e por cliente/status. [Fonte: docs/architecture/schema-service-orders.md#23-estrategia-de-indices]
- Ordens encerradas não devem ser apagadas nesta story; o MVP mantém o registro disponível para consulta. [Fonte: docs/architecture.md#observações-do-contrato]

### API e autenticação

- A listagem deve usar `GET /api/service-orders/` e aceitar `customer_id` e `status` como filtros opcionais. [Fonte: docs/architecture.md#contrato-openapi-proposto]
- A consulta individual deve usar `GET /api/service-orders/{id}/`, retornando `ServiceOrder` ou erro `NotFound`. [Fonte: docs/architecture.md#contrato-openapi-proposto]
- O encerramento deve usar o `PATCH /api/service-orders/{id}/` existente, informando `status` como `entregue` ou `cancelado`. [Fonte: docs/architecture.md#contrato-openapi-proposto]
- Operações de negócio exigem `Authorization: Token <token>`; requisições não autenticadas retornam HTTP 401. [Fonte: docs/architecture.md#convenções-da-api]
- Respostas válidas usam JSON e erros seguem `detail` para mensagens gerais e `errors` para erros de campos quando necessário. [Fonte: docs/architecture.md#padrões-de-resposta]
- Não adicionar paginação, versionamento complexo ou GraphQL no MVP. [Fonte: docs/architecture.md#convenções-da-api]

### Estrutura do projeto

- Manter a implementação no app `apps/service_orders/`, junto de `serializers.py`, `views.py`, `urls.py` e `tests.py`. [Fonte: docs/architecture.md#estrutura-de-pastas]
- `config/` deve permanecer apenas como composição e configuração do projeto; as regras de consulta ficam no domínio de ordens. [Fonte: docs/architecture.md#decisões-da-estrutura]
- Não criar `repositories/`, `services/`, `use_cases/`, filas, workers ou novos apps para esta story. [Fonte: docs/architecture.md#limites-da-estrutura]

### Testes

- Usar `APITestCase` e o Django Test Runner, com banco de testes isolado. [Fonte: docs/architecture.md#testes-de-api-e-integração]
- Cobrir listagem, filtros, consulta, 404, encerramento, autenticação e payload/status inválido. [Fonte: docs/architecture.md#testes-de-api-e-integração]
- Manter os testes próximos ao domínio em `apps/service_orders/tests.py`. [Fonte: docs/architecture.md#tipos-e-organização]
- Não criar testes E2E, containers, banco externo, testes de carga ou factories para esta story. [Fonte: docs/architecture.md#limites-contra-overengineering]

### Restrições técnicas

- Usar Django REST Framework, Django ORM e chamadas síncronas no monólito modular existente. [Fonte: docs/architecture.md#padrões-arquiteturais-e-de-design]
- Não adicionar dependências novas sem requisito claro. [Fonte: docs/architecture.md#segurança-de-dependências]
- Não versionar tokens, senhas, arquivos `.env` reais ou dados de ambiente. [Fonte: docs/architecture.md#gerenciamento-de-segredos]

### Project Structure Notes

- O arquivo `docs/architecture/unified-project-structure.md` não existe neste workspace. A estrutura foi validada contra a seção `Estrutura de pastas` de `docs/architecture.md` e contra os arquivos reais das stories concluídas.
- Não há conflito estrutural identificado para esta story.

---

## Testes

Os testes devem ser adicionados ou ajustados em `apps/service_orders/tests.py` com `APITestCase`. O conjunto mínimo inclui:

1. Listagem autenticada sem filtros.
2. Filtro por `customer_id`.
3. Filtro por `status`.
4. Combinação dos dois filtros.
5. Consulta detalhada de ordem existente.
6. Consulta de ordem inexistente retornando HTTP 404.
7. Encerramento com `status: "entregue"`.
8. Encerramento com `status: "cancelado"`.
9. Permanência de ordens encerradas na listagem e na consulta.
10. Requisição sem token retornando HTTP 401.
11. Status de filtro inválido retornando HTTP 400 sem alterar dados.
12. Contrato OpenAPI contendo listagem, filtros, consulta, PATCH, `ServiceOrder` e `ServiceOrderStatus`.

---

## Lista de arquivos planejada

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `apps/service_orders/serializers.py` | Modificado, se necessário | Reutilização ou ajuste da representação da ordem e validação do filtro/status |
| `apps/service_orders/views.py` | Modificado | Listagem filtrada e consulta detalhada; integração com o PATCH existente |
| `apps/service_orders/urls.py` | Modificado, se necessário | Rotas de listagem e consulta por identificador |
| `apps/service_orders/tests.py` | Modificado | Testes de listagem, filtros, consulta e encerramento |
| `README.md` | Modificado | Exemplos autenticados das novas operações |
| `docs/stories/story-3.3-consulta-e-encerramento-da-ordem.md` | Modificado | Registro da implementação e validação |
| `docs/architecture.md` | Modificado, somente se necessário | Ajuste do contrato OpenAPI caso a implementação revele divergência documentada |

Não se espera alteração de `models.py` ou criação de migration nesta story, pois o modelo e os índices de consulta já foram definidos nas stories anteriores e no schema aprovado.

---

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 2026-08-23 | 0.1.0 | Criação da Story 3.3 com base no PRD e na arquitetura aprovada | @sm (River) |
| 2026-08-23 | 0.1.1 | Validated GO (9/10) — Status: Draft → Ready; quality gate alinhado para @architect | @po (Pax) |
| 2026-08-23 | 1.0.0 | Implementação de listagem, filtros, consulta detalhada e encerramento de ordens de serviço (GET/PATCH), testes e documentação — Status: Ready for Review | @dev (Dex) |
| 2026-08-23 | 1.1.0 | QA Gate PASS — 62 testes, migrations, Ruff e OpenAPI aprovados; Status: Ready for Review → Done | @qa (Quinn) |
| 2026-08-23 | 1.1.1 | Fechamento administrativo após QA PASS; Story permanece Done e o MVP do Épico 3 está concluído. [closure-key: 3.3:commit:4d6be2e91235140b6c203134271f508f34d3939a] | @po (Pax) |

---

## Dev Agent Record

### Agent Model Used

Gemini 3.7 Flash

### Debug Log References

- Nenhum erro de execução ou bloqueio encontrado.
- Suíte completa de 61 testes executada e aprovada com sucesso (`Ran 61 tests in 63.5s OK`).
- Validação do schema OpenAPI 3.0.3 concluída com sucesso via `drf-spectacular`.

### Completion Notes List

- **Implementação:**
  * Atualizada `ServiceOrderListCreateView` em `apps/service_orders/views.py` com o método `GET` ordenado por `-created_at` e `-id`, suportando filtros opcionais `customer_id` e `status` (validado contra `ServiceOrderStatus.values`, rejeitando filtros inválidos com `400 Bad Request`).
  * Atualizada `ServiceOrderDetailView` em `apps/service_orders/views.py` com o método `GET` para consulta detalhada de ordens existentes (`200 OK`) ou `404 Not Found` para identificadores inexistentes.
  * O encerramento de ordens foi validado reutilizando o método `PATCH /api/service-orders/{id}/` existente, com os status `entregue` e `cancelado`.
  * Ordens encerradas permanecem completamente acessíveis tanto na consulta detalhada quanto na listagem.
- **Roteamento & Documentação:**
  * Atualizado `apps/service_orders/urls.py` com as rotas `service-order-list-create` e `service-order-detail`.
  * Atualizado `README.md` com instruções detalhadas de cURL para listagem, filtros, consulta detalhada e encerramento de ordens.
  * OpenAPI 3.0.3 documentado com todos os parâmetros query, schemas de erro, entidades e segurança `TokenAuth`.
- **Testes Automatizados:**
  * Adicionados 13 novos testes em `apps/service_orders/tests.py` cobrindo listagem padrão, filtro por cliente, filtro por status, combinação de filtros, inclusão de ordens encerradas, filtros inválidos (400), consulta detalhada (200/404), encerramento como `entregue` e `cancelado`, autenticação (401) e validação do OpenAPI schema.

### File List

- `apps/service_orders/views.py` (Modificado: adição de `GET` list com filtros e `GET` detail)
- `apps/service_orders/urls.py` (Modificado: suporte a `service-order-list-create` e `service-order-detail`)
- `apps/service_orders/tests.py` (Modificado: 13 novos testes automatizados da Story 3.3)
- `README.md` (Modificado: documentação das novas operações e exemplos de cURL)
- `docs/stories/story-3.3-consulta-e-encerramento-da-ordem.md` (Modificado: checklist de tarefas, change log, Dev Agent Record e status para Ready for Review)

---

## QA Results

### Data da revisão: 2026-08-23

### Revisado por: Quinn (Test Architect)

### Revisão analisada

`commit:4d6be2e91235140b6c203134271f508f34d3939a`

### Avaliação da qualidade

A implementação atende aos 12 critérios da Story 3.3. A API possui listagem autenticada com filtros por cliente e status, consulta detalhada com 404 para ordem inexistente, encerramento via PATCH com `entregue` ou `cancelado` e permanência de ordens encerradas nas consultas.

Foram executados 62 testes na suíte completa e 33 testes no app `service_orders`, todos aprovados. Também passaram Django check, verificação de migrations, Ruff, Ruff format e validação OpenAPI 3.0.3.

### Verificação de conformidade

- Critérios de aceite: 12 de 12 atendidos.
- Listagem: filtros `customer_id`, `status` e combinação dos dois cobertos.
- Consulta: sucesso autenticado e ordem inexistente retornando 404 cobertos.
- Encerramento: status `entregue` e `cancelado` cobertos, mantendo os registros consultáveis.
- Segurança: TokenAuthentication e IsAuthenticated aplicados; ausência de token retorna 401.
- OpenAPI: listagem, filtros, consulta, PATCH, `ServiceOrder`, `ServiceOrderStatus` e `TokenAuth` documentados.
- Migrations: `No changes detected`.
- CodeRabbit: não executado porque está desabilitado em `.aiox-core/core-config.yaml`.

### Recomendação documental

O Dev Agent Record informa 61 testes, enquanto a validação executou 62 testes na suíte completa. Isso não afeta o código ou o gate, mas o registro pode ser atualizado posteriormente para manter a documentação exata.

### NFR Validation

- Segurança: PASS.
- Performance: PASS para filtros simples via Django ORM e o escopo do MVP.
- Confiabilidade: PASS nos cenários de listagem, filtros, consulta, 404, encerramento e autenticação.
- Manutenibilidade: PASS; Ruff, migrations e OpenAPI estão alinhados e não foram adicionadas camadas artificiais.

### Gate Status

- Gate: **PASS** — `docs/qa/gates/3.3-consulta-e-encerramento-da-ordem.yml`
- Score: **100/100**
- Decisão: aprovado.

### Lifecycle Transition

- PASS: Ready for Review → Done.
