# Feature Specification: Intel OpenVINO Installer

**Feature Branch**: `feature/intel-openvino-installer`

**Created**: 2026-09-05

**Status**: Ready for implementation

**Input**: User description: "Criar a skill intel-openvino-installer para escolher, executar e validar a instalação documentada do OpenVINO em diferentes sistemas operacionais e ecossistemas, sem depender da intel-docs-reader."

## User Scenarios & Testing

### User Story 1 - Instalar OpenVINO no ambiente padrão (Priority: P1)

Como uma pessoa que precisa usar OpenVINO, quero que a skill examine meu ambiente,
escolha um método adequado e instale o runtime após minha confirmação, para não
precisar descobrir manualmente os comandos corretos.

**Why this priority**: O fluxo Python em ambiente virtual atende o caso mais comum
e entrega o MVP da skill.

**Independent Test**: Executar a skill com um perfil sanitizado de Windows, Linux
ou macOS, solicitar uma instalação Python e confirmar que ela gera um plano
determinístico, não altera o ambiente durante o planejamento e valida o runtime
quando a execução é autorizada.

**Acceptance Scenarios**:

1. **Given** um sistema suportado com Python disponível, **When** a pessoa pede a instalação do OpenVINO para Python, **Then** a skill detecta o ambiente, recomenda um ambiente virtual e apresenta as ações antes de executá-las.
2. **Given** a pessoa confirma o plano, **When** a instalação termina, **Then** a skill verifica a versão instalada, consegue importar o runtime e relata o resultado com evidências.
3. **Given** a pessoa não confirma o plano, **When** a skill recebe a resposta, **Then** nenhum comando mutável é executado e o plano permanece disponível para revisão.

### User Story 2 - Escolher o método adequado ao ecossistema (Priority: P1)

Como uma pessoa que usa um ecossistema específico, quero instalar OpenVINO por
Pip, Conda, gerenciador do sistema, Docker, npm, vcpkg, Conan ou Yocto quando
apropriado, para que a instalação respeite meu fluxo de desenvolvimento.

**Why this priority**: A documentação oficial oferece métodos diferentes por
plataforma e linguagem; escolher o método errado pode produzir um ambiente
incompatível ou difícil de manter.

**Independent Test**: Fornecer perfis sanitizados para cada método suportado e
confirmar que a skill escolhe apenas um método compatível, informa pré-requisitos
e não mistura comandos de ecossistemas diferentes.

**Acceptance Scenarios**:

1. **Given** Windows com WinGet disponível, **When** a pessoa pede uma instalação do runtime no sistema, **Then** a skill prioriza WinGet ou apresenta o arquivo compactado como alternativa documentada.
2. **Given** Ubuntu, RHEL-like ou openSUSE, **When** a pessoa pede instalação nativa, **Then** a skill seleciona APT, YUM ou Zypper conforme o sistema detectado e informa a versão escolhida.
3. **Given** um projeto Node.js, C++ ou Conda, **When** a pessoa informa esse ecossistema, **Then** a skill seleciona npm, vcpkg/Conan ou Conda, sem substituir o gerenciador do projeto por Pip.
4. **Given** Docker ou Yocto, **When** a pessoa solicita uma instalação para esse destino, **Then** a skill produz o plano específico e não tenta modificar o host como se fosse uma instalação nativa.

### User Story 3 - Instalar componentes opcionais e lidar com falhas (Priority: P2)

Como uma pessoa que precisa de GenAI, integrações de framework ou aceleração,
quero solicitar somente os componentes adicionais necessários e receber um
diagnóstico acionável quando algo falhar.

**Why this priority**: Componentes opcionais têm dependências e métodos próprios;
instalá-los sempre aumentaria o risco e o tamanho do ambiente.

**Independent Test**: Executar cenários com GenAI solicitado, componente ausente,
permissão insuficiente, gerenciador indisponível e driver não configurado, e
confirmar que a skill identifica o bloqueio sem alegar que o hardware ou o
runtime estão prontos.

**Acceptance Scenarios**:

1. **Given** GenAI foi solicitado, **When** o método escolhido suporta o componente, **Then** a skill inclui o pacote correspondente e verifica sua importação ou instalação.
2. **Given** o driver de GPU ou NPU não está pronto, **When** o runtime é instalado, **Then** a skill separa instalação do runtime de prontidão do dispositivo e informa o próximo requisito sem instalar driver automaticamente.
3. **Given** um comando falha por permissão, rede, pacote ou versão, **When** a skill processa o erro, **Then** ela informa a etapa, preserva o diagnóstico sem expor segredos e sugere uma alternativa documentada.

## Edge Cases

