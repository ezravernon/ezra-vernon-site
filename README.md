# ezra-vernon-site

Ezra Vernon's personal site: plain static HTML, no build step on Vercel.

- `site/` — what Vercel serves: `index.html` (Home), `dreams.html`, `sidequests.html`, `quotes.html`, `training.html`, `socials.html`, `404.html`, `images/`, `data/activities.json`. Editing notes are in the comment at the top of `site/index.html`.
- `tools/` — the generator (`build.py`, `build_training.py`) and the COROS activity data (`coros/activities.tsv`). Run `python3 tools/build.py` to regenerate `site/`. Weekly Training updates follow `tools/UPDATING.md`.

`vercel.json` turns off the build step and serves `site/` as-is.
