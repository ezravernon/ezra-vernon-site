# Ezra Vernon — personal site

React + Vite + Tailwind CSS v4. Originally scaffolded in Figma Make; this
version has the Figma-specific build plugins removed so it can be built and
hosted anywhere as a plain static site.

## Local development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

Outputs static files to `dist/`.

## Deploying with a custom domain (ezravernon.ca)

Your domain is registered through Wix, but Wix's own hosting only serves
sites built in the Wix editor — it can't run this Vite/React project
directly. The straightforward path:

1. Host the static site for free on **Vercel** or **Netlify** (both build
   this project automatically — Vercel picks up `vercel.json` in this repo).
2. Point `ezravernon.ca` at that host by changing its DNS, while keeping the
   domain registered at Wix:
   - **Vercel**: in your Wix domain's DNS settings, add the A/CNAME records
     Vercel gives you when you add the domain in your Vercel project
     settings (usually an A record to `76.76.21.21` for the root domain and
     a CNAME for `www`).
   - **Netlify**: same idea — add the domain in Netlify's site settings and
     it'll give you the exact records to add in Wix's DNS panel.
3. DNS changes can take up to ~24-48 hours to propagate, though it's often
   much faster.

### Option: keep it on Wix instead
If you'd rather everything live in Wix, you'd need to rebuild the design
inside the Wix editor (or use Wix's "Velo"/custom-code embed for parts of
it) — Wix can't run this React project as-is. Vercel/Netlify + Wix-for-DNS
is the simplest way to keep your existing code.

## Notes on this port

- `src/imports/DSCN1352.jpeg` (Ezra Tracker page background) was resized
  from its original 4608×3456 down to 1920px wide and re-compressed
  (~625KB, down from ~6.7MB) so the page doesn't ship a multi-megabyte
  background image.
- The "sign in" password gate uses a plaintext password (`SECRET_PASSWORD`
  in `src/App.tsx`, currently `"changeme"`) checked in the browser. This is
  fine for a soft "just for fun" gate, but it's visible to anyone who reads
  the site's JavaScript — don't use it to protect anything sensitive.
- The Google Calendar embed and Unsplash background image on the Quotes
  page are unchanged from the original.
