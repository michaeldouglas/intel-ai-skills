# Feature Specification: Localized Skills-First README

**Feature Branch**: `feature/localized-skills-readme`

**Created**: 2026-09-05

**Status**: Ready for implementation

**Input**: User description: "O README deve começar explicando as skills que temos, ter versões em pt-BR e espanhol, e permitir navegar para cada documentação ao clicar em uma bandeira."

## User Scenarios & Testing

### User Story 1 - Descobrir as skills disponíveis (Priority: P1)

Como uma pessoa que chega ao repositório, quero ver primeiro quais skills estão disponíveis e para que servem, para conseguir escolher rapidamente a mais adequada.

**Why this priority**: A página inicial deve comunicar o produto antes de explicar o processo interno do projeto.

**Independent Test**: Abrir o README raiz e confirmar que o catálogo das skills publicadas aparece antes das seções do harness, arquitetura e contribuição, com links funcionais para cada skill.

**Acceptance Scenarios**:

1. **Given** o README raiz aberto, **When** o leitor percorre o conteúdo inicial, **Then** encontra uma seção de skills disponíveis antes da explicação detalhada do harness.
2. **Given** a tabela de skills, **When** o leitor seleciona uma skill, **Then** chega ao `SKILL.md` correspondente em `skills/`.

### User Story 2 - Escolher o idioma da documentação (Priority: P1)

Como uma pessoa que prefere português do Brasil ou espanhol, quero selecionar uma bandeira visível no README principal, para abrir a documentação completa no idioma escolhido.

**Why this priority**: A navegação internacional é o caminho principal solicitado e deve ser descoberta sem procurar nomes de arquivos.

**Independent Test**: Clicar ou abrir os links identificados pelas bandeiras do Brasil e da Espanha e verificar que cada um leva a um documento localizado existente.

**Acceptance Scenarios**:

1. **Given** o README raiz, **When** o leitor visualiza o seletor de idioma, **Then** vê links acessíveis para português do Brasil e espanhol representados por bandeiras.
2. **Given** a documentação pt-BR ou es, **When** o leitor abre o seletor de idioma, **Then** consegue voltar ao README em inglês e alternar para a outra tradução.

### User Story 3 - Usar a documentação localizada (Priority: P2)

Como um leitor que escolheu um idioma, quero encontrar nele o catálogo das skills, instruções básicas de uso e contexto do projeto, para não depender da versão em inglês.

**Why this priority**: A tradução só entrega valor se cobrir o fluxo inicial de descoberta e uso, sem ser apenas um resumo.

**Independent Test**: Abrir cada tradução e verificar a presença das duas skills, seus comandos de uso, o fluxo de contribuição e links de retorno válidos.

**Acceptance Scenarios**:

1. **Given** a documentação em pt-BR ou es, **When** o leitor procura as skills, **Then** encontra as mesmas duas skills publicadas e suas finalidades.
2. **Given** um comando ou link de skill na tradução, **When** o leitor o utiliza, **Then** o caminho relativo aponta para um arquivo existente no repositório.

## Edge Cases

- O teste deve falhar se uma tradução for removida, renomeada ou deixar de estar vinculada ao seletor do README raiz.
- O teste deve detectar referências a skills publicadas que não existam mais no diretório `skills/`.
- Emojis de bandeira devem ter texto alternativo ou rótulo textual para leitores que não renderizam emoji.
- Links relativos devem continuar válidos quando o documento é visualizado no GitHub, não apenas no diretório de origem.

## Requirements

### Functional Requirements

- **FR-001**: O README raiz MUST apresentar as skills publicadas antes das seções que explicam o harness e o processo de engenharia.
- **FR-002**: O catálogo MUST listar `intel-hardware-advisor` e `intel-docs-reader`, com finalidade, público-alvo ou situação de uso e link para o `SKILL.md` correspondente.
- **FR-003**: O README raiz MUST exibir um seletor de idioma com links identificados por bandeiras para português do Brasil e espanhol.
- **FR-004**: A documentação MUST fornecer os arquivos `docs/README.pt-BR.md` e `docs/README.es.md`.
- **FR-005**: Cada documento localizado MUST conter o catálogo das duas skills, instruções essenciais de uso, contexto do projeto, contribuição e links de navegação entre os idiomas.
- **FR-006**: Os links entre documentos, skills e arquivos do repositório MUST ser relativos e apontar para destinos existentes.
- **FR-007**: A validação automatizada MUST verificar a presença dos documentos localizados, das referências de idioma e das referências das skills publicadas.
- **FR-008**: A documentação localizada MUST preservar as fronteiras de segurança, privacidade, evidência e incerteza descritas pelas skills.
- **FR-009**: A documentação MUST mostrar a instalação pelo padrão `npx skills add`, usando `codex` apenas como exemplo e indicando que o destino pode ser substituído por outro agente compatível.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Um leitor encontra o catálogo das skills nos primeiros 40% do README raiz, antes das seções de arquitetura e contribuição.
- **SC-002**: 100% dos links de idioma e das referências diretas às duas skills publicadas passam na validação automatizada.
- **SC-003**: As versões pt-BR e es permitem completar o fluxo de descobrir uma skill e abrir seu `SKILL.md` sem depender de voltar à versão em inglês.
- **SC-004**: A suíte de validação da documentação termina sem falhas em um checkout limpo do repositório.

## Assumptions

- O README raiz permanece em inglês como idioma padrão do projeto.
- `codex` será o exemplo de agente nos comandos de instalação, mas as skills não serão descritas como exclusivas do Codex.
- A pasta `docs/` será usada para documentação humana localizada e poderá receber outros idiomas no futuro.
- A lista atual de skills publicadas é formada por `intel-hardware-advisor` e `intel-docs-reader`.
- A tradução deve acompanhar o conteúdo essencial do README, mas não precisa traduzir nomes próprios, comandos, caminhos ou identificadores técnicos.
- A publicação remota e a abertura de pull request ficam fora desta implementação local.