- O sistema operacional ou a arquitetura não está na matriz documentada para o método solicitado.
- O usuário pede uma versão de desenvolvimento sem especificar que aceita uma versão não destinada a manutenção.
- O gerenciador escolhido não está instalado, está desatualizado ou aponta para uma fonte incorreta.
- O OpenVINO já está instalado por outro método e a nova instalação pode causar conflito.
- O ambiente é WSL, container ou Yocto e não deve ser tratado como uma instalação nativa comum.
- O usuário solicita GPU/NPU, mas os drivers e componentes adicionais não estão disponíveis.
- A instalação termina, mas `ov.Core` não expõe dispositivos ou o componente opcional não pode ser importado.
- O usuário cancela depois do plano e antes da execução.
- O comando retorna texto contendo tokens, caminhos pessoais ou variáveis sensíveis.

## Requirements

### Functional Requirements

- **FR-001**: A skill MUST detectar sistema operacional, arquitetura, contexto de execução, linguagem/ecossistema solicitado, gerenciadores disponíveis e permissões relevantes antes de escolher um método.
- **FR-002**: A skill MUST suportar os métodos documentados de Pip, arquivos compactados, APT, YUM, Zypper, Conda, Homebrew, WinGet, Docker, npm, vcpkg, Conan e Yocto, além de identificar compilação a partir do código-fonte como caminho avançado.
- **FR-003**: A skill MUST escolher um método principal compatível com o contexto e explicar por que ele foi escolhido, mantendo alternativas documentadas separadas.
- **FR-004**: A skill MUST considerar explicitamente a versão do OpenVINO e MUST avisar quando a versão escolhida for de desenvolvimento, manutenção ou fora do escopo detectado.
- **FR-005**: A skill MUST produzir um plano sem efeitos colaterais antes da execução, incluindo comandos, pacotes, contexto, versão e alterações esperadas.
- **FR-006**: A skill MUST exigir confirmação explícita imediatamente antes de executar operações mutáveis no ambiente.
- **FR-007**: A skill MUST executar somente o método e os componentes confirmados pelo usuário e MUST NOT instalar drivers de GPU/NPU, modificar BIOS, alterar variáveis globais ou executar benchmarks como parte do fluxo padrão.
- **FR-008**: A skill MUST validar a instalação concluída verificando o runtime, a versão, a importação apropriada ao ecossistema e, quando aplicável, a visibilidade do OpenVINO Core e dos componentes opcionais.
- **FR-009**: A skill MUST distinguir instalação do runtime, configuração de driver e compatibilidade do workload, sem transformar a instalação bem-sucedida em uma garantia de suporte ao modelo.
- **FR-010**: A skill MUST classificar falhas por etapa e causa provável, preservar evidências úteis e evitar exibir credenciais, tokens, caminhos pessoais desnecessários ou dumps arbitrários.
- **FR-011**: A skill MUST ser independente da `intel-docs-reader`, do `intel-hardware-advisor`, do harness e de arquivos internos do projeto; referências oficiais podem ser usadas como enriquecimento opcional.
- **FR-012**: A skill MUST funcionar em modo de planejamento sem instalar nada e em modo de execução somente após confirmação explícita.
- **FR-013**: A skill MUST manter instruções e scripts portáveis para Windows, Linux e macOS, sinalizando métodos que exigem Linux, macOS, Windows, container ou sistema embarcado.

### Key Entities

- **Installation Context**: Sistema, arquitetura, ambiente de execução, ecossistema, gerenciadores, permissões e destino da instalação.
- **Installation Method**: Método documentado, escopo de plataforma, versão, pré-requisitos, comandos e alternativas.
- **Installation Plan**: Plano imutável antes da confirmação, contendo ações, pacotes, alterações e verificações previstas.
- **Verification Result**: Evidências pós-instalação, incluindo versão, importação, dispositivos visíveis, componentes opcionais e falhas.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Em 100% dos cenários suportados de planejamento, a skill identifica o contexto e apresenta um único método principal compatível antes de sugerir alternativas.
- **SC-002**: Em 100% dos cenários sem confirmação, nenhum comando mutável é executado.
- **SC-003**: Em 100% dos cenários de instalação concluída, a resposta informa a versão instalada e o resultado da verificação do runtime.
- **SC-004**: A suíte de testes cobre pelo menos um cenário positivo e um cenário de falha para cada família de método suportada, sem depender de rede ou de uma máquina física específica.
- **SC-005**: A skill não expõe valores classificados como secretos ou dados pessoais nos relatórios de planejamento, execução simulada ou falha.
- **SC-006**: A skill permanece utilizável quando a `intel-docs-reader` e o `harness` não estão instalados.

## Assumptions

- A execução real exige que a pessoa solicite a instalação e confirme o plano no momento da alteração.
- A versão atual da documentação local OpenVINO 2026.3 será a base inicial; versões futuras deverão atualizar a tabela de métodos e as referências versionadas.
- Para produção, a skill preferirá uma versão de manutenção quando houver uma alternativa documentada, mas respeitará uma versão explicitamente solicitada.
- A instalação de drivers e componentes de sistema que não pertencem ao pacote OpenVINO ficará fora do fluxo automático inicial.
- A skill poderá recomendar documentação oficial ou a `intel-docs-reader`, mas nenhum desses recursos será obrigatório para planejar, executar ou verificar a instalação básica.
