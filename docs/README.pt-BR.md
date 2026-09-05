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
| **Intel Hardware Advisor** | Inspecionar um ambiente local de inferência Windows ou Linux e entender o que as evidências disponíveis permitem concluir. | [`intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Pesquisar e citar o arquivo local versionado da documentação oficial do OpenVINO. | [`intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md) |

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

### Intel Docs Reader

Use esta skill quando seu agente precisar de documentação oficial do OpenVINO
sobre APIs, dispositivos, configuração, setup ou limitações documentadas. Ela
usa um cache local e cita a página de origem dos resultados úteis.

## Início rápido

### Instalar para o seu agente

Use o comando da skill que deseja adicionar. O exemplo usa Codex; troque
`codex` por `claude-code` ou outro agente compatível quando necessário.

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-docs-reader -a codex
```

Ou instale as duas skills em um único comando:

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor --skill intel-docs-reader -a codex
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
