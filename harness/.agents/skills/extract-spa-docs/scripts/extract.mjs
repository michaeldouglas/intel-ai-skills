#!/usr/bin/env node
/**
 * extract-spa-docs — reference extractor (FAST PATH).
 *
 * Generic, configurable SPA docs -> Markdown crawler. Adapt CONFIG via env vars;
 * the only thing most sites need is START_URL and (sometimes) CONTENT_SELECTOR.
 *
 * Deps (install in a scratch dir, then run the script FROM that dir so its
 * node_modules resolves — ESM ignores NODE_PATH):
 *   cd /tmp/spa && npm i playwright-core turndown turndown-plugin-gfm
 *   START_URL=... node <skill-dir>/scripts/extract.mjs       # cwd = /tmp/spa
 * Or point DEPS_DIR at the dir that holds node_modules.
 * A Chromium must exist: Playwright's cache, or set PW_EXECUTABLE to a Chrome binary.
 *
 * Config (env):
 *   START_URL         (required)  e.g. https://developers.example.com/docs
 *   SITE_NAME         derive from hostname if unset
 *   OUT_DIR           default: ./docs/<site-name>
 *   BASE_PATH         in-scope path prefix; default: pathname of START_URL
 *   CONTENT_SELECTOR  content container; auto-detected from the h1 ancestor chain if unset
 *   EXCLUDE           comma-separated substrings to drop from routes (e.g. /api-runner/,/login)
 *   HEADLESS          "1" to run headless (default headed — many WAFs 403 headless)
 *   MAX_PAGES         cap for testing
 *   FORCE             "1" to re-extract pages whose file already exists (default: resume/skip)
 *   USER_AGENT        override UA string
 *   DISCOVER_WAIT     ms to wait for nav to render before harvesting links (default 5000)
 *   RAW_MD            "auto" (default) try fetching <route>.md and skip the browser when a
 *                     platform serves raw Markdown (Theneo/Mintlify/etc.); "1" force, "0" off
 *   SITEMAP           "0" to skip sitemap.xml seeding (default: auto-fetch ORIGIN/sitemap.xml)
 *   SITEMAP_URL       explicit sitemap URL
 *   RECURSE           "0" to disable discover-as-you-crawl (default: harvest links per page)
 *   SEED_URLS         comma/newline-separated extra routes to force into the queue — use to
 *                     recover deep pages skipped on a prior run (resume can't rediscover them)
 *   REQUEST_DELAY     ms to pause between page fetches (default 0); set 200-500 to avoid the
 *                     WAF 403 tail that fast sequential crawls trigger after ~100 pages
 *   LOG_FILE          path for the run log (default: ./extract-<site>.log in cwd, NOT in OUT_DIR)
 *   DEPS_DIR          dir containing node_modules for deps (default: cwd)
 *
 * Output: OUT_DIR/<route>.md (+ frontmatter), OUT_DIR/index.md, OUT_DIR/manifest.json
 * Re-runnable: existing files are skipped unless FORCE=1 (crash-resumable).
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

// ---------- deps (resolve from DEPS_DIR/cwd; ESM ignores NODE_PATH) ----------
async function load(name) {
  try { return await import(name); } catch {}
  const depsDir = path.resolve(process.env.DEPS_DIR || process.cwd());
  try {
    const req = createRequire(path.join(depsDir, '_resolve_.js'));
    return await import(pathToFileURL(req.resolve(name)).href);
  } catch {
    console.error(`Missing dep "${name}". Install deps in a scratch dir and run the script`);
    console.error('from that dir (or set DEPS_DIR to the dir holding node_modules):');
    console.error('  npm i playwright-core turndown turndown-plugin-gfm');
    process.exit(2);
  }
}
const pw = await load('playwright-core');
const chromium = pw.chromium || (pw.default && pw.default.chromium);
const tdMod = await load('turndown');
const TurndownService = tdMod.default || tdMod;
const gfmMod = await load('turndown-plugin-gfm');
const gfm = gfmMod.gfm || (gfmMod.default && gfmMod.default.gfm);

// ---------- config ----------
const START = process.env.START_URL;
if (!START) { console.error('START_URL is required'); process.exit(2); }
const U = new URL(START);
const ORIGIN = U.origin;
const BASE = (process.env.BASE_PATH || U.pathname).replace(/\/$/, '') || '/';
const SITE = (process.env.SITE_NAME || U.hostname.split('.').slice(-2, -1)[0] || U.hostname)
  .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const OUTDIR = path.resolve(process.env.OUT_DIR || `docs/${SITE}`);
const EXCLUDE = (process.env.EXCLUDE || '').split(',').map(s => s.trim()).filter(Boolean);
const HEADLESS = process.env.HEADLESS === '1';
const MAX = process.env.MAX_PAGES ? parseInt(process.env.MAX_PAGES, 10) : Infinity;
const FORCE = process.env.FORCE === '1';
const DISCOVER_WAIT = process.env.DISCOVER_WAIT ? parseInt(process.env.DISCOVER_WAIT, 10) : 5000;
const RAW_MD = (process.env.RAW_MD || 'auto').toLowerCase();
const RECURSE = process.env.RECURSE !== '0';
const REQUEST_DELAY = process.env.REQUEST_DELAY ? parseInt(process.env.REQUEST_DELAY, 10) : 0;
const DATE = new Date().toISOString().slice(0, 10);
const UA = process.env.USER_AGENT ||
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36';

// keep the run log OUT of OUTDIR so it never ships inside the docs deliverable
const LOG = process.env.LOG_FILE || path.join(process.cwd(), `extract-${SITE}.log`);
fs.mkdirSync(OUTDIR, { recursive: true });
const log = (m) => { const line = `[${new Date().toISOString()}] ${m}`; console.log(line); try { fs.appendFileSync(LOG, line + '\n'); } catch {} };

// ---------- locate a Chromium ----------
function findChromium() {
  if (process.env.PW_EXECUTABLE && fs.existsSync(process.env.PW_EXECUTABLE)) return process.env.PW_EXECUTABLE;
  const caches = [
    path.join(process.env.HOME || '', 'Library/Caches/ms-playwright'),
    path.join(process.env.HOME || '', '.cache/ms-playwright'),
  ];
  for (const c of caches) {
    if (!fs.existsSync(c)) continue;
    const dirs = fs.readdirSync(c).filter(d => d.startsWith('chromium-')).sort().reverse();
    for (const d of dirs) {
      const cands = [
        `${c}/${d}/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`,
        `${c}/${d}/chrome-mac/Chromium.app/Contents/MacOS/Chromium`,
        `${c}/${d}/chrome-linux/chrome`,
        `${c}/${d}/chrome-win/chrome.exe`,
      ];
      for (const e of cands) if (fs.existsSync(e)) return e;
    }
  }
  return null; // let Playwright try its default / channel
}

// ---------- turndown ----------
const td = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced', bulletListMarker: '-', emDelimiter: '*' });
td.use(gfm);
// lighter escaping: prose dashes/dots/parens should not be backslashed
td.escape = (s) => s.replace(/([\\*_`~])/g, '\\$1');
td.addRule('fencedCode', {
  filter: (n) => n.nodeName === 'PRE' && n.firstChild && n.firstChild.nodeName === 'CODE',
  replacement: (_c, n) => {
    const code = n.firstChild;
    const m = (code.getAttribute('class') || '').match(/language-([\w-]+)/);
    const lang = m ? m[1] : '';
    return `\n\n\`\`\`${lang}\n${code.textContent.replace(/\n$/, '')}\n\`\`\`\n\n`;
  },
});

// ---------- scope + route helpers ----------
const stripHash = (u) => u.split('#')[0].replace(/\/$/, '');
// non-HTML documents a browser can't render to Markdown — downloaded verbatim instead
const DOC_RE = /\.(pdf|docx?|pptx?|xlsx?|odt|ods|odp|csv|rtf)(?:$|\?)/i;
function isDocLink(u) {
  let x; try { x = new URL(u); } catch { return false; }
  return x.origin === ORIGIN && DOC_RE.test(x.pathname);
}
function inScope(u) {
  let x; try { x = new URL(u); } catch { return false; }
  if (x.origin !== ORIGIN) return false;
  const p = x.pathname.replace(/\/$/, '');
  if (!p.startsWith(BASE)) return false;
  if (p.endsWith('.md')) return false;
  if (DOC_RE.test(p)) return false;   // documents are downloaded as assets, never queued as pages
  if (EXCLUDE.some(s => u.includes(s))) return false;
  return true;
}
const routeToRel = (u) => {
  let p = new URL(u).pathname.replace(/\/$/, '');
  let r = p.startsWith(BASE) ? p.slice(BASE.length) : p;
  r = r.replace(/^\//, '');
  return r === '' ? 'home' : r;
};
const relToFile = (r) => r + '.md';
const relByPath = new Map(); // pathname -> rel (for link rewriting)
function register(url) {
  const pth = new URL(url).pathname.replace(/\/$/, '');
  if (!relByPath.has(pth)) relByPath.set(pth, routeToRel(url));
}

// rewrite same-site captured links to relative .md, leave the rest absolute
function rewriteLinks(md, file) {
  return md.replace(/\]\((https?:\/\/[^)]+|\/[^)]+)\)/g, (full, href) => {
    let abs = href.startsWith('/') ? ORIGIN + href : href; let u;
    try { u = new URL(abs); } catch { return full; }
    const pth = u.pathname.replace(/\/$/, '');
    if (u.origin === ORIGIN && relByPath.has(pth)) {
      let rl = path.relative(path.dirname(file), relToFile(relByPath.get(pth)));
      if (!rl.startsWith('.')) rl = './' + rl;
      return '](' + rl + (u.hash || '') + ')';
    }
    return '](' + abs + (u.hash || '') + ')';
  });
}

// strip leading frontmatter + first H1, drop empty/number-only headings, collapse blanks
function normalizeMd(md) {
  return md
    .replace(/^﻿?---\n[\s\S]*?\n---\s*\n/, '')   // existing frontmatter
    .replace(/^\s*#\s+.*\n+/, '')                      // duplicate top H1
    .replace(/^#{1,6}\s+\d+\s*$/gm, '')                // decorative number-only headings
    .replace(/^#{1,6}\s*$/gm, '')                      // empty headings
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

// ---------- network helpers (raw markdown + sitemap) ----------
// Fetch through the browser context so WAFs that block plain fetch() (TLS
// fingerprinting) still serve us; fall back to global fetch before the context exists.
let httpCtx = null;
async function fetchText(url) {
  const headers = { 'user-agent': UA, accept: 'text/markdown,text/plain,application/xml,*/*' };
  try {
    if (httpCtx) { const r = await httpCtx.request.get(url, { headers }); return r.ok() ? await r.text() : null; }
    const r = await fetch(url, { headers }); return r.ok ? await r.text() : null;
  } catch { return null; }
}
async function probeRawMd(routeUrl) {
  const body = await fetchText(routeUrl + '.md');
  if (!body) return null;
  if (/^\s*<(!doctype|html)/i.test(body)) return null;   // HTML masquerading as .md
  if (body.trim().length < 50) return null;
  return body;
}
async function sitemapRoutes() {
  if (process.env.SITEMAP === '0') return [];
  const seeds = process.env.SITEMAP_URL ? [process.env.SITEMAP_URL] : [`${ORIGIN}/sitemap.xml`, `${ORIGIN}/sitemap_index.xml`];
  const found = new Set();
  const isIndex = (l) => /sitemap[\w-]*\.xml/i.test(l);
  for (const sm of seeds) {
    const xml = await fetchText(sm);
    if (!xml) continue;
    const locs = [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map(m => m[1]);
    for (const l of locs) {
      if (isIndex(l)) {
        const xx = await fetchText(l);
        if (xx) for (const m of xx.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)) found.add(m[1]);
      } else found.add(l);
    }
  }
  return [...new Set([...found].map(stripHash))].filter(inScope);
}

