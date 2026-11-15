# ezra-vernon-site

Ezra Vernon's personal site: plain static HTML, no build step on Vercel.

- `site/` — what Vercel serves: `index.html` (Home), `dreams.html`, `sidequests.html`, `quotes.html`, `training.html`, `socials.html`, `404.html`, the policy pages (`privacy.html`, `terms.html`, `cookies.html`, `accessibility.html`), `images/`, `data/activities.json`. Editing notes are in the comment at the top of `site/index.html`.
- Secret section: "Sign in" in the menu opens a password prompt that decrypts `site/data/secret.json` (Summit log and more, from Ezra's Notion). The password rotates every Saturday; see `tools/SECRET.md`.
- `tools/` — the generator (`build.py`, `build_training.py`) and the COROS activity data (`coros/activities.tsv`). Run `python3 tools/build.py` to regenerate `site/`. Weekly Training updates follow `tools/UPDATING.md`.

- Policies: the Privacy, Terms, Cookie and Accessibility pages are written in `tools/build.py` (the LEGAL block) and linked from every footer. They describe the site as it is now: no cookies, no analytics, no forms. If you add analytics, embeds, a contact form or accounts, update those pages first (and the cookie-consent question needs a fresh look).

`vercel.json` turns off the build step and serves `site/` as-is.
