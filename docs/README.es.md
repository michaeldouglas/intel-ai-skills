# Intel AI Skills

<p align="center"><strong>Skills para agentes, basadas en evidencia, para cargas de trabajo de Intel AI y OpenVINO.</strong></p>

<p align="center">
  <a href="../README.md">🇺🇸 English</a> ·
  <a href="./README.pt-BR.md">🇧🇷 Português (Brasil)</a>
</p>

> **Construye con evidencia. Despliega con confianza.**

Este repositorio publica Agent Skills portátiles para hardware Intel, runtimes
OpenVINO y decisiones sobre cargas de IA basadas en evidencia. Empieza por las
skills siguientes; el harness de ingeniería y el flujo de release aparecen
después de la orientación de producto.

## Skills disponibles

Las skills publicadas están en [`skills/`](../skills/). Cada una es
autocontenida y puede copiarse o instalarse sin depender del harness interno.

| Skill | Úsala cuando necesites | Documentación |
|---|---|---|
| **Intel Hardware Advisor** | Inspeccionar un entorno local de inferencia Windows o Linux y entender qué permiten concluir las evidencias disponibles. | [`skills/intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Buscar y citar el archivo local versionado de la documentación oficial de OpenVINO. | [`skills/intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md) |

### Intel Hardware Advisor

Usa esta skill para el diagnóstico inicial de un entorno de inferencia. Hace
descubrimiento de solo lectura, separa los hechos de la plataforma de los del
runtime, sigue los identificadores de evidencia y mantiene visibles los
resultados `unknown`, `unavailable` y `no_decision`.

No instala paquetes, cambia drivers, ejecuta benchmarks, recorre archivos
arbitrarios ni infiere compatibilidad de modelos, latencia, throughput,
ahorro de memoria o soporte de precisión basándose únicamente en el nombre de
un dispositivo.

```bash
cd skills/intel-hardware-advisor
python scripts/hardware_probe.py --format text
python scripts/hardware_probe.py --format json
```

Consulta el contrato completo de comportamiento y seguridad en
[`intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md).

### Intel Docs Reader

Usa esta skill cuando una pregunta necesite documentación oficial de OpenVINO
sobre APIs, dispositivos, configuración, instalación o limitaciones
documentadas. El lector usa una caché local e informa la página de origen de
los resultados útiles.

```bash
cd skills/intel-docs-reader
python scripts/read_openvino_docs.py --query "NPU device"
python scripts/read_openvino_docs.py --query "NPU device" --offline
```

La skill no descarga nada durante la instalación. Si falta la caché, la
primera consulta online descarga el archivo oficial configurado en la caché
local del usuario, fuera de la skill instalada y del repositorio.

Consulta el contrato completo de fuentes y límites de versión en
[`intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md).

## Inicio rápido

### Instalar para tu agente

Usa el comando de la skill que quieras añadir. El ejemplo usa Codex; cambia
`codex` por `claude-code` u otro agente compatible cuando sea necesario.

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-docs-reader -a codex
```

### Usar las skills publicadas

Clona el repositorio y ejecuta cada skill desde su propio directorio:

```bash
git clone https://github.com/michaeldouglas/intel-ai-skills.git
cd intel-ai-skills

python skills/intel-hardware-advisor/scripts/hardware_probe.py --format json
python skills/intel-docs-reader/scripts/read_openvino_docs.py --query "NPU device"
```

Para una validación determinista del hardware, pasa un fixture sanitizado al
hardware advisor. Un fixture es una entrada de prueba, no una dependencia de
runtime de la skill publicada:

```bash
python skills/intel-hardware-advisor/scripts/hardware_probe.py \
  --fixture path/to/sanitized-fixture.json \
  --format json
```

### Ejecutar el harness de ingeniería

El harness valida los candidatos antes de liberarlos en `skills/`:

```bash
cd harness
python -m venv .venv
source .venv/bin/activate             # macOS/Linux
# .venv\Scripts\Activate.ps1          # Windows PowerShell

