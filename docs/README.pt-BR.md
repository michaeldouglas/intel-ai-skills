# Intel AI Skills

<p align="center"><strong>Skills para agentes, orientadas por evidências, para workloads de Intel AI e OpenVINO.</strong></p>

<p align="center">
  <a href="../README.md">🇺🇸 English</a> ·
  <a href="./README.es.md">🇪🇸 Español</a>
</p>

> **Construa com evidências. Faça deploy com confiança.**

Este repositório publica Agent Skills portáteis para hardware Intel, runtimes
OpenVINO e decisões sobre workloads de IA baseadas em evidências. Instale a
skill necessária e deixe seu agente utilizá-la quando a tarefa exigir.

## Skills disponíveis

As skills publicadas ficam em [`skills/`](../skills/). Cada uma é autocontida e
pode ser instalada de forma independente.

| Skill | Use quando você precisa | Documentação |
|---|---|---|
| **Intel Hardware Advisor** | Inspecionar um ambiente local de inferência Windows, Linux ou macOS e entender o que as evidências disponíveis permitem concluir. | [`intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Pesquisar e citar o arquivo local versionado da documentação oficial do OpenVINO. | [`intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md) |
| **Intel OpenVINO Installer** | Escolher, instalar e validar o OpenVINO Runtime com um método documentado para a plataforma e o ecossistema do usuário. | [`intel-openvino-installer/SKILL.md`](../skills/intel-openvino-installer/SKILL.md) |
| **Intel OpenVINO Model Converter** | Converter modelos de frameworks compatíveis para OpenVINO IR com shapes e artefatos explícitos. | [`intel-openvino-model-converter/SKILL.md`](../skills/intel-openvino-model-converter/SKILL.md) |
| **Intel OpenVINO Inference Runner** | Compilar e executar modelos localmente ou em Docker, relatando dispositivos e evidências de compatibilidade. | [`intel-openvino-inference-runner/SKILL.md`](../skills/intel-openvino-inference-runner/SKILL.md) |
| **Intel OpenVINO Benchmark** | Medir latência e throughput reproduzíveis entre configurações do OpenVINO. | [`intel-openvino-benchmark/SKILL.md`](../skills/intel-openvino-benchmark/SKILL.md) |
| **Intel OpenVINO Model Optimizer** | Planejar quantização e compressão de pesos preservando os artefatos originais. | [`intel-openvino-model-optimizer/SKILL.md`](../skills/intel-openvino-model-optimizer/SKILL.md) |
| **Intel OpenVINO Model Server** | Validar deployments locais do OpenVINO Model Server com Docker, repositórios, APIs e health checks. | [`intel-openvino-model-server/SKILL.md`](../skills/intel-openvino-model-server/SKILL.md) |
| **Intel OpenVINO GenAI Runner** | Planejar e validar fluxos GenAI de texto, chat, GGUF, VLM, fala e outros. | [`intel-openvino-genai-runner/SKILL.md`](../skills/intel-openvino-genai-runner/SKILL.md) |

### Intel Hardware Advisor

Use esta skill quando seu agente precisar entender o ambiente local de
inferência antes de escolher um caminho de execução Intel. Ela faz descoberta
somente leitura, separa fatos da plataforma de fatos do runtime, segue os
identificadores de evidência e mantém visíveis os resultados `unknown`,
`unavailable` e `no_decision`.

Ela não instala pacotes, altera drivers, executa benchmarks, varre arquivos
arbitrários nem infere compatibilidade de modelo, latência, throughput,
economia de memória ou suporte a precisão a partir apenas do nome do
dispositivo.

Ela também informa estados leves de configuração de GPU, NPU, GenAI, OpenCV e
contexto de execução; dúvidas detalhadas de suporte e setup ficam com o Docs
Reader versionado.

### Intel Docs Reader

Use esta skill quando seu agente precisar de documentação oficial do OpenVINO
sobre APIs, dispositivos, configuração, setup ou limitações documentadas. Ela
usa um cache local e cita a página de origem dos resultados úteis.

### Intel OpenVINO Installer

Use esta skill quando seu agente precisar escolher, instalar ou validar o
OpenVINO Runtime. Ela seleciona um método documentado para a plataforma e o
ecossistema, mostra os comandos antes da execução, pede confirmação antes de
alterar a máquina e separa a validação da instalação da validação do runtime.

### Skills do fluxo de runtime

Depois que o runtime estiver pronto, use as skills focadas em conversão de
modelos, inferência, benchmark, otimização, validação local do Model Server e
fluxos GenAI. Cada uma executa seu próprio script incluído e mantém escopo
independente.

## Início rápido

### Instalar para o seu agente

Use o comando da skill que deseja adicionar. O exemplo usa Codex; troque
`codex` por `claude-code` ou outro agente compatível quando necessário.

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-docs-reader -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-installer -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-model-converter -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-inference-runner -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-benchmark -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-model-optimizer -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-model-server -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-openvino-genai-runner -a codex
```

Ou instale as nove skills em um único comando:

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor --skill intel-docs-reader --skill intel-openvino-installer --skill intel-openvino-model-converter --skill intel-openvino-inference-runner --skill intel-openvino-benchmark --skill intel-openvino-model-optimizer --skill intel-openvino-model-server --skill intel-openvino-genai-runner -a codex
```

### Usar as skills instaladas

Depois da instalação, peça ao seu agente para inspecionar o hardware ou
responder uma pergunta sobre OpenVINO. A própria skill executa seus scripts
incluídos automaticamente. Você não precisa mudar de diretório nem executar
scripts Python manualmente.

## Por que Intel AI Skills?

Workloads de IA são cada vez mais heterogêneos. O mesmo modelo pode se
comportar de maneiras muito diferentes dependendo do processador, acelerador,
versão do runtime, driver, precisão, orçamento de memória e destino de deploy.

Intel AI Skills transforma essa complexidade em um fluxo disciplinado:

- **Orientada a hardware** — descobre a plataforma e o runtime local em vez de adivinhar pelo nome do dispositivo.
- **Qualificada por evidências** — separa fatos detectados, documentação oficial, medições, estimativas e inferências.
- **Portátil por design** — cada skill publicada é autocontida e independente.
- **Determinística** — faz o mesmo fixture produzir a mesma resposta em cada máquina e pull request.
- **Privacidade primeiro** — coleta apenas o necessário e nunca inspeciona secrets ou arquivos sem relação.
- **Honesta sobre incerteza** — um resultado desconhecido é válido quando a evidência está incompleta, conflitante, desatualizada ou indisponível.

## Como as skills funcionam

```text
Ambiente local ou pergunta sobre OpenVINO
                  │
                  ▼
O agente invoca a skill instalada e seus scripts incluídos
                  │
                  ▼
Fatos + fontes + confiança → Orientação qualificada
```

## Segurança e evidências

As skills são projetadas para descoberta somente leitura quando essa função é
necessária. Elas separam fatos detectados, documentação oficial, medições,
estimativas e inferências. Evidências desconhecidas, indisponíveis ou
conflitantes continuam visíveis em vez de serem substituídas por suposições.

## Licença

Distribuído sob a [Apache License 2.0](../LICENSE).
