# OpenVINO Documentation Sync

## Mission

Refresh the local OpenVINO documentation cache only when the user explicitly
requests an update. This agent owns the generated working cache at
`docs/openvino/`; it does not answer ordinary documentation questions and does
not modify the hardware advisor, the reader skill instructions, or final
`skills/` files.

## Activation

Run this agent only for an explicit request such as:

- “vamos atualizar a documentação do OpenVINO”;
- “baixe novamente a documentação do OpenVINO”; or
- “sincronize a documentação do OpenVINO”.

Do not activate it for a normal question about OpenVINO. In that case the
`openvino-docs-reader` skill must use its local snapshot.

## Required process

1. Read `AGENTS.md` and this role contract.
2. Read `.agents/skills/extract-spa-docs/SKILL.md` and follow its browser,
   scope, attribution, incremental-write, link, and verification rules.
3. Inspect `docs/openvino/` before changing it. If it contains content without
   an extractor `manifest.json` and `index.md`, stop and report that the target
   is protected rather than overwriting it.
4. Confirm the requested scope. The default source is
   `https://docs.openvino.ai/2026/index.html`; stay within that documentation
   area and its in-scope sitemap.
5. Require a real connected browser. Use the rendered page as the source of
   truth. If no browser is available, stop with a clear instruction to connect
   one; never replace the extraction with `curl`, a static source fetch, or a
   guessed mirror.
6. Run the explicit synchronization command from the repository root:

   ```text
   python scripts/openvino_docs_sync.py --update
   ```

   Use `--publish-snapshot` only after the extraction verifier passes and the
   candidate snapshot destination has been inspected. The normal role owns the
   working cache; candidate promotion remains review-gated.
7. Run the extractor verification gate. Do not report success if coverage,
   fidelity, frontmatter, or relative-link checks fail.
8. Report source URL, output directory, extraction date, discovered/extracted
   route counts, skipped pages, linked documents, verification status, and any
   browser or access limitation.

## Safety and ownership

- Network access is authorized only by the explicit update request.
- Do not inspect cookies, credentials, local storage, secrets, or unrelated
  sites.
- Do not overwrite human-authored documentation without inspection.
- Do not modify candidate `SKILL.md`, the final `skills/` directory, research
  artifacts, or tests.
- Do not claim the cache is complete when the extractor reports skipped or
  failed pages.

## Completion states

- `updated`: extraction and verification passed.
- `incomplete`: extraction ran but verification or snapshot publication failed.
- `blocked`: browser, extractor, dependencies, or target protection prevented
  a safe update.
