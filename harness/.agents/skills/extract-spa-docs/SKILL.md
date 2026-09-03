---
name: extract-spa-docs
description: "Extract documentation from rendered SPA or app-driven docs sites into local Markdown under a site-named docs folder. Use when docs live in an app UI or docs website with no source Markdown available, and an agent must drive a real browser for route discovery, DOM extraction, content cleanup, and link rewriting. Works with Playwright MCP, Chrome DevTools MCP, or any browser automation."
---

# Extract SPA Docs

## Purpose

Turn documentation trapped inside a rendered React app, SPA, or docs site into durable Markdown files an agent can read without reopening the browser.

The rendered browser is the source of truth. Do not rely on source-code guessing when docs are generated, hydrated, hidden behind client-side routes, loaded from APIs, or split across JavaScript chunks.

## Output

Write extracted docs under:

```text
docs/<site-name>/
```

Use the user's requested site name, or derive a stable lowercase hyphenated name from the page title, product heading, hostname, package/app name, or repo name.

Create:

- `index.md` with site name, source URL, extraction date, coverage summary, page list, skipped pages, and attribution notes.
- One Markdown file per route or article.
- Relative Markdown links between captured pages.

Use lowercase hyphenated filenames from the route or title, such as `getting-started.md`, `api-authentication.md`, or `components-button.md`. Avoid opaque counters unless no meaningful route or title exists.

Do not overwrite human-authored docs blindly. If the target folder exists, inspect it first and either update generated files carefully or write to a fresh folder such as `docs/<site-name>-extracted/`.

## Page Format

Start each generated page with compact YAML frontmatter, then one top-level heading and the extracted body:

```yaml
---
title: "Page Title"
source_url: "https://example.com/docs/page"
extracted_at: "YYYY-MM-DD"
---
```

Keep frontmatter factual and machine-readable so future agents can search, cite, filter, and refresh the docs.

## Access Rules

Extract only documentation the user is allowed to access and reuse for the requested work.

- Keep `source_url` accurate for every page.
- Do not bypass authentication, paywalls, robots restrictions, rate limits, or access controls.
- Do not crawl unrelated external sites unless explicitly in scope.
- Do not present extracted third-party docs as original project-authored content.
- Prefer purpose-limited extraction over bulk mirroring.
- Record access limits, protected pages, skipped pages, and attribution notes in `index.md`.

## Browser And Scope

Use any real browser/devtools path available: Playwright MCP, Chrome DevTools MCP, Playwright, Puppeteer, Selenium/WebDriver, Cypress, an in-app browser, or a local browser with devtools. If no browser path is available, stop and ask for one. Do not substitute static source inspection.

Scale the crawl to the request:

- **Single page:** open the URL, extract it, write one page and a minimal `index.md`.
- **Section:** discover routes inside the requested sidebar group or product area only.
- **Full site:** run full route discovery, link mapping, and quality checks.

If scope is ambiguous, confirm with the user or extract the obvious subset and record what was left out.

**Distinguish documentation from app data first.** Not every rendered SPA is a docs site. Many are apps — dashboards, event/results sites, catalogs, social feeds — whose routes are mostly per-record detail pages keyed by opaque IDs (`/teams/r1cv550094cyd5h`, `/matches/6a378ee6ak78yjk`, `/users/42`). Those records are generated database rows, not documentation: capturing hundreds of them inflates the route count without producing anything worth reading or citing. After discovery, look at the route shape. If the set is dominated by ID-keyed detail routes under a few collection prefixes, the **substantive content** is the handful of named pages (landing, guides, about, a few section indexes) — confirm with the user whether they want the full record dump or just the content pages, and either way **say plainly in `index.md` which routes are real documentation and which are bulk records**. Measure "done" against the content pages, not the raw route total — 130 near-identical record pages passing the fidelity gate does not mean the site was usefully extracted. When the target is genuinely a docs platform (Mintlify, GitBook, Docusaurus, Theneo, etc.), every route is content and this caveat does not apply.

