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
- `getting-started.html`: installation, agent portability, local preview, and
  public-vs-harness boundary.
- `skills/index.html`: grouped catalog.
- `skills/<slug>.html`: generated detail pages for every Published Skill.
- `404.html`: branded fallback for invalid routes.

## Publication Build

The build is a deterministic transformation from `docs/site/` plus the sibling
`skills/` and selected root `assets/` files to `docs/site/build/site/`. It validates the
data model, generated route set, relative links, and logo assets before the
artifact is uploaded to GitHub Pages.