// ---------- run ----------
const exe = findChromium();
log(`site=${SITE} base=${BASE} out=${OUTDIR} headless=${HEADLESS} raw_md=${RAW_MD} exe=${exe || '(default)'}`);
const launch = await chromium.launch(exe ? { executablePath: exe, headless: HEADLESS } : { headless: HEADLESS, channel: 'chrome' }).catch(async () => chromium.launch({ headless: HEADLESS }));
const ctx = await launch.newContext({ userAgent: UA, locale: 'en-US', viewport: { width: 1440, height: 1200 } });
httpCtx = ctx; // route fetchText through the browser (shares WAF-passing fingerprint)
const page = await ctx.newPage();
page.setDefaultTimeout(30000);

// reveal lazy nav: expand aria controls + scroll every scrollable container
async function revealNav() {
  for (let i = 0; i < 4; i++) {
    for (const b of await page.$$('button[aria-expanded="false"], [aria-expanded="false"]')) { try { await b.click({ timeout: 300 }); } catch {} }
    await page.waitForTimeout(300);
  }
  for (let i = 0; i < 3; i++) {
    await page.evaluate(() => { document.querySelectorAll('*').forEach(e => { if (e.scrollHeight > e.clientHeight + 50) e.scrollTop = e.scrollHeight; }); });
    await page.waitForTimeout(600);
  }
}
async function harvestAnchors() {
  const hrefs = await page.evaluate((o) => [...document.querySelectorAll('a[href]')]
    .map(a => a.getAttribute('href')).filter(Boolean)
    .map(h => h.startsWith('/') ? o + h : h), ORIGIN);
  return [...new Set(hrefs.map(stripHash))].filter(inScope);
}
async function harvestDocLinks() {
  const hrefs = await page.evaluate((o) => [...document.querySelectorAll('a[href]')]
    .map(a => a.getAttribute('href')).filter(Boolean)
    .map(h => h.startsWith('/') ? o + h : h), ORIGIN);
  return [...new Set(hrefs.map(stripHash))].filter(isDocLink);
}

