# Intel AI Skills

<p align="center"><strong>Skills para agentes, orientadas por evidências, para workloads de Intel AI e OpenVINO.</strong></p>

<p align="center">
  <a href="../README.md">🇺🇸 English</a> ·
  <a href="./README.es.md">🇪🇸 Español</a>
</p>

> **Construa com evidências. Faça deploy com confiança.**

Este repositório publica Agent Skills portáteis para hardware Intel, runtimes
OpenVINO e decisões sobre workloads de IA baseadas em evidências. Comece pelas
skills abaixo; o harness de engenharia e o fluxo de release aparecem depois da
orientação de produto.

## Skills disponíveis

As skills publicadas ficam em [`skills/`](../skills/). Cada uma é
autocontida e pode ser copiada ou instalada sem depender do harness interno.

| Skill | Use quando você precisa | Documentação |
|---|---|---|
| **Intel Hardware Advisor** | Inspecionar um ambiente local de inferência Windows ou Linux e entender o que as evidências disponíveis permitem concluir. | [`skills/intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Pesquisar e citar o arquivo local versionado da documentação oficial do OpenVINO. | [`skills/intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md) |

### Intel Hardware Advisor

Use esta skill para o primeiro diagnóstico de um ambiente de inferência. Ela
faz descoberta somente leitura, separa fatos da plataforma de fatos do runtime,
segue os identificadores de evidência e mantém visíveis os resultados
`unknown`, `unavailable` e `no_decision`.

Ela não instala pacotes, altera drivers, executa benchmarks, varre arquivos
arbitrários nem infere compatibilidade de modelo, latência, throughput,
economia de memória ou suporte a precisão a partir apenas do nome do
dispositivo.

```bash
cd skills/intel-hardware-advisor
python scripts/hardware_probe.py --format text
python scripts/hardware_probe.py --format json
```

Consulte o contrato completo de comportamento e segurança em
[`intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md).

### Intel Docs Reader

Use esta skill quando uma pergunta exigir documentação oficial do OpenVINO
sobre APIs, dispositivos, configuração, setup ou limitações documentadas. O
leitor usa um cache local e informa a página de origem dos resultados úteis.

```bash
cd skills/intel-docs-reader
python scripts/read_openvino_docs.py --query "NPU device"
python scripts/read_openvino_docs.py --query "NPU device" --offline
```

A skill não baixa nada durante a instalação. Se o cache estiver ausente, a
primeira consulta online baixa o arquivo oficial configurado para o cache local
do usuário, fora da skill instalada e do repositório.

Consulte o contrato completo de fontes e limites de versão em
[`intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md).

## Quickstart

### Usar as skills publicadas

Clone o repositório e execute cada skill a partir do seu próprio diretório:

```bash
git clone https://github.com/michaeldouglas/intel-ai-skills.git
cd intel-ai-skills

python skills/intel-hardware-advisor/scripts/hardware_probe.py --format json
python skills/intel-docs-reader/scripts/read_openvino_docs.py --query "NPU device"
```

Para uma validação determinística do hardware, passe um fixture sanitizado ao
hardware advisor. O fixture é uma entrada de teste, não uma dependência de
runtime da skill publicada:

```bash
python skills/intel-hardware-advisor/scripts/hardware_probe.py \
  --fixture path/to/sanitized-fixture.json \
  --format json
```

### Executar o harness de engenharia

O harness valida candidatos antes que eles sejam liberados em `skills/`:

```bash
cd harness
python -m venv .venv
source .venv/bin/activate             # macOS/Linux
# .venv\Scripts\Activate.ps1          # Windows PowerShell

python -m pip install --upgrade pip pytest
python -m pytest -q
```

A suíte determinística foi projetada para rodar sem hardware Intel, OpenVINO,
acesso à internet ou acesso a secrets. Verificações em hardware real são
complementares.

## Por que Intel AI Skills?

Workloads de IA são cada vez mais heterogêneos. O mesmo modelo pode se
comportar de maneiras muito diferentes dependendo do processador, acelerador,
versão do runtime, driver, precisão, orçamento de memória e destino de
deploy.

