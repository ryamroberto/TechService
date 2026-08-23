# TechService API — Documento de Requisitos do Produto (PRD)

> Status: Pronto para arquitetura  
> Versão: 0.7  
> Data: 22/08/2026  
> Tipo de projeto: Projeto de portfólio para desenvolvedor freelancer júnior

## Objetivos e Contexto

### Objetivos

- Centralizar as informações de clientes, equipamentos e ordens de serviço de uma pequena assistência técnica.
- Permitir que a equipe acompanhe um conserto desde a entrada até a entrega usando poucos status claros.
- Registrar o diagnóstico, o orçamento e as observações relacionadas a cada ordem de serviço.
- Entregar uma API REST documentada que demonstre conhecimentos práticos de Python, Django e Django REST Framework.
- Manter o projeto pequeno o suficiente para ser concluído, testado e explicado por um desenvolvedor júnior.

### Contexto

A TechService API é um sistema proposto para pequenas assistências técnicas que precisam de uma forma básica de organizar clientes, equipamentos e ordens de serviço de celulares, computadores, impressoras e outros aparelhos. A primeira versão será focada no fluxo operacional de receber um equipamento, registrar o problema, acompanhar o status do conserto e finalizar o atendimento.

Ainda não existe um documento inicial do projeto ou documento de pesquisa com usuários. Portanto, o usuário-alvo e o fluxo abaixo são suposições iniciais para validar durante o desenvolvimento: o usuário principal é o atendente ou proprietário da assistência, responsável por cadastrar a ordem de serviço, enquanto o técnico pode atualizar o diagnóstico e as observações do conserto. Este é um MVP voltado para portfólio, não um SaaS multiempresa pronto para produção.

### Limites do MVP

#### Essencial para o MVP

- Cadastro e consulta de clientes.
- Cadastro de equipamentos vinculados a um cliente.
- Criação de ordens de serviço vinculadas a um cliente e equipamento.
- Acompanhamento do status do conserto.
- Registro de diagnóstico, orçamento e observações.
- Autenticação para operações protegidas da API.
- Testes automatizados e documentação da API.

#### Explicitamente fora do escopo do MVP

- Pagamentos, emissão de notas fiscais e documentos fiscais.
- Controle de estoque e gerenciamento de peças.
- Notificações por WhatsApp, e-mail ou SMS.
- Múltiplas empresas, multi-tenancy e cobrança por assinatura.
- Atualizações em tempo real, aplicativo mobile e microsserviços.
- Permissões avançadas, dashboards analíticos e funcionalidades de IA.

### Histórico de alterações

| Data | Versão | Descrição | Autor |
|---|---:|---|---|
| 22/08/2026 | 0.1 | Criação do primeiro rascunho enxuto do PRD | Morgan (PM) |
| 22/08/2026 | 0.2 | Inclusão dos requisitos e das premissas técnicas aprovadas | Morgan (PM) |
| 22/08/2026 | 0.3 | Inclusão da lista de épicos aprovada | Morgan (PM) |
| 22/08/2026 | 0.4 | Aprovação do Épico 1 e detalhamento inicial do Épico 2 | Morgan (PM) |
| 22/08/2026 | 0.5 | Aprovação do Épico 2 e detalhamento inicial do Épico 3 | Morgan (PM) |
| 22/08/2026 | 0.6 | Aprovação do Épico 3 e conclusão da estrutura principal do PRD | Morgan (PM) |
| 22/08/2026 | 0.7 | Execução do checklist do PM e aprovação para a fase de arquitetura | Morgan (PM) |

## Requisitos

### Requisitos funcionais