// discovery: start page nav + sitemap
await page.goto(START, { waitUntil: 'domcontentloaded', timeout: 45000 });
await page.waitForTimeout(DISCOVER_WAIT);
await revealNav();

let SELECTOR = process.env.CONTENT_SELECTOR || await page.evaluate(() => {
  for (const s of ['main', 'article', '[role="main"]', '.theme-doc-markdown', '#THContent', '#content-area']) {
    const el = document.querySelector(s); if (el && el.innerText.trim().length > 200) return s;
  }
  let el = document.querySelector('h1'); if (!el) return 'body';
  let best = el, prev = el.innerText.length;
  while (el && el.parentElement && el.parentElement.tagName !== 'BODY') {
    const pl = el.parentElement.innerText.length;
    if (pl > prev * 1.6) break;
    best = el.parentElement; prev = pl; el = el.parentElement;
  }
  if (best.id) return '#' + best.id;
  const cls = (best.className || '').toString().trim().split(/\s+/)[0];
  return cls ? best.tagName.toLowerCase() + '.' + cls : best.tagName.toLowerCase();
});
log(`content selector: ${SELECTOR}`);

const navRoutes = await harvestAnchors();
const smRoutes = await sitemapRoutes();
const docLinks = new Set(await harvestDocLinks()); // global nav/footer docs; unioned with per-page finds during the crawl
log(`discovery: nav=${navRoutes.length} sitemap=${smRoutes.length} docs=${docLinks.size}`);

