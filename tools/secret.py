#!/usr/bin/env python3
"""The secret section of the site. Full guide: tools/SECRET.md.

  python3 tools/secret.py build              # tools/secret/entries.json -> site/data/secret.json, with a NEW password
  python3 tools/secret.py add-photo IMG [caption...]
                                             # encrypt one photo into site/data/secret/p/<id>.bin and print its
                                             # "Photo keys" line for the Notion entry
  python3 tools/secret.py demo               # write a sample tools/secret/entries.json (for testing the layout)

`build` prints the new password on the last line ("PASSWORD: ...") and also writes it to tools/secret/PASSWORD.
Set SECRET_PASSWORD to rebuild with a specific password instead of a new one (testing only; the weekly update rotates).
tools/secret/ is git-ignored: nothing in it is ever committed.

Crypto (matches the browser code in build.py):
  page:   PBKDF2-SHA256(password, salt, 600k) -> 256-bit key -> AES-256-GCM(html). Stored in site/data/secret.json.
  photos: each photo has its own random 256-bit key, AES-256-GCM. File = 12-byte IV || ciphertext+tag.
          The keys live only in Notion ("Photo keys") and inside the encrypted page, so photos can only be
          viewed after unlocking. Photos never need re-encrypting when the password rotates.
"""
import base64, datetime as dt, html, io, json, os, pathlib, re, secrets, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
WORK = TOOLS / "secret"
ENTRIES = WORK / "entries.json"
OUT = ROOT / "site" / "data" / "secret.json"
PHOTOS = ROOT / "site" / "data" / "secret" / "p"
ITER = 600_000
WORDS = 4

# Tabs, in order. Any other "Section" value found in Notion gets its own tab automatically, after these.
SECTIONS = ["Summit log", "Dreams", "Notes", "Wishlist", "Gear"]
EMPTY = {
    "Summit log": "No summits published yet. Add a row in the Notion Summit Log with Section “Summit log” and tick Publish.",
    "Notes": "No notes yet. Add a row with Section “Notes”.",
    "Wishlist": "Nothing on the wishlist yet. Add a row with Section “Wishlist” for routes you’re scouting.",
    "Gear": "No gear notes yet. Add a row with Section “Gear”.",
}
# The four peaks on the public Dreams page (same order)
DREAMS = [("Tetrahedron Peak", "1,739 m · Tetrahedron"), ("Mount Drew", "2,608 m · Squamish"),
          ("Mount Tantalus", "2,603 m · Tantalus Range"), ("Mount Churchill", "No recorded climbs")]
# COROS sport codes that can be a summit day (outdoor, on foot or ski)
SUMMIT_SPORTS = {100: "Run", 102: "Trail run", 103: "Mountain climb", 104: "Hike", 500: "Ski", 501: "Ski touring", 900: "Walk"}

b64 = lambda b: base64.b64encode(b).decode()
esc = lambda s: html.escape(str(s or ""), quote=True)


# ------------------------------------------------------------------ crypto
def page_key(password, salt, iterations=ITER):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations).derive(password.encode())


def new_password():
    words = [w.strip() for w in (TOOLS / "wordlist.txt").read_text().split() if w.strip()]
    rng = secrets.SystemRandom()
    return "-".join(rng.choice(words) for _ in range(WORDS))


def encrypt_page(markup, password):
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    ct = AESGCM(page_key(password, salt)).encrypt(iv, markup.encode(), None)
    return {"v": 2, "kdf": "PBKDF2-SHA256", "iter": ITER, "salt": b64(salt), "iv": b64(iv), "ct": b64(ct)}


# ------------------------------------------------------------------ photos
def add_photo(path, caption=""):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")   # fix rotation; convert() drops EXIF/GPS
    im.thumbnail((1800, 1800))
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=80, method=6)
    pid, key, iv = secrets.token_hex(8), AESGCM.generate_key(256), secrets.token_bytes(12)
    PHOTOS.mkdir(parents=True, exist_ok=True)
    (PHOTOS / f"{pid}.bin").write_bytes(iv + AESGCM(key).encrypt(iv, buf.getvalue(), None))
    caption = " ".join(caption.split())
    line = f"{pid} {b64(key)} {im.width}x{im.height}" + (f" {caption}" if caption else "")
    print(line)
    return line