Intel AI Skills transforma essa complexidade em um fluxo disciplinado:

- **Orientada a hardware** — descobre a plataforma e o runtime local em vez de adivinhar pelo nome do dispositivo.
- **Qualificada por evidências** — separa fatos detectados, documentação oficial, medições, estimativas e inferências.
- **Portátil por design** — mantém as skills de produto independentes do harness interno.
- **Determinística** — faz o mesmo fixture produzir a mesma resposta em cada máquina e pull request.
- **Privacidade primeiro** — coleta apenas o necessário e nunca inspeciona secrets ou arquivos sem relação.
- **Honesta sobre incerteza** — um resultado desconhecido é válido quando a evidência está incompleta, conflitante, desatualizada ou indisponível.

## Como isso é diferente?

```text
Ambiente local
      │
      ▼
Descoberta somente leitura → Fatos + fontes + confiança → Orientação qualificada
      │                                             │
      └────────────────→ Desconhecido continua desconhecido
```

O projeto transforma pesquisa em uma skill distribuível por meio de artefatos
explícitos, fixtures reproduzíveis, testes automatizados, avaliação e revisão.

## Arquitetura

```text
intel-ai-skills/
├── harness/
│   ├── .specify/             # Constituição e memória do projeto Spec Kit
│   ├── candidates/           # Skills em desenvolvimento
│   ├── evaluations/          # Avaliações de recomendação e comportamento
│   ├── fixtures/             # Ambientes sanitizados e reproduzíveis
│   ├── research/             # Pesquisa técnica e evidências versionadas
│   ├── specs/                # Especificações, planos e tarefas
│   └── tests/                # Testes unitários, de contrato e integração
├── skills/                   # Agent Skills revisadas e distribuíveis
├── docs/                     # Documentação localizada
├── .github/workflows/        # Automação de política de branches e qualidade
├── CONTRIBUTING.md           # Fluxo de contribuição e promoção
└── LICENSE                   # Apache License 2.0
```

A separação é intencional:

1. A pesquisa estabelece o que está documentado e o que ainda é desconhecido.
2. O Spec Kit transforma requisitos em design e sequência de tarefas explícitos.
3. As skills candidatas implementam o comportamento de produto no harness.
4. Fixtures e testes tornam o comportamento reproduzível nas plataformas suportadas.
5. Avaliações e revisão de qualidade somente leitura controlam a promoção.
6. Apenas artefatos revisados chegam a `skills/`.

## Fluxo de branches e release

Todo trabalho segue `feature/<nome-kebab-case> → develop → main`:

- Pull requests de features têm como destino `develop`.
- Depois que uma feature entra em `develop`, o GitHub Actions abre ou reutiliza uma PR para `main`.
- A PR de promoção é revisada e integrada manualmente.
- Commits e pushes diretos em `main` não fazem parte do fluxo.

Leia o processo completo em [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Spec Kit + Graphify

O **Spec Kit** transforma uma ideia em especificação, plano, tarefas,
implementação, avaliação e revisão. O **Graphify** fornece navegação localizada
do código por conceitos, relações, caminhos e estrutura entre arquivos.

A sequência esperada é:

```text
Specify → Clarify → Plan → Tasks → Analyze → Implement → Evaluate → Review
```

O índice gerado pelo Graphify é um recurso de engenharia e não substitui
testes ou revisão.

## Contribuição

Ideias, relatórios de bugs, melhorias de evidências, fixtures e novas skills
são bem-vindos. Antes de abrir uma mudança:

1. Crie `feature/<nome-kebab-case>` a partir de `develop`.
2. Siga os artefatos do Spec Kit.
3. Mantenha fixtures sanitizados e reproduzíveis.
4. Execute os testes e avaliações relevantes.
5. Faça o commit local das mudanças pretendidas.
6. Publique a branch e abra a PR contra `develop` somente após a revisão local.

Consulte [`CONTRIBUTING.md`](../CONTRIBUTING.md) e a
[constituição](../harness/.specify/memory/constitution.md) do projeto.

## Licença

Distribuído sob a [Apache License 2.0](../LICENSE).