// decide raw-markdown mode: probe START and a real leaf route (section landings
// often have no .md twin even when leaf pages do)
let rawMode = false;
if (RAW_MD === '1') rawMode = true;
else if (RAW_MD !== '0') {
  const probes = [stripHash(START), ...navRoutes.filter(r => r !== stripHash(START)).slice(0, 2)];
  for (const r of probes) { if (await probeRawMd(r)) { rawMode = true; break; } }
}
log(`raw-markdown mode: ${rawMode ? 'ON (fetching <route>.md)' : 'off (rendering DOM)'}`);

// seed queue (START first), register all known routes for link rewriting
const startRoute = stripHash(START);
const seedUrls = (process.env.SEED_URLS || '').split(/[\n,]/).map(s => s.trim()).filter(Boolean)
  .map(s => s.startsWith('http') ? s : ORIGIN + (s.startsWith('/') ? s : '/' + s)).map(stripHash).filter(inScope);
if (seedUrls.length) log(`seed-urls: ${seedUrls.length} extra routes injected`);
const queue = [...new Set([startRoute, ...seedUrls, ...navRoutes, ...smRoutes])];
for (const r of queue) register(r);
const seen = new Set(queue);
log(`seeded routes: ${queue.length}`);

// ---------- per-page extractors ----------
// an error shell (WAF 403 / 404 page) masquerading as content
const isErrorShell = (title, domLen) => /^(40\d|50\d)\b/.test((title || '').trim()) || /\b(Forbidden|Not Found|Access Denied|Too Many Requests)\b/i.test(title || '') || domLen < 40;