## Two Paths

**Fast path (preferred when Node + a Chromium are available):** this skill ships a reference crawler. Install deps in a scratch dir **and run the script from that dir** — ESM resolves bare imports from the working dir, not the script's location, so `NODE_PATH` does not help:

```bash
mkdir -p /tmp/spa && cd /tmp/spa
npm i playwright-core turndown turndown-plugin-gfm
START_URL="https://site/docs" OUT_DIR="docs/<site>" node <skill-dir>/scripts/extract.mjs
node <skill-dir>/scripts/verify.mjs docs/<site>
```

Run from the dir holding `node_modules`, or set `DEPS_DIR` to it. (Copying the two `.mjs` files into the scratch dir also works.)

`extract.mjs`:

- **Tries raw Markdown first.** Many doc platforms (Theneo, Mintlify, GitBook) serve a `.md` twin of every page. The script probes `<route>.md`; when it returns real Markdown it fetches that directly and skips browser rendering — faster and higher fidelity than DOM→Markdown. Force with `RAW_MD=1`, disable with `RAW_MD=0`.
- **Seeds discovery from the sitemap.** It fetches `ORIGIN/sitemap.xml` (and sitemap indexes) and merges in-scope URLs, so coverage does not depend on the sidebar rendering perfectly. Disable with `SITEMAP=0`.
- **Reveals lazy nav.** It waits (`DISCOVER_WAIT`, default 5s), expands `aria-expanded` controls, and scrolls every scrollable container — SPA sidebars (Theneo/GitBook) lazy-render links on scroll, so a short wait alone misses most routes.
- **Discovers as it crawls.** Every visited page contributes its in-scope links back to the queue (`RECURSE=0` to disable), catching orphan pages linked only from deep routes.
- Auto-detects the content container (overridable via `CONTENT_SELECTOR`), writes one Markdown file per route with frontmatter, rewrites links, and emits `manifest.json` (with a `coverage` block) + `index.md`. It writes incrementally and resumes (re-run skips existing files; `FORCE=1` re-does them). `index.md`/`manifest.json` are rebuilt from **every file on disk** each run — so a resume that re-fetches only a few pages still produces a complete index, and the skipped list drops pages since recovered.
- **Downloads linked documents instead of rendering them.** PDF/Office files (`.pdf`, `.docx`, `.xlsx`, `.pptx`, …) can't be rendered to Markdown — a browser returns an empty shell. The script detects these links, excludes them from page scope, fetches them verbatim into `OUT_DIR/assets/`, and lists them under a **Linked documents** heading in `index.md` (with a `documents` block in `manifest.json`) rather than burying them as skipped pages. These are often the most authoritative content (terms, rulebooks, spec sheets), so they are captured, not dropped.
- **Recovers pages skipped on a prior run.** WAFs rate-limit fast crawls and 403 the tail; those deep routes were discovered mid-crawl, so a plain resume won't re-queue them (their parent pages are skipped before contributing links). Re-run with `SEED_URLS="<full-url-1>,<full-url-2>,..."` (the *full* URLs from the prior run's skipped list, including the base path) to inject them directly. The 403s are usually transient — wait a moment and the same pages succeed.

`verify.mjs` is the acceptance gate — it checks per-page fidelity **and** crawl coverage (extracted vs. sitemap count), so an under-crawl that captures a fraction of the site fails the gate instead of passing silently. Read `reference/cleanup-rules.md` before adapting the converter.

**Fallback path (no scripts, or a browser MCP only):** follow the prose Workflow below by hand. Same contract, same checks — just driven through whatever browser tool you have.

Whichever path you take, the Output, Page Format, Access Rules, and Verification Gate below are binding.

## Workflow

