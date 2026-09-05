# Research: GitHub Pages Documentation Site

## Decision: Deploy a generated static artifact with GitHub Actions

GitHub's custom Pages workflow supports checking out the repository, building
static files, uploading a Pages artifact, and deploying that artifact. The
deployment job requires `pages: write` and `id-token: write` permissions and
should target the `github-pages` environment. We will use the current official
action major versions: `actions/configure-pages@v5`,
`actions/upload-pages-artifact@v4`, and `actions/deploy-pages@v4`.

**Rationale**: This keeps `docs/` out of the publication input, makes the
build step explicit, and gives the repository a repeatable deployment path when
`main` changes.

**Alternatives considered**:

- Branch-based Pages from `docs/`: rejected because the user explicitly wants
  the existing `docs/` directory left untouched.
- A frontend framework: rejected because the site is static documentation and
  a standard-library build is easier to run locally and audit.

## Decision: Use authored JSON metadata plus generated HTML pages

The build will discover the directories under `skills/` and require a matching
entry in `docs/site/content/skills.json`. It will generate one detail page per
published skill and fail if coverage, required fields, or internal links are
invalid.

**Rationale**: The catalog stays explicit and reviewable while preventing a
new published skill from silently missing from the public site.

**Alternatives considered**:

- Copying full `SKILL.md` files into the site: rejected because agent
  instructions and harness-oriented implementation details are not the same as
  public product documentation.
- Hand-maintaining unrelated HTML pages: rejected because page coverage and
  navigation would drift more easily.

## Decision: Progressive enhancement with no frontend runtime dependency

Pages will contain complete semantic HTML and CSS. A small optional script may
enhance mobile navigation and theme behavior, but the overview, catalog, skill
links, and page content will work without JavaScript.

**Sources consulted**:

- GitHub Docs, *Using custom workflows with GitHub Pages*, consulted 2026-09-05:
  https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- GitHub Docs, *Configuring a publishing source for your GitHub Pages site*,
  consulted 2026-09-05:
  https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- `actions/deploy-pages` README, consulted 2026-09-05:
  https://github.com/actions/deploy-pages/blob/main/README.md