- **RF1:** O usuário autenticado deve poder cadastrar, consultar, atualizar e listar clientes.
- **RF2:** O usuário deve poder cadastrar equipamentos vinculados a um cliente, informando tipo, marca, modelo e, opcionalmente, um identificador.
- **RF3:** O usuário deve poder criar uma ordem de serviço vinculada a um cliente e a um equipamento existentes.
- **RF4:** A ordem de serviço deve possuir um status entre: recebido, em diagnóstico, aguardando aprovação, em conserto, pronto, entregue ou cancelado.
- **RF5:** O usuário deve poder registrar diagnóstico, orçamento estimado e observações do conserto.
- **RF6:** O usuário deve poder consultar ordens de serviço por cliente e por status.
- **RF7:** A API deve rejeitar ordens de serviço sem cliente, equipamento ou descrição do problema válidos.
- **RF8:** O usuário deve poder consultar os detalhes completos de uma ordem de serviço, incluindo cliente, equipamento, status e informações do conserto.

### Requisitos não funcionais

- **RNF1:** As operações de negócio devem exigir autenticação.
- **RNF2:** A API deve utilizar JSON e respostas HTTP consistentes para sucesso e erro.
- **RNF3:** Os relacionamentos entre clientes, equipamentos e ordens de serviço devem preservar a integridade dos dados.
- **RNF4:** O fluxo principal deve possuir testes automatizados de API.
- **RNF5:** O projeto deve possuir documentação básica de instalação, autenticação e endpoints.
- **RNF6:** Segredos e credenciais não podem ser armazenados diretamente no código-fonte.
- **RNF7:** A aplicação deve ser executável localmente seguindo as instruções do README, sem infraestrutura complexa.

### Critérios para evitar overengineering

1. Toda funcionalidade deve contribuir diretamente para o fluxo de cadastro e acompanhamento de ordens de serviço.
2. O MVP deve utilizar uma aplicação monolítica simples, sem microsserviços, filas ou comunicação em tempo real.
3. O domínio inicial deve permanecer limitado a usuário, cliente, equipamento e ordem de serviço.
4. A autenticação deve ser simples, sem login social, OAuth ou matriz avançada de permissões.
5. Cada funcionalidade deve caber em uma story pequena e ser implementável em uma sessão de desenvolvimento júnior.
6. Integrações externas, pagamentos, notificações e relatórios avançados devem permanecer no backlog futuro.
7. Se uma decisão aumentar significativamente a complexidade sem melhorar o fluxo principal, ela deve ser adiada.

## Premissas técnicas

- **Linguagem:** Python.
- **Framework:** Django com Django REST Framework.
- **Arquitetura:** Monólito simples.
- **Estrutura do repositório:** Um único repositório para a aplicação.
- **Banco de dados local:** SQLite durante o desenvolvimento.
- **Banco de dados futuro:** PostgreSQL somente quando houver necessidade de deploy.
- **Autenticação:** Token simples da DRF, sem login social ou OAuth.
- **Usuários:** Sistema padrão de usuários do Django.
- **Testes:** Testes unitários e testes de API utilizando o `APIClient`.
- **Documentação:** README com instalação, autenticação e endpoints, além de documentação OpenAPI simples.
- **Deploy:** Fora do MVP inicial; a primeira entrega deve funcionar localmente.
- **Infraestrutura:** Sem Docker, Redis, Celery, filas ou microsserviços na primeira versão.

## Lista de épicos

### Épico 1 — Fundação da API e autenticação

Configurar o projeto Django/DRF, criar uma rota de saúde da aplicação, autenticação básica, estrutura inicial de testes e README.

### Épico 2 — Clientes e equipamentos

Permitir o cadastro, consulta e atualização de clientes e equipamentos, mantendo o relacionamento entre eles.

### Épico 3 — Ordens de serviço e acompanhamento

Permitir criar ordens de serviço, atualizar status, registrar diagnóstico, orçamento, observações e consultar ordens por cliente ou status.

## Detalhes do Épico 1 — Fundação da API e autenticação

> Status: Aprovado

### Objetivo do épico

Disponibilizar uma base executável e testável para o TechService API, incluindo uma verificação simples de saúde da aplicação e autenticação para proteger os recursos de negócio. Ao final deste épico, o projeto deve poder ser executado localmente e estar preparado para receber os cadastros de clientes e equipamentos.

