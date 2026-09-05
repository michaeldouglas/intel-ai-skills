# Quickstart: GitHub Pages Documentation Site

## Prerequisites

- Python 3.11 or newer.
- A checkout of the repository.

## Build and validate locally

From the repository root:

```powershell
python docs/site/scripts/build_site.py
```

Expected result: the command validates the published-skill catalog and writes
the generated site to `docs/site/build/site/`.

## Preview locally

From the repository root:

```powershell
python docs/site/scripts/serve_site.py
```

Open `http://127.0.0.1:8000/` in a browser. The preview script rebuilds the
site before starting the standard-library web server, so it represents the same
artifact used by the Pages workflow.

## Validate the repository

From `harness/`:

```powershell
python -m pytest -q
```

The site-specific tests verify that all published skills have pages, required
logo assets are copied, internal links resolve, and generated output exists.

## Publication flow

After the feature is merged into `main`,
`.github/workflows/deploy-pages.yml` runs the build, uploads `docs/site/build/site/` as a
Pages artifact, and deploys it to the `github-pages` environment. The first
publication may require the repository maintainer to enable GitHub Pages with
GitHub Actions as its source.
