# The Thoughts page (public)

`site/thoughts.html` is a PUBLIC page, built by `python3 tools/build.py` from `tools/thoughts/thoughts.json`
(committed, plain text). It moved out of the secret section on Nov 19, 2026.

## Where the content lives

Ezra's Notion database **Thoughts**
(https://app.notion.com/p/8f1a14a9d18d4c81b09a2d993d54ffb6, data source `collection://7b6ff07b-bcd6-48c9-9322-988d9c43e6cb`).
Every row is published unless **Hide** is ticked. Name = optional title; Date = date shown (if empty, the date part of
**Created**, America/Vancouver); page body = the thought.

## Weekly update (done by the Saturday scheduled task)

1. Query ALL rows of the Thoughts data source where Hide is not ticked. Never include a row with Hide ticked:
   the repo and the page are public.
2. Fetch each page and write `tools/thoughts/thoughts.json`, replacing its contents:
   ```json
   {"thoughts": [{"name": "Life", "date": "2026-11-19", "body_md": "<page content, as is>"}]}
   ```
   Copy the text exactly; don't rewrite Ezra's words. Skip pages with no content. A thought whose Hide box was ticked
   since last week simply drops out.
3. `python3 tools/build.py`, then commit `tools/thoughts/thoughts.json` and `site/thoughts.html`.

Formatting: headings, paragraphs, lists, bold/italic, links and quotes work. Notion's double line breaks become paragraphs.
