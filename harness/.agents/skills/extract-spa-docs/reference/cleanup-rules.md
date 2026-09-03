# Converter cleanup rules

Recurring DOM noise that wrecks SPA-docs Markdown, and the fix for each. These are
platform-agnostic patterns observed across real docs sites (Theneo, Mintlify,
Docusaurus, GitBook). `extract.mjs` already applies most; this is the checklist to
extend it when a new site shows a new artifact.

## Inside the content container, before conversion

| Symptom in Markdown | DOM cause | Fix |
|---|---|---|
| Empty `## ` / `###` heading, real text on next line | heading wraps a `.copy-button`/permalink `<div>`+`<svg>` | strip `.copy-button, [class*="copy"], button, [role="button"], svg` inside the container before converting |
| `###### 1` … `#### Title` step soup | "steps" component marks step numbers as headings | drop headings whose text is only digits (`/^\d+$/`) or empty |
| Duplicate top `# Title` | container repeats the page H1 | drop the first `^#\s` line; re-add your own H1 from frontmatter |
| Orphaned `Copy`, `Ask AI`, `Was this helpful?`, `On this page` | feedback / TOC widgets inside the container | remove those nodes (or `[aria-hidden="true"]`) before converting |
| Nav/sidebar text leaking in | container selector too high in the tree | tighten the selector — walk the H1 ancestor chain to the smallest wrapper |

## On the converted Markdown

| Symptom | Fix |
|---|---|
| Over-escaping: `\-`, `\.`, `\(`, `\)` peppering prose | override Turndown `escape` to only escape `\ * _ \` ~` |
| 3+ blank lines | collapse `\n{3,}` → `\n\n` |
| Code fence lost its language | custom `pre>code` rule that reads `language-*` from the `class` |
| Tables mangled | use `turndown-plugin-gfm` |

## Sanity, not just cleanup

- **Content-loss ratio.** Record `mdLen / domLen` per page; a low ratio (< ~0.5) means
  text was dropped, not that the page is short. `verify.mjs` gates on this.
- **Absent content types.** Zero code blocks / tables across a whole site is often *real*
  (image-based walkthroughs; code lives in an excluded API explorer). Confirm in the DOM
  before assuming a conversion bug, and record the finding in `index.md`.
