---
projeto: TechService API
atualizado_em: 2026-08-26
fonte_de_verdade: docs/prd.md
---

# Backlog de Stories — TechService API

Este backlog registra decisões de planejamento posteriores ao MVP. Os itens abaixo não alteram os requisitos, funcionalidades ou limites do MVP original.

## Resumo

- Stories concluídas: 0 itens neste backlog de acompanhamento.
- Itens bloqueados/adiados: 1.
- Itens não executados no ciclo atual: 1.
- Próxima prioridade: nenhuma; foco atual em portfólio e apresentação do MVP.

## Itens adiados ou fora do ciclo atual

### [STORY-4.2] Story 4.2 — Execução local com Docker

- **Fonte**: PRD, Épico 4; decisão de escopo de 26/08/2026.
- **Prioridade**: 🟢 LOW
- **Esforço**: Não estimado; não agendado.
- **Status**: ⏸️ BLOCKED
- **Responsável**: Não atribuído.
- **Sprint**: Não agendada.
- **Motivo do bloqueio**: Docker não será instalado ou utilizado neste momento por decisão de escopo e limitação de espaço no computador.
- **Descrição**: A configuração Docker permanece como possibilidade futura, mas não faz parte da entrega atual do projeto.
- **Critério para reavaliar**:
  - [ ] Existir uma necessidade real de execução em container.
  - [ ] Haver espaço e ambiente adequados para instalar e validar o Docker.
- **Aceite futuro**: Somente retomar após nova decisão de escopo e nova validação do fluxo pelo `@sm`, `@po`, `@devops` e `@qa`.

---

### [STORY-4.3] Story 4.3 — PostgreSQL opcional e documentação de publicação

- **Fonte**: PRD, Épico 4; decisão de escopo de 26/08/2026.
- **Prioridade**: 🟢 LOW
- **Esforço**: Não estimado; não agendado.
- **Status**: ❌ CANCELLED (ciclo atual)
- **Responsável**: Não atribuído.
- **Sprint**: Não agendada.
- **Descrição**: PostgreSQL opcional e documentação de publicação não serão executados neste momento. SQLite e execução local continuam sendo suficientes para o MVP e para a demonstração do portfólio.
- **Critério para reavaliar**:
  - [ ] Haver necessidade concreta de publicar a API.
  - [ ] Existir uma decisão futura para preparar um ambiente de publicação.
- **Aceite futuro**: Reabrir somente mediante nova decisão registrada no PRD e criação/validação das stories correspondentes.

---

## Observação de ciclo

A Story 4.2 continua com o status `InProgress` no arquivo da story porque seu Quality Gate foi `FAIL`; ela não foi marcada como concluída. O status administrativo da Story 4.2 só poderá ser alterado por uma decisão de ciclo compatível com as regras do projeto, sem atribuir aprovação ao QA.
