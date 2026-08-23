# Story 3.2: Atualização do diagnóstico e do andamento

> **Status:** Ready for Review  
> **Épico:** 3 — Ordens de serviço e acompanhamento  
> **Executor:** @dev  
> **Quality gate:** @architect  
> **Quality gate tools:** Validação do contrato OpenAPI, testes automatizados de atualização, validação de status e orçamento  
> **Branch sugerida:** `feature/3.2-atualizacao-do-diagnostico-e-do-andamento`

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - "Validação do contrato OpenAPI"
  - "Testes automatizados de atualização parcial"
  - "Validação de status e orçamento não negativo"
```

---

## História

**Como** técnico da assistência técnica,  
**quero** atualizar o status, o diagnóstico, o orçamento e as observações da ordem,  
**para** registrar o andamento do conserto.

### Contexto e valor

Esta é a segunda story do **Épico 3**. A Story 3.1 já permite abrir uma ordem vinculada a um cliente e a um equipamento, com status inicial `recebido`. Agora o técnico precisa registrar a evolução do atendimento sem alterar os vínculos originais da ordem.

Esta story cobre somente a atualização parcial da ordem existente. Consulta, listagem, filtros e encerramento ficam para a Story 3.3. Não criar histórico detalhado de alterações de status, regras de autorização por papel ou novas camadas de serviço.

**Fontes:** [docs/prd.md — Story 3.2](../../docs/prd.md#story-32-atualização-do-diagnóstico-e-do-andamento), [docs/architecture.md — Fluxo 3](../../docs/architecture.md#fluxo-3--atualização-e-encerramento-do-conserto), [docs/architecture.md — Especificação REST/OpenAPI](../../docs/architecture.md#especificação-restopenapi), [docs/architecture/schema-service-orders.md](../architecture/schema-service-orders.md)

---

## Critérios de aceite

1. [ ] Um usuário autenticado deve conseguir atualizar uma ordem existente por `PATCH /api/service-orders/{id}/`.
2. [ ] A API deve retornar HTTP 404 em JSON quando o identificador da ordem não existir.
3. [ ] A atualização deve ser parcial e aceitar somente os campos desta story: `status`, `diagnosis`, `estimated_budget` e `notes`.
4. [ ] A atualização não deve alterar `customer_id`, `equipment_id` ou `problem_description` da ordem criada na Story 3.1.
5. [ ] `status`, quando informado, deve aceitar somente `recebido`, `em_diagnostico`, `aguardando_aprovacao`, `em_conserto`, `pronto`, `entregue` ou `cancelado`.
6. [ ] `diagnosis` e `notes` devem poder ser atualizados como campos opcionais, respeitando os tipos e a possibilidade de valor nulo definida no modelo.
7. [ ] `estimated_budget`, quando informado, deve aceitar somente valor numérico válido maior ou igual a zero, rejeitando valores negativos.
8. [ ] Status, orçamento ou payload inválidos devem retornar HTTP 400 em JSON consistente e não devem persistir a alteração inválida.
9. [ ] Quando a atualização for válida, a API deve retornar HTTP 200 com a ordem atualizada, incluindo identificador, referências, problema, status, campos de andamento e timestamps.
10. [ ] A rota deve exigir `Authorization: Token <token>` e retornar HTTP 401 para requisições sem autenticação válida.
11. [ ] O contrato OpenAPI deve documentar o `PATCH /api/service-orders/{id}/`, a segurança `TokenAuth`, o schema `ServiceOrder` e o enum `ServiceOrderStatus`.
12. [ ] Devem existir testes automatizados para atualização válida, atualização parcial, campos imutáveis, status inválido, orçamento inválido, ordem inexistente e autenticação.

### Limites explícitos

- Não implementar listagem, filtros, consulta detalhada ou encerramento nesta story; essas responsabilidades pertencem à Story 3.3.
- Não criar uma matriz de transição de status, pois o PRD define os valores permitidos, mas não define regras de sequência entre eles.
- Não implementar histórico de status, notificações, permissões por papel, pagamentos ou integrações externas.
- Não criar migration nova se a implementação usar os campos já existentes no modelo `ServiceOrder`. Caso o modelo seja alterado, a migration correspondente deverá ser criada e validada.

---

## Pré-condições

- [x] Story 3.1 concluída com o modelo `ServiceOrder`, migration inicial e endpoint de criação.
- [x] O app `apps/service_orders` está registrado no projeto Django.
- [x] A autenticação por token e o formato de erros JSON já estão disponíveis.
- [x] O contrato arquitetural do endpoint `PATCH /api/service-orders/{id}/` está aprovado.

---

## Integração com CodeRabbit

> **CodeRabbit Integration**: Disabled
>
> CodeRabbit CLI não está habilitado em `core-config.yaml`.
> A validação de qualidade será feita por revisão manual e pelos quality gates definidos nesta story.
> Para habilitar, defina `coderabbit_integration.enabled: true` em `core-config.yaml`.

### Análise do tipo de story

- **Tipo principal:** API.
- **Tipo secundário:** nenhum.
- **Complexidade:** Média — altera endpoint, serializer, resposta, testes e contrato OpenAPI dentro de um único app de domínio.
- **Agentes principais:** @dev para implementação; @qa para validação dos critérios; @architect como quality gate do contrato.
- **Apoio:** @devops somente para versionamento e Pull Request após o gate de QA.

---

## Tarefas / Subtarefas

- [x] **Implementar a atualização parcial da ordem** (AC: 1, 3, 4, 9)
  - [x] Adicionar operação `PATCH` em `apps/service_orders/views.py` para `/api/service-orders/{id}/`.
  - [x] Buscar a ordem pelo identificador e retornar 404 JSON quando não existir.
  - [x] Usar atualização parcial, sem permitir alteração de cliente, equipamento ou descrição do problema.
  - [x] Retornar a representação completa da ordem com HTTP 200.
- [x] **Implementar validações do andamento** (AC: 5, 6, 7, 8)
  - [x] Validar status contra `ServiceOrderStatus.choices`.
  - [x] Validar orçamento não negativo conforme o campo e a constraint existentes.
  - [x] Aceitar atualização dos campos `diagnosis`, `estimated_budget` e `notes` conforme o modelo.
  - [x] Preservar a ordem no banco quando a validação falhar.
- [x] **Preservar autenticação e consistência de respostas** (AC: 1, 8, 10)
  - [x] Exigir `TokenAuthentication` e `IsAuthenticated`.
  - [x] Manter respostas 400, 401 e 404 em JSON no padrão `detail`/`errors`.
- [x] **Atualizar o contrato OpenAPI** (AC: 11)
  - [x] Documentar `PATCH /api/service-orders/{id}/` com request, respostas 200/400/401/404 e `TokenAuth`.
  - [x] Garantir que o contrato use `ServiceOrderStatus`, conforme a correção já aplicada na Story 3.1.
- [x] **Criar testes automatizados** (AC: 2, 5, 6, 7, 8, 10, 12)
  - [x] Usar `APITestCase` em `apps/service_orders/tests.py` e banco de testes isolado.
  - [x] Testar atualização completa válida e atualização de apenas um campo.
  - [x] Confirmar que cliente, equipamento e descrição permanecem inalterados.
  - [x] Testar status inválido, orçamento negativo, ordem inexistente e ausência de token.
  - [x] Confirmar ausência de persistência para payload inválido.
- [x] **Validar a entrega** (AC: 11, 12)
  - [x] Executar `python manage.py check`.
  - [x] Executar `python manage.py test`.
  - [x] Executar `python manage.py makemigrations --check --dry-run`.
  - [x] Executar `python manage.py spectacular --validate`.
  - [x] Executar `python -m ruff check .` e `python -m ruff format --check .`.
  - [x] Atualizar o README com exemplo autenticado de `PATCH`, se o padrão da documentação exigir a operação.

---

## Dev Notes

### Contexto das stories anteriores

- A Story 3.1 criou `ServiceOrder` no app `apps/service_orders`, com `customer`, `equipment`, `problem_description`, `status`, `diagnosis`, `estimated_budget`, `notes`, `created_at` e `updated_at`.
- A Story 3.1 definiu o status inicial como `recebido` e validou que o equipamento pertence ao cliente informado.
- A atualização desta story deve preservar os vínculos e a descrição originais da ordem.

### Modelo e regras de dados

- O modelo `ServiceOrder` possui os campos de andamento `status`, `diagnosis`, `estimated_budget` e `notes`; `diagnosis`, `estimated_budget` e `notes` são opcionais. [Fonte: docs/architecture/schema-service-orders.md#3-blueprint-do-modelo-django]
- Os status técnicos são `recebido`, `em_diagnostico`, `aguardando_aprovacao`, `em_conserto`, `pronto`, `entregue` e `cancelado`. [Fonte: docs/architecture.md#ordem-de-serviço]
- O banco possui constraint para impedir orçamento negativo e constraint para limitar os valores de status. [Fonte: docs/architecture/schema-service-orders.md#22-constraints-de-integridade]
- A ordem mantém referências protegidas para cliente e equipamento; esta story não altera esses relacionamentos. [Fonte: docs/architecture/schema-service-orders.md#21-estratégia-de-deleção-on_delete]

### API e autenticação

- O endpoint de atualização é `PATCH /api/service-orders/{id}/`, protegido por `TokenAuth`, e retorna a ordem atualizada com HTTP 200. [Fonte: docs/architecture.md#especificação-restopenapi]
- A atualização usa `PATCH` para permitir alterações parciais. [Fonte: docs/architecture.md#observações-do-contrato]
- Operações de negócio exigem `Authorization: Token <token>`. Erros de validação retornam 400, token ausente ou inválido retorna 401 e recurso inexistente retorna 404. [Fonte: docs/architecture.md#padrões-de-resposta]
- A validação deve ocorrer nos serializers, na borda da API, antes da persistência. [Fonte: docs/architecture.md#padrões-de-código]

### Estrutura do projeto

- Manter a implementação no app de domínio `apps/service_orders/`, junto de `models.py`, `serializers.py`, `views.py`, `urls.py` e `tests.py`. [Fonte: docs/architecture.md#estrutura-de-pastas]
- `config/` deve permanecer apenas como composição e configuração da aplicação; regras de negócio ficam em `apps/service_orders/`. [Fonte: docs/architecture.md#decisões-da-estrutura]
- Não criar `repositories/`, `services/`, `use_cases/`, filas ou novos apps para esta atualização. [Fonte: docs/architecture.md#limites-da-estrutura]

### Testes

- Usar `APITestCase` e o Django Test Runner, com banco de testes criado e destruído automaticamente. [Fonte: docs/architecture.md#testes-de-api-e-integração]
- Cobrir sucesso autenticado, token ausente, recurso inexistente, payload inválido e orçamento inválido. [Fonte: docs/architecture.md#testes-de-api-e-integração]
- Manter os testes em `apps/service_orders/tests.py`, próximos ao domínio. [Fonte: docs/architecture.md#tipos-e-organização]
- Não criar testes E2E, containers, banco externo, testes de carga ou factories nesta story. [Fonte: docs/architecture.md#limites-contra-overengineering]

### Restrições técnicas

- Usar Django REST Framework, Django ORM e chamadas síncronas dentro do monólito modular existente. [Fonte: docs/architecture.md#padrões-arquiteturais-e-de-design]
- Não adicionar dependências novas sem requisito claro. [Fonte: docs/architecture.md#segurança-de-dependências]
- Não versionar segredos, tokens, senhas ou arquivos `.env` reais. [Fonte: docs/architecture.md#gerenciamento-de-segredos]

### Project Structure Notes

- O arquivo `docs/architecture/unified-project-structure.md` não existe neste workspace. A estrutura foi validada contra a seção `Estrutura de pastas` de `docs/architecture.md` e contra os arquivos reais das stories concluídas.
- Não há conflito estrutural identificado para esta story.

---

## Testes

Os testes devem ser adicionados ou ajustados em `apps/service_orders/tests.py` com `APITestCase`. O conjunto mínimo inclui:

1. Atualização válida de status, diagnóstico, orçamento e observações com HTTP 200.
2. Atualização parcial de somente um campo, preservando os demais.
3. Tentativa de alterar `customer_id`, `equipment_id` ou `problem_description` não altera esses campos.
4. Status fora do enum retorna 400 e não persiste.
5. Orçamento negativo retorna 400 e não persiste.
6. Ordem inexistente retorna 404.
7. Requisição sem token retorna 401.
8. O schema OpenAPI contém o endpoint PATCH, `ServiceOrder`, `ServiceOrderStatus` e `TokenAuth`.

---

## Lista de arquivos planejada

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `apps/service_orders/serializers.py` | Modificado | Validação e serialização da atualização parcial |
| `apps/service_orders/views.py` | Modificado | Operação PATCH protegida |
| `apps/service_orders/urls.py` | Modificado | Rota por identificador da ordem, se necessário |
| `apps/service_orders/tests.py` | Modificado | Testes da atualização e validações |
| `README.md` | Modificado | Exemplo autenticado de atualização, se aplicável |
| `docs/stories/story-3.2-atualizacao-do-diagnostico-e-do-andamento.md` | Modificado | Registro do desenvolvimento e da validação |

Não se espera alteração de `models.py` ou migration nesta story, pois os campos necessários já fazem parte do modelo aprovado. Se isso mudar durante a implementação, o @dev deverá registrar a justificativa e a migration correspondente no Dev Agent Record.

---

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 2026-08-23 | 0.1.0 | Criação da Story 3.2 com base no PRD e na arquitetura aprovada | @sm (River) |
| 2026-08-23 | 0.2.0 | Validated GO (8/10) — Status: Draft → Ready; recomendada confirmação do schema de request PATCH pelo @architect | @po (Pax) |
| 2026-08-23 | 1.0.0 | Implementação da atualização parcial de ordens de serviço (PATCH), testes e documentação — Status: Ready for Review | @dev (Dex) |

---

## Dev Agent Record

### Agent Model Used

Gemini 3.7 Flash

### Debug Log References

- Nenhum erro de execução ou bloqueio encontrado.
- Suíte completa de 47 testes executada e aprovada com sucesso (`Ran 47 tests in 57.8s OK`).
- Validação do schema OpenAPI 3.0.3 concluída com sucesso via `drf-spectacular`.

### Completion Notes List

- **Implementação:**
  - Criado `ServiceOrderUpdateInputSerializer` em `apps/service_orders/serializers.py` validando `status` (contra `ServiceOrderStatus.choices`), `diagnosis`, `estimated_budget` (não negativo via `min_value=Decimal("0.00")`) e `notes`.
  - Criada `ServiceOrderDetailView` em `apps/service_orders/views.py` com suporte à operação `PATCH /api/service-orders/{id}/`, autenticação `TokenAuthentication` e permissão `IsAuthenticated`.
  - Configurada rota `<int:pk>/` em `apps/service_orders/urls.py` com o nome `service-order-detail`.
  - Imutabilidade garantida: campos `customer_id`, `equipment_id` e `problem_description` são ignorados no PATCH e permanecem inalterados.
- **Documentação e Contrato:**
  - OpenAPI 3.0 documentado com schema `PatchedServiceOrderUpdateInput`, `ServiceOrder`, `ServiceOrderStatus` e segurança `TokenAuth`.
  - `README.md` atualizado com exemplos de cURL e JSON de retorno do endpoint de atualização parcial.
- **Testes Automatizados:**
  - 8 novos testes adicionados em `apps/service_orders/tests.py` cobrindo atualização completa, parcial, campos imutáveis, status inválido, orçamento negativo, ordem inexistente (404), sem token (401), campos nulos e conformidade do OpenAPI schema.

### File List

- `apps/service_orders/serializers.py` (Modificado: adição de `ServiceOrderUpdateInputSerializer`)
- `apps/service_orders/views.py` (Modificado: adição de `ServiceOrderDetailView` com operação `PATCH`)
- `apps/service_orders/urls.py` (Modificado: inclusão do padrão `<int:pk>/` para `service-order-detail`)
- `apps/service_orders/tests.py` (Modificado: 8 novos testes automatizados da Story 3.2)
- `README.md` (Modificado: documentação do endpoint `PATCH /api/service-orders/{id}/`)
- `docs/stories/story-3.2-atualizacao-do-diagnostico-e-do-andamento.md` (Modificado: atualização do status, checklist de tarefas, change log e Dev Agent Record)

---

## QA Results

_A ser preenchido pelo @qa após a implementação._
