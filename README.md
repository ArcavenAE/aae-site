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

The site builds in CI (`.github/workflows/build.yml`). Do not run `npm` on a fleet host; build on a machine that is not part of the agent fleet, or read the CI result. CI installs from the committed `package-lock.json` with `npm ci`, so a dependency change needs a matching lockfile made off the fleet.

## Not here yet

The site address, hosting and media are not set up. `astro.config.mjs` sets no `site` or `base` until the address is chosen.

## Theme

The look is dark only (the theme picker is removed and `astro.config.mjs` forces the dark attribute). Tokens and the type rules are in `src/styles/aae.css`. The raven and trace art in `src/assets/` and `public/favicon.svg` is drawn as plain SVG; no logo PNG is stored or served here. The wordmark face is Montserrat 500, fetched by the CI build from a pinned URL into `public/fonts/` together with its OFL license text, and checked against a pinned sha256. The files are not committed. Until they are pinned and present, the wordmark falls back to the system sans stack.