python -m pip install --upgrade pip pytest
python -m pytest -q
```

La suite determinista está diseñada para ejecutarse sin hardware Intel,
OpenVINO, internet ni acceso a secretos. Las comprobaciones en hardware real
son complementarias.

## ¿Por qué Intel AI Skills?

Las cargas de IA son cada vez más heterogéneas. El mismo modelo puede
comportarse de forma muy diferente según el procesador, acelerador, versión
del runtime, driver, precisión, presupuesto de memoria y destino de despliegue.

Intel AI Skills convierte esa complejidad en un flujo disciplinado:

- **Consciente del hardware** — descubre la plataforma y el runtime local en lugar de adivinar por el nombre del dispositivo.
- **Calificada por evidencia** — separa hechos detectados, documentación oficial, mediciones, estimaciones e inferencias.
- **Portátil por diseño** — mantiene las skills de producto independientes del harness interno.
- **Determinista** — hace que el mismo fixture produzca la misma respuesta en cada máquina y pull request.
- **Privacidad por defecto** — recopila solo lo necesario y nunca inspecciona secretos o archivos no relacionados.
- **Honesta con la incertidumbre** — un resultado desconocido es válido cuando la evidencia está incompleta, en conflicto, desactualizada o no disponible.

## ¿Qué lo hace diferente?

```text
Entorno local
      │
      ▼
Descubrimiento de solo lectura → Hechos + fuentes + confianza → Orientación calificada
      │                                               │
      └────────────────→ Lo desconocido sigue desconocido
```

El proyecto convierte la investigación en una skill distribuible mediante
artefactos explícitos, fixtures reproducibles, pruebas automatizadas,
evaluación y revisión.

## Arquitectura

```text
intel-ai-skills/
├── harness/
│   ├── .specify/             # Constitución y memoria del proyecto Spec Kit
│   ├── candidates/           # Skills en desarrollo
│   ├── evaluations/          # Evaluaciones de recomendaciones y comportamiento
│   ├── fixtures/             # Entornos sanitizados y reproducibles
│   ├── research/             # Investigación técnica y evidencias versionadas
│   ├── specs/                # Especificaciones, planes y tareas
│   └── tests/                # Pruebas unitarias, de contrato e integración
├── skills/                   # Agent Skills revisadas y distribuibles
├── docs/                     # Documentación localizada
├── .github/workflows/        # Automatización de ramas y calidad
├── CONTRIBUTING.md           # Flujo de contribución y promoción
└── LICENSE                   # Apache License 2.0
```

La separación es intencional:

1. La investigación establece qué está documentado y qué sigue desconocido.
2. Spec Kit convierte los requisitos en un diseño y una secuencia de tareas explícitos.
3. Las skills candidatas implementan el comportamiento de producto dentro del harness.
4. Fixtures y pruebas hacen reproducible el comportamiento en las plataformas compatibles.
5. Las evaluaciones y la revisión de calidad de solo lectura controlan la promoción.
6. Solo los artefactos revisados llegan a `skills/`.

## Flujo de ramas y release

Todo trabajo sigue `feature/<nombre-kebab-case> → develop → main`:

- Los pull requests de features tienen como destino `develop`.
- Cuando una feature entra en `develop`, GitHub Actions abre o reutiliza un PR hacia `main`.
- El PR de promoción se revisa y se integra manualmente.
- Los commits y pushes directos a `main` no forman parte del flujo.

Lee el proceso completo en [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Spec Kit + Graphify

**Spec Kit** convierte una idea en especificación, plan, tareas,
implementación, evaluación y revisión. **Graphify** proporciona navegación
acotada del código mediante conceptos, relaciones, rutas y estructura entre
archivos.

La secuencia esperada es:

```text
Specify → Clarify → Plan → Tasks → Analyze → Implement → Evaluate → Review
```

El índice generado por Graphify es una ayuda de ingeniería y no sustituye las
pruebas ni la revisión.

## Contribuir

Son bienvenidos las ideas, informes de errores, mejoras de evidencia, fixtures
y nuevas skills. Antes de abrir un cambio:

1. Crea `feature/<nombre-kebab-case>` desde `develop`.
2. Sigue los artefactos de Spec Kit.
3. Mantén los fixtures sanitizados y reproducibles.
4. Ejecuta las pruebas y evaluaciones relevantes.
5. Haz el commit local de los cambios previstos.
6. Publica la rama y abre el PR contra `develop` solo después de la revisión local.

Consulta [`CONTRIBUTING.md`](../CONTRIBUTING.md) y la
[constitución](../harness/.specify/memory/constitution.md) del proyecto.

## Licencia

Distribuido bajo la [Apache License 2.0](../LICENSE).