### Dependências

- Nenhuma dependência funcional anterior.
- O Épico 2 depende da conclusão deste épico.

### Story 1.1 — Configuração inicial e verificação de saúde

**Como** desenvolvedor do projeto,  
**quero** executar a aplicação e verificar se a API está disponível,  
**para** ter uma base confiável para desenvolver as próximas funcionalidades.

#### Critérios de aceite

1. O projeto deve iniciar localmente seguindo as instruções do README.
2. A API deve disponibilizar uma rota simples de verificação de saúde.
3. A rota de saúde deve responder com sucesso e informar que a aplicação está disponível.
4. Deve existir pelo menos um teste automatizado para a rota de saúde.
5. O README deve explicar como instalar as dependências, preparar o ambiente e executar os testes.

### Story 1.2 — Autenticação de usuários

**Como** usuário autorizado da assistência técnica,  
**quero** me autenticar na API,  
**para** acessar com segurança os recursos de clientes, equipamentos e ordens de serviço.

#### Critérios de aceite

1. Deve existir uma forma documentada de criar um usuário local para acessar a API.
2. Usuários com credenciais válidas devem receber um token de autenticação.
3. Credenciais inválidas devem ser rejeitadas com uma resposta de erro apropriada.
4. Recursos protegidos não devem ser acessíveis sem autenticação.
5. Um token válido deve permitir o acesso aos recursos protegidos.
6. Senhas não podem ser retornadas nas respostas da API nem armazenadas em texto puro.
7. O fluxo de autenticação deve possuir testes automatizados para sucesso e falha.

## Detalhes do Épico 2 — Clientes e equipamentos

> Status: Aprovado

### Objetivo do épico

Permitir que a assistência técnica mantenha os cadastros básicos usados no atendimento: clientes e equipamentos. Ao final deste épico, um usuário autenticado poderá registrar um equipamento vinculado a um cliente e consultar essas informações para abrir futuras ordens de serviço.

### Dependências

- Épico 1 — Fundação da API e autenticação.
- O cliente deve existir antes que um equipamento seja cadastrado.
- O Épico 3 depende dos cadastros deste épico.

### Story 2.1 — Cadastro e consulta de clientes

**Como** atendente da assistência técnica,  
**quero** cadastrar e consultar clientes,  
**para** manter os dados necessários para os atendimentos.

#### Critérios de aceite

1. O usuário autenticado deve poder cadastrar um cliente com nome e telefone.
2. O e-mail deve ser opcional, mas validado quando informado.
3. O usuário deve poder listar clientes cadastrados.
4. O usuário deve poder consultar os detalhes de um cliente.
5. O usuário deve poder atualizar os dados de um cliente.
6. A API deve retornar erros claros quando campos obrigatórios forem ausentes ou inválidos.
7. As operações devem possuir testes automatizados de sucesso e falha.

### Story 2.2 — Cadastro de equipamentos vinculados a clientes

**Como** atendente da assistência técnica,  
**quero** cadastrar equipamentos vinculados a um cliente,  
**para** identificar corretamente o aparelho que será atendido.

#### Critérios de aceite

1. O usuário autenticado deve poder cadastrar um equipamento para um cliente existente.
2. O equipamento deve registrar pelo menos tipo, marca e modelo.
3. O identificador do equipamento deve ser opcional para suportar aparelhos sem número de série informado.
4. A API deve impedir o cadastro de equipamento para um cliente inexistente.
5. O usuário deve poder listar e consultar os equipamentos de um cliente.
6. O usuário deve poder atualizar os dados de um equipamento.
7. A descrição do problema deve ser registrada na ordem de serviço, e não no cadastro permanente do equipamento.
8. As operações devem possuir testes automatizados de relacionamento e validação.

## Detalhes do Épico 3 — Ordens de serviço e acompanhamento

> Status: Aprovado

### Objetivo do épico