1. Open the start URL or local dev-server route in a browser and wait for rendering.
2. Derive or confirm the site name and output folder.
3. Discover in-scope documentation routes when scope is section or full-site.
4. Visit each route, including client-side routes without full page reloads.
5. Reveal hidden docs content: accordions, details, tabs, code variants, and show-more controls.
6. Extract the smallest meaningful content container.
7. Convert the content to clean Markdown.
8. Rewrite links using the route-to-file map.
9. Write `index.md`.
10. Run the verification gate before reporting.

## Runtime And Throughput

Rendered crawls are slow — budget ~2-4 seconds per page (navigation + render + reveal waits). A 50-page site is several minutes, which exceeds typical foreground command limits.

- **Write incrementally.** Save each page as it is extracted, never only at the end — a crash or timeout must not lose the whole run.
- **Make it resumable.** Skip routes whose output file already exists so a re-run continues where it stopped (force a refresh explicitly). Rebuild the index/manifest from all files on disk, not just the current batch, or a resume will overwrite a complete crawl's index with a partial one.
- **Expect WAF rate-limiting on the tail of large crawls.** Fast sequential requests get 403'd after ~100 pages. Set `REQUEST_DELAY=300` (ms between fetches) to avoid it proactively; to recover pages already skipped, feed their exact URLs back in via `SEED_URLS` (the block is transient).
- **Run long crawls in the background** and poll progress from a log, rather than blocking on one foreground call.
- **Cap during testing** (a small page limit) before committing to the full site.

## Route Discovery

Collect routes from multiple signals — never trust the rendered sidebar alone:

- **`sitemap.xml` (and sitemap indexes)** — the most reliable full list; fetch it first and use it as the coverage baseline.
- Header, sidebar, table of contents, footer, card, tab, and menu links.
- Links revealed after expanding navigation **and after scrolling** — SPA sidebars often lazy-render entries only when their container scrolls into view, so a fixed wait misses most of the tree. Scroll every scrollable container, then re-harvest.
- **Links found on each crawled page**, fed back into the queue (discover-as-you-crawl), to catch orphans linked only from deep pages.
- Client-side route changes caused by clicking docs navigation.
- Search index, route manifest, or JSON payloads seen in network requests.
- Static assets or script chunks only when the browser UI does not expose enough navigation.
- URL patterns clearly inside the same docs area.

Cross-check the final route count against the sitemap. If you captured far fewer pages than the sitemap lists, discovery undershot — fix it and re-crawl; do not report done.

Stay in scope. Avoid marketing pages, login flows, external sites, app dashboards, or destructive routes unless the user asks.

## DOM Extraction

First identify the docs platform and its content container — it is platform-specific and often **not** a semantic tag. Try `main`, `article`, `[role="main"]` first, but many SPAs (Theneo, Mintlify, Docusaurus, GitBook) wrap content in a framework `div` such as `#THContent` or `.theme-doc-markdown`. When semantic selectors miss, inspect the ancestor chain of the page `h1` to find the smallest wrapper that holds the full body, then reuse that selector for every route.

Exclude app chrome and noise: nav, sidebars, repeated headers, unrelated footers, cookie banners, ads, feedback widgets, edit links, theme controls, and hidden duplicates unless needed for tabs or collapsed docs.

## Markdown Conversion

Preserve:

- Heading hierarchy, paragraphs, notes, warnings, callouts, and blockquotes.
- Ordered/unordered lists, tables, inline code, keyboard shortcuts, and command snippets.
- Code blocks with language labels.
- API names, props, options, parameters, and return values.

Images: keep `alt` text, and reference each image by absolute URL by default so pages render without the app. Note in `index.md` that images depend on the source CDN. Download images to a local `assets/` folder and rewrite to relative paths only when the user asks for a self-contained mirror or the source is likely to disappear. Flag image-heavy pages where the meaning lives in screenshots, since those degrade most if the CDN goes away.

Clean (see `reference/cleanup-rules.md` for the full pattern→fix table):

