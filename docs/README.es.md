# Intel AI Skills

<p align="center"><strong>Skills para agentes, basadas en evidencia, para cargas de trabajo de Intel AI y OpenVINO.</strong></p>

<p align="center">
  <a href="../README.md">🇺🇸 English</a> ·
  <a href="./README.pt-BR.md">🇧🇷 Português (Brasil)</a>
</p>

> **Construye con evidencia. Despliega con confianza.**

Este repositorio publica Agent Skills portátiles para hardware Intel, runtimes
OpenVINO y decisiones sobre cargas de IA basadas en evidencia. Instala la skill
que necesites y deja que tu agente la use cuando la tarea lo requiera.

## Skills disponibles

Las skills publicadas están en [`skills/`](../skills/). Cada una es
autocontenida y puede instalarse de forma independiente.

| Skill | Úsala cuando necesites | Documentación |
|---|---|---|
| **Intel Hardware Advisor** | Inspeccionar un entorno local de inferencia Windows o Linux y entender qué permiten concluir las evidencias disponibles. | [`intel-hardware-advisor/SKILL.md`](../skills/intel-hardware-advisor/SKILL.md) |
| **Intel Docs Reader** | Buscar y citar el archivo local versionado de la documentación oficial de OpenVINO. | [`intel-docs-reader/SKILL.md`](../skills/intel-docs-reader/SKILL.md) |

### Intel Hardware Advisor

Usa esta skill cuando tu agente necesite entender el entorno local de
inferencia antes de elegir un camino de ejecución Intel. Hace descubrimiento de
solo lectura, separa los hechos de la plataforma de los del runtime, sigue los
identificadores de evidencia y mantiene visibles los resultados `unknown`,
`unavailable` y `no_decision`.

No instala paquetes, cambia drivers, ejecuta benchmarks, recorre archivos
arbitrarios ni infiere compatibilidad de modelos, latencia, throughput,
ahorro de memoria o soporte de precisión basándose únicamente en el nombre de
un dispositivo.

### Intel Docs Reader

Usa esta skill cuando tu agente necesite documentación oficial de OpenVINO
sobre APIs, dispositivos, configuración, instalación o limitaciones
documentadas. Usa una caché local y cita la página de origen de los resultados
útiles.

## Inicio rápido

### Instalar para tu agente

Usa el comando de la skill que quieras añadir. El ejemplo usa Codex; cambia
`codex` por `claude-code` u otro agente compatible cuando sea necesario.

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor -a codex
npx skills add michaeldouglas/intel-ai-skills --skill intel-docs-reader -a codex
```

O instala las dos skills con un solo comando:

```bash
npx skills add michaeldouglas/intel-ai-skills --skill intel-hardware-advisor --skill intel-docs-reader -a codex
```

### Usar las skills instaladas

Después de la instalación, pide a tu agente que inspeccione el hardware o
responda una pregunta sobre OpenVINO. La propia skill ejecuta sus scripts
incluidos automáticamente. No necesitas cambiar de directorio ni ejecutar
scripts Python manualmente.

## ¿Por qué Intel AI Skills?

Las cargas de IA son cada vez más heterogéneas. El mismo modelo puede
comportarse de forma muy diferente según el procesador, acelerador, versión
del runtime, driver, precisión, presupuesto de memoria y destino de despliegue.

Intel AI Skills convierte esa complejidad en un flujo disciplinado:

- **Consciente del hardware** — descubre la plataforma y el runtime local en lugar de adivinar por el nombre del dispositivo.
- **Calificada por evidencia** — separa hechos detectados, documentación oficial, mediciones, estimaciones e inferencias.
- **Portátil por diseño** — cada skill publicada es autocontenida e independiente.
- **Determinista** — hace que el mismo fixture produzca la misma respuesta en cada máquina y pull request.
- **Privacidad por defecto** — recopila solo lo necesario y nunca inspecciona secretos o archivos no relacionados.
- **Honesta con la incertidumbre** — un resultado desconocido es válido cuando la evidencia está incompleta, en conflicto, desactualizada o no disponible.

## Cómo funcionan las skills

```text
Entorno local o pregunta sobre OpenVINO
                  │
                  ▼
El agente invoca la skill instalada y sus scripts incluidos
                  │
                  ▼
Hechos + fuentes + confianza → Orientación calificada
```

## Seguridad y evidencia

Las skills están diseñadas para el descubrimiento de solo lectura cuando esa
función es necesaria. Separan hechos detectados, documentación oficial,
mediciones, estimaciones e inferencias. La evidencia desconocida, no
disponible o en conflicto permanece visible en lugar de ser sustituida por
suposiciones.

## Licencia

Distribuido bajo la [Apache License 2.0](../LICENSE).
