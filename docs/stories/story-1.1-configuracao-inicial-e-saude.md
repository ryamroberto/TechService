# Story 1.1: Configuração inicial e verificação de saúde

> **Status:** Done  
> **Épico:** 1 — Fundação da API e autenticação  
> **Executor:** @dev  
> **Quality gate:** @architect  
> **Quality gate tools:** Validação do contrato OpenAPI, revisão de consistência arquitetural  
> **Branch sugerida:** `feature/1.1-configuracao-e-saude`

---

## Executor Assignment

```yaml
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools:
  - "Validação do contrato OpenAPI"
  - "Revisão de consistência arquitetural"
```

---

## História

**Como** desenvolvedor do projeto,  
**quero** executar a aplicação e verificar se a API está disponível por meio de uma rota de saúde,  
**para** ter uma base confiável e testável para desenvolver as próximas funcionalidades.

### Contexto e valor

Esta é a primeira story do TechService API. Ela cria somente a fundação executável do projeto, uma rota pública de health check, a estrutura inicial de testes e o README. Autenticação e recursos de negócio serão tratados em stories posteriores.

**Fonte:** [docs/prd.md — Épico 1 e Story 1.1](../../docs/prd.md#story-11-configuração-inicial-e-verificação-de-saúde)

---

## Critérios de aceite

1. [x] O projeto deve iniciar localmente seguindo as instruções do README.
2. [x] A API deve disponibilizar uma rota simples de verificação de saúde.
3. [x] A rota de saúde deve responder com sucesso e informar que a aplicação está disponível.
4. [x] Deve existir pelo menos um teste automatizado para a rota de saúde.
5. [x] O README deve explicar como instalar as dependências, preparar o ambiente e executar os testes.

### Detalhamento técnico dos critérios

- A rota prevista para a story é `GET /api/health/`, conforme a abordagem recomendada para o Épico 1.
- A rota de saúde deve ser pública e não exigir token.
- O teste deve validar uma resposta HTTP de sucesso e um JSON que informe a disponibilidade da aplicação.
- O README deve usar comandos compatíveis com Python, `venv`, `pip` e `requirements.txt`.

**Fontes:** [docs/architecture/recommended-approach.md — Fase 1](../../docs/architecture/recommended-approach.md#5-plano-de-implementação-em-fases), [docs/architecture.md — Segurança](../../docs/architecture.md#segurança)

---

## Pré-condições

- [x] O `@architect` incluiu `GET /api/health/` na especificação OpenAPI, com resposta `HealthResponse` e acesso público explícito.

---

## 🤖 CodeRabbit Integration

> **CodeRabbit Integration**: Disabled
>
> CodeRabbit CLI is not enabled in `core-config.yaml`.
> Quality validation will use manual review process only.
> To enable, set `coderabbit_integration.enabled: true` in `core-config.yaml`

---

## Tarefas / Subtarefas

- [x] **Preparar o ambiente e as dependências** (AC: 1, 5)
  - [x] Criar `requirements.txt` com as versões aprovadas de Django, Django REST Framework, drf-spectacular e Ruff.
  - [x] Criar `.env.example` sem segredos reais, conforme as regras de configuração do projeto.
  - [x] Não adicionar dependências, Docker ou outra ferramenta que não esteja no Tech Stack aprovado.
- [x] **Criar o scaffold do projeto Django** (AC: 1)
  - [x] Criar `manage.py` e o pacote `config/` com `settings.py`, `urls.py`, `asgi.py` e `wsgi.py`.
  - [x] Configurar Django REST Framework e as aplicações necessárias sem criar um app `core`.
  - [x] Manter a configuração sem regras de negócio.
- [x] **Implementar a rota de saúde** (AC: 2, 3)
  - [x] Criar a view mínima do health check em `config/views.py`.
  - [x] Registrar `GET /api/health/` em `config/urls.py`.
  - [x] Permitir acesso público à rota e retornar JSON indicando que a aplicação está disponível.
- [x] **Criar o teste automatizado** (AC: 4)
  - [x] Criar o teste em `config/tests.py` usando `APITestCase`.
  - [x] Verificar rota, status HTTP de sucesso, payload JSON e ausência de exigência de autenticação.
  - [x] Executar `python manage.py test` e registrar o resultado.
- [x] **Documentar a execução local** (AC: 1, 5)
  - [x] Criar `README.md` com criação do ambiente virtual, instalação, configuração local, execução da API, health check e testes.
  - [x] Manter a documentação em português do Brasil.

---

## Dev Notes

### Contexto da arquitetura

- A aplicação é um monólito modular Django/DRF em um único repositório, sem frontend, filas, microsserviços ou integrações externas.
  - **Fonte:** [docs/architecture.md — Arquitetura de alto nível](../../docs/architecture.md#arquitetura-de-alto-nível)
- O projeto deve usar Python 3.13.15, Django 5.2.17, Django REST Framework 3.16.1, drf-spectacular 0.30.0 e Ruff 0.16.2.
  - **Fonte:** [docs/architecture.md — Tech Stack](../../docs/architecture.md#tech-stack)
- O ambiente local usa `venv`, `pip`, `requirements.txt` e SQLite; Docker e deploy ficam fora do MVP inicial.
  - **Fonte:** [docs/architecture.md — Infraestrutura e deploy](../../docs/architecture.md#infraestrutura-e-deploy)

### Estrutura de arquivos

- O projeto usa `config/` para configurações, URLs principais e composição da aplicação.
- Não criar um app `core` apenas para o health check; a rota é uma preocupação transversal pequena e deve permanecer próxima da configuração nesta story.
- Os testes devem ficar próximos do componente testado; para esta story, `config/tests.py` é o arquivo inicial do teste de saúde.
  - **Fonte:** [docs/architecture.md — Estrutura de pastas](../../docs/architecture.md#estrutura-de-pastas)

### Regras de implementação

- A rota de saúde é pública; operações de negócio protegidas serão implementadas em stories posteriores.
- Não adicionar autenticação, clientes, equipamentos, ordens de serviço ou banco de domínio nesta story.
- Não armazenar segredos no código, no README ou no repositório.
- Os erros e respostas da API devem usar JSON consistente quando houver erro.
  - **Fonte:** [docs/architecture.md — Segurança](../../docs/architecture.md#segurança), [docs/architecture.md — Estratégia de tratamento de erros](../../docs/architecture.md#estratégia-de-tratamento-de-erros)

### Testing / Testes

- Usar Django Test Runner e `APITestCase` do Django REST Framework.
- O teste deve cobrir o caminho feliz da rota e o fato de ela não exigir autenticação.
- Não usar banco externo, fixtures globais, `factory_boy`, containers ou testes end-to-end.
  - **Fonte:** [docs/architecture.md — Estratégia de testes](../../docs/architecture.md#estratégia-de-testes)

### Atualização da dependência de arquitetura

O contrato OpenAPI foi atualizado na arquitetura v1.8. O path `GET /api/health/` está documentado com a resposta `HealthResponse` e `security: []`, portanto a rota permanece pública. O `@dev` deve seguir esse contrato e não alterar decisões de arquitetura por conta própria.

**Fonte:** [docs/architecture.md — Relatório de validação do Architect](../../docs/architecture.md#relatório-de-validação-do-architect)

### Project Structure Notes

A arquitetura define `config/` como projeto Django principal, mas não lista individualmente `config/views.py` e `config/tests.py`. Esses arquivos são uma extensão pequena e localizada para a rota transversal de saúde e seu teste; não introduzem novo app ou camada de negócio.

---

## File List planejada

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `requirements.txt` | Novo | Dependências aprovadas do projeto |
| `.env.example` | Novo | Exemplo de configuração local sem segredos reais |
| `manage.py` | Novo | CLI do Django |
| `config/__init__.py` | Novo | Pacote de configuração |
| `config/settings.py` | Novo | Configurações do Django e DRF |
| `config/urls.py` | Novo | Roteamento principal e health check |
| `config/asgi.py` | Novo | Entrada ASGI |
| `config/wsgi.py` | Novo | Entrada WSGI |
| `config/views.py` | Novo | View mínima do health check |
| `config/tests.py` | Novo | Teste da rota de saúde |
| `README.md` | Novo | Instalação, execução, health check e testes |

---

## Change Log

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 22/08/2026 | 0.1 | Rascunho inicial da Story 1.1 | @sm (River) |
| 22/08/2026 | 0.2 | Alinhamento ao template oficial, PRD e arquitetura aprovada | @sm (River) |
| 2026-08-22 | 0.2.1 | Validation NO-GO — contrato OpenAPI do health check pendente; quality gate alinhado ao template | @po (Pax) |
| 2026-08-22 | 0.3.0 | Validated GO (8/10) — Status: Draft → Ready | @po (Pax) |
| 2026-08-22 | 1.0.0 | Implementação completa da fundação Django/DRF, health check, testes, README e linting | @dev (Dex) |
| 2026-08-22 | 1.0.1 | QA FAIL — escopo de autenticação antecipado, contrato HealthResponse incompleto e dependências não fixadas; Status: Ready for Review → InProgress | @qa (Quinn) |
| 2026-08-22 | 1.0.2 | Correções aplicadas (QA-001 a QA-004): remoção de autenticação antecipada, campos obrigatórios no HealthResponse, fixação de dependências e remoção de fallback de SECRET_KEY; Status: InProgress → Ready for Review | @dev (Dex) |

---

| 2026-08-22 | 1.1.0 | QA CONCERNS - criterios e contrato aprovados; ambiente local usa Python 3.14.7 em vez do Python 3.13.15 definido na arquitetura; Status: Ready for Review -> Done | @qa (Quinn) |

---

## Dev Agent Record

### Agent Model Used

Gemini 3.7 Flash (High) / Antigravity Dex (Builder)

### Debug Log References

- `python manage.py check`: `System check identified no issues (0 silenced).`
- `python manage.py test`: `Ran 2 tests in 0.024s - OK`
- `ruff check .`: `All checks passed!`
- `ruff format --check .`: `18 files already formatted`
- `python manage.py spectacular --validate`: Schema OpenAPI gerado e validado com sucesso, contendo `required: [service, status]` para `HealthResponse`.

### Completion Notes List

- **QA-001:** Removida rota `/api/auth/token/` e `rest_framework.authtoken` de `config/settings.py` e `config/urls.py` (autenticação reservada para a Story 1.2).
- **QA-002:** Criado `HealthResponseSerializer` explícito com `required=True`, gerando `status` e `service` como propriedades obrigatórias no contrato OpenAPI.
- **QA-003:** Fixadas as dependências no `requirements.txt` conforme versões aprovadas no Tech Stack (`Django==5.2.17`, `djangorestframework==3.16.1`, `drf-spectacular==0.30.0`, `ruff==0.16.2`) e atualizado o `README.md`.
- **QA-004:** Removido o fallback hardcoded de `SECRET_KEY` em `config/settings.py`, exigindo a variável de ambiente explicitamente.
- Testes automatizados passando sem falhas e lint 100% limpo.

### File List

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `requirements.txt` | Modificado | Dependências fixadas nas versões aprovadas pela arquitetura |
| `.env.example` | Novo | Exemplo de variáveis de ambiente para desenvolvimento local |
| `manage.py` | Novo | Utilitário CLI padrão do Django |
| `config/__init__.py` | Novo | Inicialização do pacote de configuração |
| `config/settings.py` | Modificado | Configurações do Django/DRF com SECRET_KEY estrita e sem authtoken |
| `config/urls.py` | Modificado | Roteamento restrito a health check e OpenAPI docs |
| `config/asgi.py` | Novo | Configuração ASGI para o servidor |
| `config/wsgi.py` | Novo | Configuração WSGI para o servidor |
| `config/views.py` | Modificado | View com HealthResponseSerializer contendo campos obrigatórios |
| `config/tests.py` | Novo | Testes automatizados com APITestCase para o health check |
| `README.md` | Modificado | Instruções completas de setup, versões e testes |

---

## QA Results

### Review Date: 2026-08-22

### Reviewed By: Quinn (Test Architect)

### Reviewed Revision: working-tree-digest `6ff6e70193a47000c0cd604e2f77d89c79b357962f625696b0f2b153dfb29847`

### Code Quality Assessment

Os critérios funcionais básicos da Story 1.1 estão implementados e os testes automatizados passam. Entretanto, o gate não pode ser aprovado porque a implementação adiciona autenticação antes da Story 1.2, não reproduz integralmente o contrato OpenAPI aprovado para `HealthResponse` e usa dependências abertas em vez das versões aprovadas.

### Refactoring Performed

Nenhum. A QA não alterou o código; os ajustes devem ser feitos pelo @dev para preservar a rastreabilidade da implementação.

### Compliance Check

- Coding Standards: ✓ Ruff passou em `check` e `format --check`.
- Project Structure: ✗ A rota de token e o app `rest_framework.authtoken` antecipam escopo da Story 1.2.
- Testing Strategy: ✓ Dois testes `APITestCase` passam; `manage.py check` também passa.
- All ACs Met: ✗ Os ACs funcionais passam, mas há divergências obrigatórias nas regras técnicas da story e no contrato OpenAPI.

### Improvements Checklist

- [ ] Remover a rota `/api/auth/token/` e `rest_framework.authtoken` desta story; implementar autenticação na Story 1.2.
- [ ] Corrigir `HealthResponse` para que `status` e `service` sejam campos obrigatórios no schema OpenAPI.
- [ ] Fixar no `requirements.txt` as versões aprovadas pela arquitetura: Django 5.2.17, DRF 3.16.1, drf-spectacular 0.30.0 e Ruff 0.16.2.
- [ ] Alinhar o README e o ambiente virtual às versões aprovadas, evitando anunciar Django 6.x e Python 3.14+ nesta story.
- [ ] Remover o fallback de `SECRET_KEY` hardcoded de `config/settings.py`; exigir variável de ambiente para evitar segredo no código.

### Security Review

A rota de health check está pública de forma explícita e não expõe dados sensíveis. Porém, `config/settings.py` possui uma chave secreta fallback hardcoded, e a autenticação foi parcialmente implementada fora da story. Ambos devem ser corrigidos antes de considerar a fundação pronta.

### Performance Considerations

Nenhum problema de performance identificado para o escopo local da story. A rota é simples e os testes terminam rapidamente.

### Files Modified During Review

Nenhum arquivo de código foi modificado durante a revisão.

### Gate Status

Gate: FAIL → `docs/qa/gates/1.1-configuracao-inicial-e-saude.yml`
Risk profile: `docs/qa/assessments/1.1-risk-20260822.md`
NFR assessment: `docs/qa/assessments/1.1-nfr-20260822.md`
CodeRabbit: não executado; integração desativada em `.aiox-core/core-config.yaml`.

### Lifecycle Transition

FAIL: Ready for Review → InProgress (equivalente ao fluxo canônico InReview → InProgress).

### Revalidation Date: 2026-08-22

### Reviewed By: Quinn (Test Architect)

### Reviewed Revision: working-tree-digest `716ca95ee45fd8d81479d6da47606cc221b898a209ce18bae5cfe49ea0c701f7`

### Revalidation Summary

Os quatro achados do QA anterior foram corrigidos pelo @dev. A implementação agora está limitada ao health check e à documentação da API, o contrato OpenAPI gera `status` e `service` como campos obrigatórios, as dependências estão fixadas e `SECRET_KEY` é obrigatória por variável de ambiente.

### Evidence

- `manage.py check`: PASS.
- `manage.py test`: PASS — 2 testes.
- `ruff check .`: PASS.
- `ruff format --check .`: PASS — 18 arquivos formatados.
- `manage.py spectacular --validate`: PASS — `HealthResponse.required` contém `service` e `status`.
- Dependências instaladas no `venv`: Django 5.2.17, DRF 3.16.1, drf-spectacular 0.30.0 e Ruff 0.16.2.

### Remaining Concern

- A arquitetura define Python 3.13.15, mas a máquina disponível possui somente Python 3.14.7. A suíte passou em Python 3.14.7; recomenda-se recriar o `venv` com Python 3.13.15 quando esse runtime estiver disponível.

### Compliance Check

- Coding Standards: ✓ Ruff passou.
- Project Structure: ✓ Não há autenticação nem app de domínio antecipado.
- Testing Strategy: ✓ Testes `APITestCase` passam.
- Acceptance Criteria: ✓ Todos os cinco critérios possuem evidência.
- Security: ✓ Sem fallback de segredo; health check público explicitamente.

### Refactoring Performed

Nenhum. A QA somente atualizou os artefatos de validação.

### Gate Status

Gate: CONCERNS → `docs/qa/gates/1.1-configuracao-inicial-e-saude.yml`
Risk profile: `docs/qa/assessments/1.1-risk-20260822.md`
NFR assessment: `docs/qa/assessments/1.1-nfr-20260822.md`
CodeRabbit: não executado; integração desativada em `.aiox-core/core-config.yaml`.

### Lifecycle Transition

CONCERNS: Ready for Review → Done (equivalente ao fluxo canônico InReview → Done).