- Strip UI chrome inside the container before converting: copy buttons, permalink icons, `svg`, feedback widgets.
- Drop empty headings and decorative number-only headings (step components).
- Remove the duplicate top-level H1; re-add your own from the frontmatter title.
- Lighten escaping so prose `-`, `.`, `(` `)` are not backslashed; collapse 3+ blank lines.
- Mark uncertain conversions with a short note instead of silently dropping content.

Use a DOM-to-Markdown library when available (the fast path uses Turndown + GFM). Otherwise convert headings, paragraphs, lists, tables, links, images, `pre`/`code`, and blockquotes directly.

## Link Rewriting

Keep a route-to-file map.

- Same-site captured route -> relative `.md` link.
- Same-site uncaptured route -> original absolute URL.
- External link -> original absolute URL.
- Same-page hash -> local anchor when the heading exists.
- Asset link -> original absolute URL unless intentionally downloaded.
- Document link (`.pdf`, `.docx`, `.xlsx`, `.pptx`, …) -> download the file verbatim into `assets/` and link it relatively. Do **not** try to render a PDF/Office file through the browser — it yields an empty shell. List these under a **Linked documents** heading in `index.md`; they are frequently the most authoritative material on the site.

Do not invent pages for uncaptured links. Record important skipped links in `index.md`.

## Worked Example

For `https://acme.dev/docs/auth`, pick `article`, drop app chrome, and rewrite in-scope links:

```html
<nav>...</nav>
<article>
  <h1>Authentication</h1>
  <p>Authenticate requests with a bearer token.</p>
  <pre><code class="language-bash">curl -H "Authorization: Bearer $TOKEN" ...</code></pre>
  <a href="/docs/errors">Error reference</a>
  <footer>Was this helpful?</footer>
</article>
```

````markdown
---
title: "Authentication"
source_url: "https://acme.dev/docs/auth"
extracted_at: "2026-06-23"
---

# Authentication

Authenticate requests with a bearer token.

```bash
curl -H "Authorization: Bearer $TOKEN" ...
```

See the [Error reference](errors.md).
````

## Verification Gate

This is the acceptance step, not a spot-check. The fast path runs it as `verify.mjs <out-dir>`; the fallback path performs the same checks by hand. **Do not report done until the gate passes.**

- **Coverage:** the number of pages extracted matches the route count discovered, and covers ~all of the sitemap (the gate fails below ~90%). A handful of pages out of a large sitemap means discovery undershot — fix discovery and re-crawl, do not accept it. Per-page fidelity passing does **not** imply the crawl was complete. Conversely, a high route count made up mostly of ID-keyed record pages does **not** imply the *documentation* was captured — confirm the real content pages are present and called out in `index.md` (see "Distinguish documentation from app data").
- **Frontmatter:** every page has `title`, `source_url`, and matching `extracted_at`.
- **No content loss:** per-page text ratio (converted text ÷ rendered DOM text) is above ~0.5. A low ratio means text was dropped, not that the page is short. (Raw-Markdown pages are authoritative and exempt from the ratio check.)
- **Fidelity, not just presence:** no empty headings, headings split from their text, orphaned nav/UI labels (`Copy`, `Was this helpful?`), over-escaped characters, or broken lists. On failure, **fix the converter and re-run — do not hand-patch pages.**
- **Links resolve:** every relative `.md` link points at a captured file.
- **Self-contained:** the folder reads without running the app (note any CDN-dependent images).
- **Verified absence:** when a content type is missing everywhere (e.g. zero code blocks across an API docs site), confirm in the DOM it is genuinely absent — it may live in an excluded app — and record that in `index.md`.
- Record skipped routes, failed pages, auth barriers, and attribution notes in `index.md`.

## Reporting

Report the source URL, output folder, route count discovered/extracted, coverage vs. the sitemap, whether raw Markdown or rendered DOM was used, browser/devtools tool used, skipped pages, and assumptions about site name, scope, authentication, or generated content.

The final result should be a docs folder an agent can search, read, and cite directly as Markdown.
