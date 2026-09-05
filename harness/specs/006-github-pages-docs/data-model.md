# Data Model: GitHub Pages Documentation Site

## Published Skill

Represents one distributable directory under `skills/` and one public detail
page.

| Field | Type | Required | Validation |
|---|---|---:|---|
| `id` | string | yes | Matches an existing directory under `skills/` |
| `slug` | string | yes | Lowercase URL-safe identifier, unique |
| `name` | string | yes | Public display name |
| `category` | string | yes | One of the navigation groups |
| `tagline` | string | yes | One-sentence value statement |
| `purpose` | string | yes | Public explanation of the skill |
| `when_to_use` | string[] | yes | At least two concrete situations |
| `workflow` | string[] | yes | Ordered high-level behavior |
| `boundaries` | string[] | yes | At least one limitation or non-goal |
| `install` | string | yes | Copyable `npx skills add` command |
| `related` | string[] | no | References valid skill IDs |

## Documentation Site

The generated static site contains:

- `index.html`: project overview and primary calls to action.
- `getting-started.html`: installation, agent portability, and the boundary
  between a portable skill and the repository that publishes it.
- `skills/index.html`: grouped catalog.
- `skills/<slug>.html`: generated detail pages for every Published Skill.
- `404.html`: branded fallback for invalid routes.

Each documentation route also exposes a shared navigation shell:

- `sidebar`: project entry points plus grouped links for every published skill;
- `breadcrumbs`: the current location from the project home to the page;
- `toc`: anchors for the major sections available on the current page;
- `previous/next`: adjacent skill links on generated skill detail pages.

These navigation fields are generated from the localized site and catalog data;
they are presentation metadata, not a second source of truth for skill content.

## Locale

Represents one supported language and its translated public copy.

| Field | Type | Required | Validation |
|---|---|---:|---|
| `id` | string | yes | `en`, `pt-br`, or `es`; unique route prefix |
| `lang` | string | yes | HTML language tag |
| `label` | string | yes | Short accessible selector label |
| `ui` | object | yes | Contains every shared interface label |
| `categories` | object | yes | Contains every catalog category |
| `skills` | object | yes | Contains translated metadata for every Published Skill |

English is emitted at the site root. The `pt-br` and `es` locales are emitted
under their route prefixes and preserve the same page and skill slugs.

## Publication Build

The build is a deterministic transformation from `docs/site/` plus the sibling
`skills/` and selected root `assets/` files to `docs/site/build/site/`. It validates the
data model, generated route set, relative links, and logo assets before the
artifact is uploaded to GitHub Pages.
