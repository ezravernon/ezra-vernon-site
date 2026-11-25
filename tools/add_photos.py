"""Add photos to the Home page gallery.

    python3 tools/add_photos.py PHOTO [PHOTO ...] [--alt "description" ...] [--caption "text" ...]

Each photo is resized to 800px and 1600px wide WebP copies in site/images/gallery/ and added to the
END of site/data/gallery.json (newest last). --alt / --caption values are matched to photos in order;
every photo should get an --alt (what's in the picture) for screen readers. Then run tools/build.py.
To reorder or remove photos, edit site/data/gallery.json (and delete the matching files).
"""
import argparse, json, pathlib, re
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "images" / "gallery"
DATA = ROOT / "site" / "data" / "gallery.json"

ap = argparse.ArgumentParser()
ap.add_argument("photos", nargs="+")
ap.add_argument("--alt", action="append", default=[])
ap.add_argument("--caption", action="append", default=[])
a = ap.parse_args()

data = json.loads(DATA.read_text()) if DATA.exists() else {"photos": []}
used = {p["src"] for p in data["photos"]}
OUT.mkdir(parents=True, exist_ok=True)
for i, path in enumerate(a.photos):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    base = re.sub(r"[^a-z0-9]+", "-", pathlib.Path(path).stem.lower()).strip("-") or "photo"
    name, n = base, 2
    while name in used:
        name, n = f"{base}-{n}", n + 1
    used.add(name)
    for w in (800, 1600):
        c = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        c.save(OUT / f"{name}-{w}.webp", "WEBP", quality=80, method=6)
    data["photos"].append({"src": name, "w": im.width if im.width < 1600 else 1600,
                           "h": round(im.height * min(1, 1600 / im.width)),
                           "alt": a.alt[i] if i < len(a.alt) else "",
                           "caption": a.caption[i] if i < len(a.caption) else ""})
    print("added", name)
DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
