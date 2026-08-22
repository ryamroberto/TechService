# AGENTS.md - TechService Workspace

Este arquivo instrui os agentes e executores (Antigravity e Codex CLI) a acessar a inteligência e os agentes do AIOX diretamente do runtime global sem duplicar arquivos.

## Runtime Global AIOX
- **Caminho do Core:** `C:\Users\User\.aiox-core`
- **Constitution:** `C:\Users\User\.aiox-core\constitution.md`
- **Agentes:** `C:\Users\User\.aiox-core\development\agents`
- **Squads:** `C:\Users\User\.aiox-core\.codex\squads` e `C:\Users\User\.aiox-core\.antigravity\squads`

## Atalhos de Agentes (Personas)
Ao acionar qualquer um dos atalhos abaixo, carregue a fonte de verdade em `C:\Users\User\.aiox-core\development\agents\<agente>.md`, renderize a saudação e adote a persona até `*exit`:

- `@architect` -> `C:\Users\User\.aiox-core\development\agents\architect.md`
- `@dev` -> `C:\Users\User\.aiox-core\development\agents\dev.md`
- `@qa` -> `C:\Users\User\.aiox-core\development\agents\qa.md`
- `@pm` -> `C:\Users\User\.aiox-core\development\agents\pm.md`
- `@po` -> `C:\Users\User\.aiox-core\development\agents\po.md`
- `@sm` -> `C:\Users\User\.aiox-core\development\agents\sm.md`
- `@analyst` -> `C:\Users\User\.aiox-core\development\agents\analyst.md`
- `@devops` -> `C:\Users\User\.aiox-core\development\agents\devops.md`
- `@data-engineer` -> `C:\Users\User\.aiox-core\development\agents\data-engineer.md`
- `@ux-design-expert` -> `C:\Users\User\.aiox-core\development\agents\ux-design-expert.md`
- `@squad-creator` -> `C:\Users\User\.aiox-core\development\agents\squad-creator.md`
- `@aiox-master` -> `C:\Users\User\.aiox-core\development\agents\aiox-master.md`

## Regras de Execução
1. Mantenha o diretório deste projeto limpo; resolva todas as dependências de framework contra `C:\Users\User\.aiox-core`.
2. Siga as diretrizes da Constituição AIOX.
3. Não invente requisitos fora dos artefatos do projeto.