def parse_photo_keys(text):
    out = []
    for raw in (text or "").splitlines():
        parts = raw.strip().split(" ", 3)
        if len(parts) >= 3 and re.fullmatch(r"[0-9a-f]{16}", parts[0]) and re.fullmatch(r"\d+x\d+", parts[2]):
            if (PHOTOS / f"{parts[0]}.bin").exists():
                w, h = parts[2].split("x")
                out.append({"id": parts[0], "key": parts[1], "w": int(w), "h": int(h), "cap": parts[3] if len(parts) > 3 else ""})
            else:
                print(f"warning: photo {parts[0]} is in Notion but site/data/secret/p/{parts[0]}.bin is missing; skipped", file=sys.stderr)
    return out


# ------------------------------------------------------------------ text (Notion markdown subset -> safe HTML)
INLINE_TAGS = {"b": "strong", "strong": "strong", "i": "em", "em": "em", "u": "u", "s": "s", "code": "code", "br": "br"}


def inline(s):
    s = esc(s)
    # re-allow a few simple inline tags that Notion emits (<b>, <i> ...); attributes are never allowed
    s = re.sub(r"&lt;(/?)(b|strong|i|em|u|s|code)&gt;", lambda m: f"<{m.group(1)}{INLINE_TAGS[m.group(2)]}>", s)
    s = re.sub(r"&lt;br\s*/?&gt;", "<br>", s)
    s = re.sub(r"&lt;/?[a-zA-Z][^&]*?&gt;", "", s)                                  # drop any other tag
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"~~(.+?)~~", r"<s>\1</s>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    def link(m):
        url = html.unescape(m.group(2))
        if not re.match(r"https?://|mailto:", url):
            return m.group(1)
        return f'<a href="{esc(url)}" rel="noopener noreferrer" target="_blank">{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)


def markdown(md):
    out, para, lst = [], [], None
    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + "<br>".join(inline(x) for x in para) + "</p>"); para = []
        if lst:
            out.append(f"<{lst[0]}>" + "".join(f"<li>{inline(x)}</li>" for x in lst[1]) + f"</{lst[0]}>"); lst = None
    for raw in (md or "").replace("\r", "").split("\n"):
        line = raw.strip()
        line = re.sub(r"^<(?:/?(?:details|summary|callout|columns|column|toggle)[^>]*)>\s*", "", line)   # unwrap Notion blocks
        if not line or line in {"<empty-block/>", "---"}:
            flush()
            if line == "---": out.append("<hr>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush(); lvl = min(len(m.group(1)) + 1, 4)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); continue
        m = re.match(r"^(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?(.*)", line)
        if m:
            kind = "ol" if line[0].isdigit() else "ul"
            if para: flush()
            if not lst or lst[0] != kind:
                flush(); lst = (kind, [])
            lst[1].append(m.group(1)); continue
        if line.startswith(">"):
            flush(); out.append(f"<blockquote>{inline(line.lstrip('> '))}</blockquote>"); continue
        if lst: flush()
        para.append(line)
    flush()
    return "\n".join(out)


# ------------------------------------------------------------------ COROS join
def coros_by_date():
    days = {}
    tsv = TOOLS / "coros" / "activities.tsv"
    for raw in tsv.read_text(encoding="utf-8").splitlines():
        c = raw.split("\t")
        if len(c) < 5 or not re.match(r"\d{4}-\d{2}-\d{2}$", c[0]):
            continue
        try:
            code = int(c[1])
        except ValueError:
            continue
        if code not in SUMMIT_SPORTS:
            continue
        secs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(c[2].split(":")))) if re.fullmatch(r"[\d:]+", c[2]) else 0
        a = {"sport": SUMMIT_SPORTS[code], "time": c[2], "dist": "" if c[3] == "-" else c[3], "hr": c[4], "secs": secs}
        if c[0] not in days or secs > days[c[0]]["secs"]:   # the longest summit-type activity that day
            days[c[0]] = a
    return days