Implementar o fluxo principal da assistência técnica: abrir uma ordem de serviço para um equipamento, acompanhar o andamento do conserto e registrar as informações necessárias até a entrega ou cancelamento. Ao final deste épico, o MVP terá um fluxo completo e demonstrável de atendimento.

### Dependências

- Épico 1 — Fundação da API e autenticação.
- Épico 2 — Clientes e equipamentos.
- A ordem de serviço deve sempre referenciar um cliente e um equipamento existentes.

### Story 3.1 — Abertura de ordem de serviço

**Como** atendente da assistência técnica,  
**quero** abrir uma ordem de serviço para um equipamento,  
**para** registrar a solicitação de conserto do cliente.

#### Critérios de aceite

1. O usuário autenticado deve poder criar uma ordem de serviço.
2. A ordem deve estar vinculada a um cliente e a um equipamento existentes.
3. O equipamento informado deve pertencer ao cliente selecionado.
4. A descrição do problema deve ser obrigatória.
5. A ordem deve receber automaticamente o status inicial “recebido”.
6. A API deve retornar erro quando o cliente, o equipamento ou a descrição forem inválidos.
7. A criação da ordem deve possuir testes automatizados de sucesso e falha.

### Story 3.2 — Atualização do diagnóstico e do andamento

**Como** técnico da assistência técnica,  
**quero** atualizar o status, o diagnóstico, o orçamento e as observações da ordem,  
**para** registrar o andamento do conserto.

#### Critérios de aceite

1. O usuário autenticado deve poder atualizar uma ordem de serviço existente.
2. O status deve aceitar apenas os valores definidos no PRD.
3. O diagnóstico e as observações devem poder ser atualizados durante o atendimento.
4. O orçamento estimado deve aceitar apenas valores válidos e não negativos.
5. A API deve rejeitar status ou valores inválidos com mensagens claras.
6. O fluxo deve possuir testes automatizados para atualização e validação.

### Story 3.3 — Consulta e encerramento da ordem

**Como** atendente da assistência técnica,  
**quero** consultar e encerrar ordens de serviço,  
**para** acompanhar os atendimentos e saber quais consertos foram finalizados.

#### Critérios de aceite

1. O usuário deve poder consultar os detalhes completos de uma ordem de serviço.
2. O usuário deve poder listar ordens filtrando por cliente e status.
3. O usuário deve poder marcar uma ordem como “entregue” ou “cancelada”.
4. A resposta deve incluir cliente, equipamento, status, diagnóstico, orçamento e observações.
5. Ordens entregues ou canceladas devem continuar disponíveis para consulta.
6. A listagem, os filtros e o encerramento devem possuir testes automatizados.
7. O MVP não precisa manter histórico detalhado de cada alteração de status.

## Relatório do Checklist do PM

> Data da avaliação: 22/08/2026  
> Modo: Análise completa  
> Responsável: Morgan (PM)

### Resumo executivo

- **Completude estimada do PRD:** 82%.
- **Adequação do escopo do MVP:** Adequado — compatível com um projeto júnior de portfólio.
- **Prontidão para arquitetura:** Pronto para o Architect, com pontos de atenção não bloqueadores.
- **Conclusão:** O PRD possui problema, escopo, requisitos, épicos, stories e critérios de aceite suficientes para orientar uma arquitetura inicial. Ainda não deve ser usado diretamente para implementação sem a criação das stories formais pelo `@sm`.

### Análise por categoria