async function extractRendered(url) {
  const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  const status = resp ? resp.status() : 0;
  await page.waitForTimeout(1200);
  for (const b of await page.$$('button[aria-expanded="false"]')) { try { await b.click({ timeout: 250 }); } catch {} }
  for (const d of await page.$$('details:not([open])')) { try { await d.evaluate(e => (e.open = true)); } catch {} }
  await page.waitForTimeout(250);
  const data = await page.evaluate((sel) => {
    const src = document.querySelector(sel) || document.querySelector('main') || document.body;
    if (!src) return { html: null };
    const c = src.cloneNode(true);
    c.querySelectorAll('.copy-button,[class*="copy"],button,[role="button"],svg,[aria-hidden="true"]').forEach(e => e.remove());
    c.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => { const t = h.textContent.trim(); if (/^\d+$/.test(t) || t === '') h.remove(); });
    const h1 = document.querySelector('h1');
    return { html: c.innerHTML, title: h1 ? h1.innerText.trim() : (document.title || '').trim(), domLen: c.innerText.replace(/\s+/g, ' ').trim().length, imgs: c.querySelectorAll('img').length };
  }, SELECTOR);
  // reject non-2xx and error shells so we never persist a "403 Forbidden" as a doc page
  if (!data.html || status >= 400 || isErrorShell(data.title, data.domLen)) {
    return { error: status >= 400 ? `HTTP ${status}` : (data.html ? `error shell "${(data.title || '').slice(0, 40)}"` : 'no content container'), status };
  }
  let md = normalizeMd(td.turndown(data.html));
  const newLinks = RECURSE ? await harvestAnchors() : [];
  const newDocs = RECURSE ? await harvestDocLinks() : [];
  return { md, title: data.title, domLen: data.domLen, imgs: data.imgs, status, source: 'render', newLinks, newDocs };
}