# ------------------------------------------------------------------ rendering
def nice_date(d):
    try:
        x = dt.date.fromisoformat((d or "")[:10])
        return f"{x:%b} {x.day}, {x.year}"
    except ValueError:
        return ""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "section"


def photos_html(ps):
    if not ps:
        return ""
    figs = []
    for p in ps:
        cap = f"<figcaption>{esc(p['cap'])}</figcaption>" if p["cap"] else ""
        figs.append(f'<figure class="v-photo"><div class="v-frame" style="aspect-ratio:{p["w"]}/{p["h"]}">'
                    f'<img data-p="{p["id"]}" data-k="{esc(p["key"])}" width="{p["w"]}" height="{p["h"]}" alt="{esc(p["cap"]) or "Photo"}"></div>{cap}</figure>')
    cls = "v-photos v-photos--one" if len(ps) == 1 else "v-photos"
    return f'<div class="{cls}">{"".join(figs)}</div>'


def summit_html(e, coros):
    meta = [("Elevation", f"{e['elevation']:,.0f} m" if isinstance(e.get("elevation"), (int, float)) else ""),
            ("Route", e.get("route")), ("Partners", e.get("partners")), ("Conditions", e.get("conditions")), ("Rating", e.get("rating"))]
    dl = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in meta if v)
    sub = " · ".join(x for x in [nice_date(e.get("date")), esc(e.get("range"))] if x)
    a = coros.get((e.get("date") or "")[:10])
    watch = ""
    if a:
        bits = [a["sport"], a["time"], a["dist"], f"{a['hr']} bpm avg" if a["hr"] and a["hr"] != "-" else ""]
        watch = f'<p class="v-watch"><span>From the watch</span>{" · ".join(esc(b) for b in bits if b)}</p>'
    dream = f'<span class="v-badge">Dream peak</span>' if e.get("dream") else ""
    return f"""<article class="v-entry" id="{esc(e['anchor'])}">
  <p class="eyebrow">{sub}</p>
  <h2>{esc(e['name'])}{dream}</h2>
  {f'<dl class="v-meta">{dl}</dl>' if dl else ''}
  {watch}
  {photos_html(e['photos'])}
  <div class="v-body">{markdown(e.get('body_md'))}</div>
</article>"""


def note_html(e):
    d = nice_date(e.get("date"))
    return f"""<article class="v-entry v-entry--note" id="{esc(e['anchor'])}">
  {f'<p class="eyebrow">{d}</p>' if d else ''}
  <h2>{esc(e['name'])}</h2>
  {photos_html(e['photos'])}
  <div class="v-body">{markdown(e.get('body_md'))}</div>
</article>"""


