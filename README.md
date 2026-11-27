# aae-site

A reader who wants to learn the ArcavenAE projects has to hunt through each repository's README to find guides and references. This repository is the documentation site that gathers them in one place.

Status: first slice. It is an [Astro Starlight](https://starlight.astro.build) site with one step-through page, the generated marvel command reference, and `llms.txt`. More projects land by PR.

## Layout

- `src/content/docs/`: the pages. `e1-tour.md` is the step-through; `reference/` is generated.
- `public/llms.txt`: a plain list of the pages for tools and agents. Generated with the reference.
- `reference-source.txt`: the marvel commit the reference was copied from.
- `scripts/sync-marvel-reference.py`: copies marvel's `docs/reference/` into `src/content/docs/reference/`, adds the front matter Starlight needs, and rewrites `llms.txt`.

## Refresh the reference

```sh
python3 scripts/sync-marvel-reference.py <path-to-marvel-checkout>
```

Run it against a marvel checkout at the commit you want, then commit the result. The script uses only the standard library.

## Build

The site builds in CI (`.github/workflows/site.yml`) on every pull request and on main. The build checks internal links and dry-runs the deploy without a token. Do not run `npm` on a fleet host; build on a machine that is not part of the agent fleet, or read the CI result. CI installs from the committed `package-lock.json` with `npm ci`, so a dependency change needs a matching lockfile made off the fleet. Both jobs block outbound traffic except the hosts the workflow lists, so a new host needs a change there.

## Deploy

The same workflow publishes the built site to <https://docs.darkatelier.org> as a static-assets Cloudflare Worker named `aae-site` (`wrangler.jsonc`). The deploy job runs only from main, on a push or a manual run, and only while the repository variable `CF_READY` is `true`. It uses the `production` environment, the secret `CLOUDFLARE_API_TOKEN` and the variable `CLOUDFLARE_ACCOUNT_ID`. The build job packs its installed `node_modules` for it, so the deploy job installs nothing. The `wrangler` version in `package.json` and `wranglerVersion` in the workflow must match.

## Not here yet

Media hosting and pull request previews are not set up.

## Theme

The look is dark only (the theme picker is removed and `astro.config.mjs` forces the dark attribute). Tokens and the type rules are in `src/styles/aae.css`. The favicon, `public/favicon.svg`, is a plain SVG monogram; no logo PNG is stored or served here. The wordmark face is Montserrat 500, fetched by the CI build from a pinned URL into `public/fonts/` together with its OFL license text, and checked against a pinned sha256. The files are not committed. The wordmark falls back to the system sans stack only if the font file is missing.
