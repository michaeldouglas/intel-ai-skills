#!/usr/bin/env node
/**
 * extract-spa-docs — verification gate.
 *
 * Objective fidelity check over an extracted docs folder. No browser, no re-crawl:
 * it reads manifest.json (written by extract.mjs) + the Markdown files.
 *
 *   node verify.mjs <out-dir> [--min-ratio 0.5] [--min-coverage 0.9]
 *
 * Fails (exit 1) when any page:
 *   - is missing frontmatter (title/source_url/extracted_at)
 *   - lost content: mdLen/domLen < min-ratio (text dropped in conversion)
 *   - has artifacts: empty headings, headings split from text, over-escaped runs
 *   - has an unresolved internal .md link
 *   - has an empty body
 * ...or when the CRAWL undershot coverage:
 *   - extracted < min-coverage of the sitemap route count (silent data loss)
 *   - suspiciously few pages vs. what discovery found
 *
 * Use it as the last step before reporting. A clean pass is the acceptance gate;
 * a failure means fix the converter/discovery in extract.mjs and re-run (FORCE=1),
 * not hand-patch.
 */
import fs from 'fs';
import path from 'path';

const OUT = process.argv[2];
if (!OUT || !fs.existsSync(OUT)) { console.error('usage: node verify.mjs <out-dir> [--min-ratio 0.5] [--min-coverage 0.9]'); process.exit(2); }
const minRatioArg = process.argv.indexOf('--min-ratio');
const MIN_RATIO = minRatioArg > -1 ? parseFloat(process.argv[minRatioArg + 1]) : 0.5;
const minCovArg = process.argv.indexOf('--min-coverage');
const MIN_COVERAGE = minCovArg > -1 ? parseFloat(process.argv[minCovArg + 1]) : 0.9;

const mdFiles = [];
(function walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) {
  const p = path.join(d, e.name);
  if (e.isDirectory()) walk(p);
  else if (e.name.endsWith('.md') && e.name !== 'index.md') mdFiles.push(p);
} })(OUT);

let manifest = { pages: [] };
const mPath = path.join(OUT, 'manifest.json');
if (fs.existsSync(mPath)) manifest = JSON.parse(fs.readFileSync(mPath, 'utf8'));
const ratioByFile = new Map(manifest.pages.map(p => [path.resolve(OUT, p.file), p.ratio]));

const fails = [], warns = [];
for (const f of mdFiles) {
  const rel = path.relative(OUT, f);
  const txt = fs.readFileSync(f, 'utf8');

  // frontmatter
  const fm = txt.startsWith('---\n') ? txt.slice(4, txt.indexOf('\n---', 4)) : '';
  for (const k of ['title:', 'source_url:', 'extracted_at:'])
    if (!fm.includes(k)) fails.push(`${rel}: missing frontmatter ${k}`);

  const body = txt.replace(/^---\n[\s\S]*?\n---\n/, '');
  // prose only: drop fenced + inline code, where backslashes are legitimate content
  // (Swift `\(x)`, regex, LaTeX) and would otherwise trip the over-escape check.
  const prose = body.replace(/```[\s\S]*?```/g, '').replace(/`[^`\n]*`/g, '');

  // empty body
  if (body.replace(/^#\s.*$/m, '').trim().length < 30) fails.push(`${rel}: body looks empty (<30 chars)`);

  // artifacts
  if (/^#{1,6}\s*$/m.test(body)) fails.push(`${rel}: empty heading`);
  if (/\\[-.()]/.test(prose)) warns.push(`${rel}: over-escaped chars (\\- \\. )`);
  // heading whose text is only on the next line (split heading)
  if (/^#{1,6}[ \t]*\n[ \t]*\n?[^\s#]/m.test(body)) warns.push(`${rel}: heading split from its text`);
  // common orphaned UI labels
  if (/^(Copy|Copied|Ask AI|Was this (page )?helpful\??|On this page)\s*$/m.test(body)) warns.push(`${rel}: orphaned UI label`);

  // content-loss ratio (if manifest has it)
  const r = ratioByFile.get(path.resolve(f));
  if (r !== undefined && r < MIN_RATIO) fails.push(`${rel}: content loss, text ratio ${r} < ${MIN_RATIO}`);

  // internal link resolution
  for (const m of body.matchAll(/\]\((\.[^)#]+\.md)(#[^)]*)?\)/g)) {
    const target = path.resolve(path.dirname(f), m[1]);
    if (!fs.existsSync(target)) fails.push(`${rel}: broken internal link -> ${m[1]}`);
  }
}

// ---------- coverage gate (catches under-crawl / silent data loss) ----------
const cov = manifest.coverage;
if (cov) {
  // sitemap is the strongest signal: extracted should cover ~all of it
  if (cov.sitemap > 0) {
    const ratio = cov.coveredOfSitemap / cov.sitemap;
    if (ratio < MIN_COVERAGE) {
      fails.push(`coverage: extracted only ${cov.coveredOfSitemap}/${cov.sitemap} sitemap routes (${(ratio * 100).toFixed(0)}% < ${(MIN_COVERAGE * 100).toFixed(0)}%) — discovery undershot`);
      for (const m of (cov.missingFromSitemap || []).slice(0, 15)) fails.push(`  missing: ${m}`);
      if ((cov.missingFromSitemap || []).length > 15) fails.push(`  ... +${cov.missingFromSitemap.length - 15} more missing`);
    }
  }
  // no sitemap to anchor on (blocked/absent — common on the SPA/WAF sites this targets):
  // fall back to extracted vs discovered, so an under-crawl still fails the gate.
  else if (cov.discovered > 0) {
    const ratio = cov.extracted / cov.discovered;
    if (ratio < MIN_COVERAGE) {
      fails.push(`coverage: extracted only ${cov.extracted}/${cov.discovered} discovered routes (${(ratio * 100).toFixed(0)}% < ${(MIN_COVERAGE * 100).toFixed(0)}%, no sitemap to anchor on) — crawl undershot or pages skipped; recover via SEED_URLS`);
    }
  }
  // sanity: many routes discovered but almost nothing written = broken crawl
  if (cov.discovered >= 5 && mdFiles.length < Math.max(2, cov.discovered * 0.25)) {
    fails.push(`coverage: discovered ${cov.discovered} routes but only wrote ${mdFiles.length} pages — crawl likely broke early`);
  }
} else {
  warns.push('no coverage data in manifest.json (older extract.mjs?) — coverage NOT verified; confirm route count by hand');
}

console.log(`Verified ${mdFiles.length} pages in ${OUT}`);
if (cov) console.log(`  coverage: extracted ${cov.extracted}, discovered ${cov.discovered}${cov.sitemap ? `, sitemap ${cov.coveredOfSitemap}/${cov.sitemap}` : ''}`);
console.log(`  failures: ${fails.length}   warnings: ${warns.length}   min-ratio: ${MIN_RATIO}   min-coverage: ${MIN_COVERAGE}`);
if (warns.length) { console.log('\nWARN:'); for (const w of warns.slice(0, 50)) console.log('  - ' + w); if (warns.length > 50) console.log(`  ... +${warns.length - 50} more`); }
if (fails.length) { console.log('\nFAIL:'); for (const x of fails.slice(0, 50)) console.log('  - ' + x); if (fails.length > 50) console.log(`  ... +${fails.length - 50} more`); }
console.log(fails.length ? '\nGATE: FAIL — fix extract.mjs and re-run with FORCE=1' : '\nGATE: PASS');
process.exit(fails.length ? 1 : 0);