def render(entries):
    coros = coros_by_date()
    for i, e in enumerate(entries):
        e["section"] = (e.get("section") or "Summit log").strip()
        e["anchor"] = f"e-{slug(e.get('name') or 'entry')}-{i}"
        e["photos"] = parse_photo_keys(e.get("photo_keys"))
    entries.sort(key=lambda e: e.get("date") or "", reverse=True)
    sections = SECTIONS + sorted({e["section"] for e in entries} - set(SECTIONS))
    summits = [e for e in entries if e["section"] == "Summit log"]

    panels = []
    for s in sections:
        sid = "v-" + slug(s)
        if s == "Dreams":
            rows = []
            for name, sub in DREAMS:
                done = sorted((e for e in summits if e.get("dream") == name), key=lambda e: e.get("date") or "")
                if done:
                    last = done[-1]
                    when = nice_date(last.get("date")) or "Summited"
                    extra = f" · {len(done)} times" if len(done) > 1 else ""
                    status = f'<a href="#{esc(last["anchor"])}" data-goto="v-summit-log">{when}{extra}</a>'
                else:
                    status = "Not yet"
                rows.append(f'<li class="{"is-done" if done else ""}"><span class="v-check" aria-hidden="true"></span>'
                            f'<div><b>{name}</b><span>{sub}</span></div><em>{status}</em></li>')
            n = sum(1 for name, _ in DREAMS if any(e.get("dream") == name for e in summits))
            body = (f'<p class="eyebrow">Dreams</p><h1>{n} of {len(DREAMS)}.</h1>'
                    f'<p class="lede">The four peaks from the Dreams page. A climb counts once its Summit log entry has “Dream peak” set.</p>'
                    f'<ul class="v-dreams">{"".join(rows)}</ul>')
        else:
            items = [e for e in entries if e["section"] == s]
            if s == "Summit log":
                head = (f'<p class="eyebrow">Summit log</p><h1>Summits.</h1>'
                        f'<p class="lede">{len(items)} logged{", newest first" if len(items) > 1 else ""}.</p>' if items else
                        '<p class="eyebrow">Summit log</p><h1>Summits.</h1>')
                inner = "".join(summit_html(e, coros) for e in items)
            else:
                head = f'<p class="eyebrow">{esc(s)}</p><h1>{esc(s)}.</h1>'
                inner = "".join(note_html(e) for e in items)
            body = head + (inner or f'<p class="v-empty">{esc(EMPTY.get(s, "Nothing here yet."))}</p>')
        panels.append(f'<section class="v-panel" id="{sid}" data-panel{"" if s == sections[0] else " hidden"}>{body}</section>')

    tabs = "".join(f'<button type="button" class="v-tab" data-tab="v-{slug(s)}" aria-selected="{"true" if s == sections[0] else "false"}">{esc(s)}</button>'
                   for s in sections)
    stamp = f"{dt.date.today():%b} {dt.date.today().day}, {dt.date.today().year}"
    return (f'<nav class="v-tabs" aria-label="Secret sections">{tabs}</nav>\n' + "\n".join(panels) +
            f'\n<p class="v-stamp">Updated {stamp}. The password changes every Saturday.</p>')


# ------------------------------------------------------------------ commands
def build():
    data = json.loads(ENTRIES.read_text(encoding="utf-8"))
    entries = [e for e in data.get("entries", []) if e.get("name")]
    markup = render(entries)
    password = os.environ.get("SECRET_PASSWORD") or new_password()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(encrypt_page(markup, password)) + "\n")
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "preview.html").write_text(markup, encoding="utf-8")
    (WORK / "PASSWORD").write_text(password + "\n")
    counts = {}
    for e in entries:
        counts[e["section"]] = counts.get(e["section"], 0) + 1
    print("entries:", json.dumps(counts), "| photos:", sum(len(e["photos"]) for e in entries))
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"PASSWORD: {password}")


DEMO = {"entries": [
    {"name": "Mount Arrowsmith", "section": "Summit log", "date": "2026-08-16", "elevation": 1819, "range": "Vancouver Island Ranges",
     "route": "Judges Route", "partners": "Two friends", "conditions": "Clear, light wind", "rating": "★★★★", "dream": "",
     "photo_keys": "", "body_md": "Sample entry to preview the layout.\n\n## The day\n\nStarted at **5 am**, gully was still frozen.\n\n- Snow in the upper gully\n- Summit by 11"},
    {"name": "Tetrahedron Peak", "section": "Summit log", "date": "2025-07-20", "elevation": 1739, "range": "Tetrahedron",
     "route": "", "partners": "", "conditions": "", "rating": "★★★★★", "dream": "Tetrahedron Peak", "photo_keys": "",
     "body_md": "Sample entry. The S-4.1 scramble near the top."},
    {"name": "Rack list for the Tantalus trip", "section": "Gear", "date": "2026-11-01", "body_md": "- Glacier kit\n- 2 pickets"},
]}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        build()
    elif cmd == "add-photo" and len(sys.argv) > 2:
        add_photo(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "demo":
        WORK.mkdir(parents=True, exist_ok=True); ENTRIES.write_text(json.dumps(DEMO, indent=1, ensure_ascii=False)); print(f"wrote {ENTRIES}")
    else:
        sys.exit(__doc__)