async function extractRaw(url) {
  const body = await probeRawMd(url);
  if (body == null) return null;
  // title from frontmatter or first H1
  let title = '';
  const fmTitle = body.match(/^﻿?---\n[\s\S]*?\btitle:\s*["']?([^"'\n]+)/);
  if (fmTitle) title = fmTitle[1].trim();
  if (!title) { const h1 = body.match(/^\s*#\s+(.+)$/m); if (h1) title = h1[1].trim(); }
  const md = normalizeMd(body);
  const imgs = (md.match(/!\[[^\]]*\]\(/g) || []).length;
  // resolve absolute, root-relative, AND ./relative links against this page's URL so
  // discover-as-you-crawl works in raw-md mode too (rendered mode re-harvests anchors).
  const allLinks = RECURSE ? [...md.matchAll(/\]\(([^)\s]+)\)/g)]
    .map(m => { try { return new URL(m[1], url).href; } catch { return null; } })
    .filter(Boolean).map(stripHash) : [];
  const newLinks = allLinks.filter(inScope);
  const newDocs = allLinks.filter(isDocLink);
  return { md, title, domLen: 0, imgs, status: 200, source: 'raw-md', newLinks, newDocs };
}

// ---------- crawl (incremental, resumable, recursive) ----------
const manifest = [];
const skipped = [];
let n = 0;
for (let qi = 0; qi < queue.length && n < MAX; qi++) {
  const url = queue[qi];
  n++;
  const rel = routeToRel(url), file = relToFile(rel), outPath = path.join(OUTDIR, file);
  if (!FORCE && fs.existsSync(outPath)) { log(`(${n}) RESUME-SKIP ${rel}`); continue; }
  try {
    if (REQUEST_DELAY) await page.waitForTimeout(REQUEST_DELAY); // proactive pacing to dodge WAF rate-limits
    // up to 3 attempts with backoff — WAFs rate-limit fast sequential crawls with 403s
    let res = null, lastErr = '';
    for (let attempt = 1; attempt <= 3; attempt++) {
      res = rawMode ? await extractRaw(url) : await extractRendered(url);
      if (!res && rawMode) res = await extractRendered(url); // raw missed this route -> render fallback
      if (res && res.md) break;
      lastErr = (res && res.error) || 'no content';
      res = null;
      if (attempt < 3) { log(`(${n}) RETRY ${rel} (${lastErr}) backoff ${attempt * 2}s`); await page.waitForTimeout(attempt * 2000); }
    }
    if (!res || !res.md) { skipped.push({ url, reason: lastErr }); log(`(${n}) SKIP ${rel} (${lastErr})`); continue; }

    // enqueue newly discovered in-scope links; collect any linked documents
    if (RECURSE && res.newLinks) {
      for (const l of res.newLinks) if (!seen.has(l)) { seen.add(l); register(l); if (queue.length < MAX) queue.push(l); }
    }
    if (res.newDocs) for (const d of res.newDocs) docLinks.add(d);

    const md = rewriteLinks(res.md, file);
    const mdLen = md.replace(/[#>*`_\-\[\]()!]/g, '').replace(/\s+/g, ' ').trim().length;
    const ratio = res.source === 'raw-md' ? 1 : (res.domLen ? +(mdLen / res.domLen).toFixed(2) : 0); // raw-md is authoritative; empty render = 0
    // collapse newlines/whitespace so a multi-line hero <h1> can't break the YAML title or the body heading
    const cleanTitle = (res.title || rel).replace(/\s+/g, ' ').trim();
    // JSON.stringify yields a valid double-quoted YAML scalar (escapes quotes AND backslashes),
    // so a title ending in "\" or containing quotes can't break the frontmatter
    const fm = `---\ntitle: ${JSON.stringify(cleanTitle)}\nsource_url: ${JSON.stringify(url)}\nextracted_at: "${DATE}"\n---\n\n# ${cleanTitle}\n\n`;
    // defense in depth: a route's derived path must stay inside OUTDIR
    if (!path.resolve(outPath).startsWith(path.resolve(OUTDIR) + path.sep)) {
      skipped.push({ url, reason: 'route path escapes out dir' }); log(`(${n}) SKIP ${rel} (path escapes out dir)`); continue;
    }
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, fm + md + '\n');
    manifest.push({ url, rel, file, title: res.title, domLen: res.domLen, mdLen, ratio, imgs: res.imgs, source: res.source });
    log(`(${n}/${queue.length}) OK ${res.status} ${rel} [${res.source}] ratio=${ratio}`);
  } catch (e) {
    skipped.push({ url, reason: e.message.split('\n')[0] });
    log(`(${n}) FAIL ${rel} ${e.message.split('\n')[0]}`);
  }
}

// ---------- download linked documents (PDF/Office files) ----------
// These are excluded from page scope (a browser renders a PDF to an empty shell),
// so fetch them verbatim into assets/ instead of dropping real reference material.
const documents = [];
if (docLinks.size) {
  const assetsDir = path.join(OUTDIR, 'assets');
  for (const u of [...docLinks].sort()) {
    let name; try { name = decodeURIComponent(new URL(u).pathname.split('/').pop()) || ''; } catch { name = ''; }
    // basename only: a decoded segment can contain encoded path separators
    // (file..%2f..%2fevil.pdf -> ../../evil.pdf) that would escape assetsDir on join
    name = path.basename(name);
    if (!name || name === '.' || name === '..') name = 'document';
    const rel = `assets/${name}`, outPath = path.join(assetsDir, name);
    // defense in depth: never write outside the assets dir
    if (!path.resolve(outPath).startsWith(path.resolve(assetsDir) + path.sep)) {
      skipped.push({ url: u, reason: 'doc path escapes assets dir' }); log(`DOC SKIP ${name} (path escapes assets dir)`); continue;
    }
    if (!FORCE && fs.existsSync(outPath)) { documents.push({ url: u, file: rel }); continue; }
    try {
      const r = await httpCtx.request.get(u, { headers: { 'user-agent': UA }, timeout: 45000 });
      if (!r.ok()) { skipped.push({ url: u, reason: `doc HTTP ${r.status()}` }); log(`DOC SKIP ${name} (HTTP ${r.status()})`); continue; }
      const buf = await r.body();
      fs.mkdirSync(assetsDir, { recursive: true });
      fs.writeFileSync(outPath, buf);
      documents.push({ url: u, file: rel, bytes: buf.length });
      log(`DOC OK ${name} (${buf.length} bytes)`);
    } catch (e) { skipped.push({ url: u, reason: `doc ${e.message.split('\n')[0]}` }); log(`DOC FAIL ${name} ${e.message.split('\n')[0]}`); }
  }
}

// ---------- rebuild full page list from ALL files on disk ----------
// Resume runs only extract a subset, so manifest/index must be rebuilt from every
// file present (this run + prior runs) or they would clobber a complete crawl.
const prior = (() => { try { return JSON.parse(fs.readFileSync(path.join(OUTDIR, 'manifest.json'), 'utf8')); } catch { return null; } })();
function walkMd(dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const fp = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walkMd(fp));
    else if (e.name.endsWith('.md') && fp !== path.join(OUTDIR, 'index.md')) out.push(fp);
  }
  return out;
}
const curByFile = new Map(manifest.map(p => [p.file, p]));
const pages = walkMd(OUTDIR).map(fp => {
  const file = path.relative(OUTDIR, fp);
  const cur = curByFile.get(file);
  if (cur) return cur;
  const txt = fs.readFileSync(fp, 'utf8');
  const title = (txt.match(/^title:\s*"(.*)"$/m) || [])[1] || file.replace(/\.md$/, '');
  const url = (txt.match(/^source_url:\s*"(.*)"$/m) || [])[1] || `${ORIGIN}/${file.replace(/\.md$/, '')}`;
  return { url, rel: file.replace(/\.md$/, ''), file, title, imgs: (txt.match(/!\[[^\]]*\]\(/g) || []).length, source: 'prior-run' };
}).sort((a, b) => a.rel.localeCompare(b.rel));

// ---------- coverage ----------
const onDisk = new Set(pages.map(p => { try { return new URL(p.url).pathname.replace(/\/$/, ''); } catch { return p.rel; } }));
const smPaths = smRoutes.map(r => new URL(r).pathname.replace(/\/$/, ''));
const missingFromSitemap = smPaths.filter(p => !onDisk.has(p));
const coverage = {
  discovered: Math.max(queue.length, prior?.coverage?.discovered || 0, pages.length),
  extracted: pages.length,
  sitemap: smPaths.length,
  coveredOfSitemap: smPaths.length ? smPaths.length - missingFromSitemap.length : null,
  missingFromSitemap,
};

// merge skipped across runs; drop any that now exist on disk
const skippedAll = [...(prior?.skipped || []), ...skipped]
  .filter(s => { try { return !onDisk.has(new URL(s.url).pathname.replace(/\/$/, '')); } catch { return true; } });
const skippedMerged = [...new Map(skippedAll.map(s => [s.url, s])).values()];

// merge downloaded documents across runs; keep only those still present on disk
const documentsMerged = [...new Map([...(prior?.documents || []), ...documents].map(d => [d.url, d])).values()]
  .filter(d => fs.existsSync(path.join(OUTDIR, d.file)));

// preserve a real content selector from a prior run when this run detected nothing useful
const SELECTOR_OUT = manifest.length ? SELECTOR : (prior?.selector || SELECTOR);

// ---------- manifest + index ----------
fs.writeFileSync(path.join(OUTDIR, 'manifest.json'), JSON.stringify({ site: SITE, start: START, base: BASE, selector: SELECTOR_OUT, date: DATE, rawMode, coverage, pages, documents: documentsMerged, skipped: skippedMerged }, null, 2));
const imgPages = pages.filter(p => p.imgs >= 6).length;
let idx = `# ${SITE} docs (extracted)\n\n`;
idx += `- **Source:** ${START}\n- **Extracted:** ${DATE}\n`;
idx += `- **Tool:** ${rawMode ? 'Raw Markdown fetch (platform-served .md)' : 'Playwright (Chromium) rendered DOM'} via local automation\n`;
idx += `- **Content selector:** \`${SELECTOR_OUT}\`\n`;
idx += `- **Coverage:** extracted ${coverage.extracted}, discovered ${coverage.discovered}`;
if (coverage.sitemap) idx += `, sitemap ${coverage.sitemap} (covered ${coverage.coveredOfSitemap})`;
idx += `\n\n## Pages\n\n`;
for (const p of pages) { let pth = p.rel; try { pth = new URL(p.url).pathname; } catch {} idx += `- [${p.title || p.rel}](${p.file}) — \`${pth}\`\n`; }
if (documentsMerged.length) {
  idx += `\n## Linked documents\n\nNon-HTML files linked from the site, downloaded verbatim (a browser cannot render these to Markdown):\n\n`;
  for (const d of documentsMerged) idx += `- [${path.basename(d.file)}](${d.file}) — ${d.url}\n`;
}
if (skippedMerged.length) { idx += `\n## Skipped\n\n`; for (const s of skippedMerged) idx += `- ${s.url} — ${s.reason}\n`; }
if (missingFromSitemap.length) { idx += `\n## In sitemap but not extracted\n\n`; for (const m of missingFromSitemap) idx += `- ${ORIGIN}${m}\n`; }
idx += `\n## Notes\n\n`;
if (imgPages) idx += `- ${imgPages} image-heavy pages (≥6 images) reference images by absolute URL; they depend on the source CDN. Re-run with local download for a self-contained mirror.\n`;
idx += `- Rendered with a real browser; no authentication or access control bypassed.\n`;
idx += `- Run \`verify.mjs ${OUTDIR}\` to gate fidelity and coverage before relying on these docs.\n`;
fs.writeFileSync(path.join(OUTDIR, 'index.md'), idx);

log(`DONE extracted=${manifest.length} (total on disk ${pages.length}) docs=${documentsMerged.length} skipped=${skippedMerged.length} imgPages=${imgPages} coverage=${coverage.extracted}/${coverage.sitemap || coverage.discovered} missing=${missingFromSitemap.length}`);
await launch.close();