| Categoria | Status | Observações principais |
|---|---|---|
| 1. Definição do problema e contexto | PARCIAL | Problema e usuários estão descritos, mas não há pesquisa, análise competitiva, impacto quantificado ou prazo de sucesso. |
| 2. Definição do escopo do MVP | APROVADO | Funcionalidades essenciais e fora de escopo estão claras e coerentes com um projeto júnior. |
| 3. Requisitos de experiência do usuário | PARCIAL | O fluxo da API aparece nas stories, mas não há jornada formal, matriz de erros ou requisitos de acessibilidade. Não há UI no MVP. |
| 4. Requisitos funcionais | APROVADO | Requisitos são objetivos, testáveis e relacionados às stories e aos épicos. |
| 5. Requisitos não funcionais | PARCIAL | Segurança, testes, documentação e execução local estão cobertos; faltam metas de desempenho, disponibilidade, backup e retenção de dados. |
| 6. Estrutura de épicos e stories | APROVADO | Três épicos sequenciais, dependências claras e critérios de aceite definidos. As stories formais ainda precisam ser criadas pelo `@sm`. |
| 7. Orientação técnica | PARCIAL | Stack e restrições estão definidas; autenticação, documentação OpenAPI e estratégia de deploy precisam de validação do `@architect`. |
| 8. Requisitos cross-functional | PARCIAL | Entidades e relacionamentos estão identificados; não há integrações externas no MVP e os requisitos operacionais ainda são mínimos. |
| 9. Clareza e comunicação | APROVADO | Documento está em pt-BR, versionado, organizado e com histórico de alterações. |

### Problemas por prioridade

#### Bloqueadores

- Nenhum bloqueador impede a criação da arquitetura inicial.

#### Alta prioridade

- Validar com o `@architect` a autenticação por token, a documentação OpenAPI e a estratégia SQLite/PostgreSQL.
- Criar as stories formais com checkboxes, dependências e File List antes de qualquer implementação.
- Definir como o MVP será demonstrado e validado no portfólio.

#### Média prioridade

- Definir métricas simples de sucesso, como conclusão do fluxo cliente → equipamento → ordem → entrega.
- Registrar uma jornada principal do atendente e os principais cenários de erro da API.
- Definir política mínima para dados de contato e exclusão ou preservação de registros.

#### Baixa prioridade

- Adicionar diagrama simples de entidades e fluxo.
- Registrar pesquisa com uma assistência técnica real ou feedback de um usuário.
- Definir melhorias futuras após o MVP.

### Avaliação do MVP

O MVP está bem dimensionado para um desenvolvedor júnior. Ele demonstra autenticação, relacionamentos entre entidades, validação, filtros, testes e documentação sem exigir pagamentos, estoque, notificações ou infraestrutura avançada.

Não há funcionalidade essencial evidente faltando para demonstrar o fluxo principal. O maior risco é adicionar recursos antes de concluir as três entidades centrais: cliente, equipamento e ordem de serviço.

### Prontidão técnica

- **Pontos claros:** Python, Django, Django REST Framework, monólito, SQLite local, testes de API e execução local.
- **Riscos a investigar:** escolha exata do mecanismo de token, formato de erros, documentação OpenAPI, permissões do usuário e eventual deploy em PostgreSQL.
- **Restrições confirmadas:** sem microsserviços, filas, Redis, Docker obrigatório, integrações externas ou frontend no MVP.

### Recomendações

1. Encaminhar este PRD ao `@architect` para elaborar a arquitetura inicial.
2. Pedir ao `@architect` para revisar as premissas técnicas sem aumentar o escopo.
3. Depois da arquitetura, usar o `@sm` para criar as stories formais.
4. Inicializar o repositório Git antes da primeira implementação.
5. Implementar somente após existir uma story aprovada, começando pela Story 1.1.
6. Usar o `@qa` para validar cada story antes de avançar.

### Decisão final

**PRONTO PARA O ARCHITECT** — O PRD e os épicos estão suficientemente completos para a fase de arquitetura. A decisão não autoriza implementação imediata; o código só deve começar depois da arquitetura e da criação das stories formais.

## Próximos passos

1. `@architect`: criar a arquitetura simples da TechService API usando este PRD.
2. `@sm`: transformar os épicos aprovados em stories formais.
3. `@devops`: inicializar Git e preparar a base de trabalho, sem fazer deploy ainda.
4. `@dev`: implementar a primeira story aprovada.
5. `@qa`: executar testes e validar os critérios de aceite.
