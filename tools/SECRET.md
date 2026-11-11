# The secret section

The "Sign in" button (bottom-right on every page) opens a password prompt. The right password decrypts
`site/data/secret.json` in the browser and shows a full-screen black section with tabs:
**Summit log** (the main one) and **Thoughts**.
Any new "Section" value used in the Summit Log gets its own tab automatically. The old Dreams, Notes, Wishlist and Gear
sections were removed (Nov 2026); rows with those Section values are ignored.

## Where the content lives

**Thoughts** come from Ezra's private Notion database **Thoughts**
(https://app.notion.com/p/8f1a14a9d18d4c81b09a2d993d54ffb6, data source `collection://7b6ff07b-bcd6-48c9-9322-988d9c43e6cb`).
Every row is shown unless **Hide** is ticked (no Publish box: anything he writes goes up at the next weekly update).
Name = optional title; Date = date shown (if empty, use the date part of **Created**); page body = the thought.

Everything else comes from Ezra's private Notion database **Summit Log**
(https://app.notion.com/p/d49a6821dca141bbba1928cd9b0fcc8e, data source `collection://e5bd3954-d98e-42e7-90be-964c5ca33205`).

| Property | Use |
|---|---|
| Name | entry title (peak name) |
| Section | Summit log (or a new value = new tab; Notes / Wishlist / Gear are retired and ignored) |
| Publish | only ticked rows go on the site |
| Date | summit day; also used to match a COROS activity |
| Elevation (m), Range / area, Route, Partners, Conditions, Rating | shown on Summit log entries when filled |
| Dream peak | shows a "Dream peak" badge on the entry |
| Photo keys | managed by Claude, one line per photo: `<id> <key> <WxH> <caption>` |
| page body | the write-up (headings, paragraphs, lists, bold/italic, links) |

Nothing from Notion is committed in plain text. The repo is public; only encrypted output is committed.

## Weekly rotation (done by the Saturday scheduled task, every week, even with no new activities)

1. Query the Summit Log data source for rows with Publish ticked. For each, fetch the page and write
   `tools/secret/entries.json`:
   ```json
   {"entries": [{"name": "...", "section": "Summit log", "date": "2026-08-16", "elevation": 1819,
     "range": "...", "route": "...", "partners": "...", "conditions": "...", "rating": "★★★★",
     "dream": "Tetrahedron Peak", "photo_keys": "<the Photo keys text, as is>", "body_md": "<page content, as is>"}]}
   ```
   Use "" for empty text fields and null for an empty elevation/date. Copy values exactly; don't rewrite Ezra's text.
   Then query ALL rows of the **Thoughts** data source where Hide is not ticked, fetch each page, and append to the same
   `entries` list: `{"name": "<Name or \"\">", "section": "Thoughts", "date": "<Date, else Created, as YYYY-MM-DD>", "body_md": "<page content, as is>"}`.
   Untitled thoughts are fine; empty pages are skipped.
2. `python3 tools/secret.py build` — renders the section, encrypts it with a **new** 4-word password,
   and prints `PASSWORD: word-word-word-word` (also in `tools/secret/PASSWORD`).
3. Commit `site/data/secret.json` (and nothing from `tools/secret/`). Report the password at the top of the recap.

Watch stats: for each Summit log entry, the longest outdoor on-foot/ski activity in `tools/coros/activities.tsv`
on the same date is shown as "From the watch" (sport, time, distance, average heart rate).

## Adding photos (in a chat with Claude; Notion photo files can't be downloaded by the cloud update)

1. Ezra sends the photos in a chat and says which entry they belong to.
2. For each: `python3 tools/secret.py add-photo <file> <caption>` — strips EXIF/GPS, resizes to 1800 px, converts to
   WebP, encrypts it with its own random key into `site/data/secret/p/<id>.bin`, and prints the Photo keys line.
3. Append the printed line(s) to that entry's **Photo keys** property in Notion, and commit/push the `.bin` file(s).
   The photo appears at the next weekly rotation (or run the rotation right away and give Ezra the new password).

Photos are only decryptable with keys that live in Notion and inside the encrypted page, so they don't need
re-encrypting when the password changes. To remove a photo: delete its line in Notion and its `.bin` file.

## Security notes

- Page: PBKDF2-SHA256 (600k iterations) -> AES-256-GCM. A wrong password just fails to decrypt; no hash is stored.
- Passwords: 4 words from the EFF long wordlist (`tools/wordlist.txt`, words of 4–8 letters; EFF, CC BY 3.0), about 50 bits.
- Old versions of `secret.json` stay in git history; an old password only opens the content as it was that week.
- After unlocking, the page key is kept in `sessionStorage` until the tab closes or "Lock" is pressed.
- `python3 tools/secret.py demo` writes sample entries for testing the layout; never commit a build made from it.
