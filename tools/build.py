#!/usr/bin/env python3
"""Generates the static pages for ezra-vernon/. The OUTPUT is plain HTML (no build step needed to host it);
this script only exists so the shared header/footer/styles stay byte-identical on every page."""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "site"
PW_HASH = "eb740430888cafad58f8882004534e966e9f13775ecb87450da7d24ac53ce126"

FONTS = ("https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500"
         "&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&display=swap")
QUOTE_FONTS = ("https://fonts.googleapis.com/css2?family=Caveat:wght@500&family=DM+Sans:opsz,wght@9..40,400;9..40,500"
               "&family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&display=swap")

SHARED_CSS = """
/* ===== SHARED STYLES — keep identical on all pages ===== */
:root{
  /* Colour: one neutral base, one dark text colour, one accent */
  --base:#F6F3EE;        /* warm paper off-white */
  --base-deep:#EDE7DE;   /* slightly deeper tint of the base, for alternating sections */
  --ink:#1E2A27;         /* deep pine — main text (13.4:1 on base) */
  --ink-soft:#5B6662;    /* secondary text (5.4:1 on base) */
  --accent:#1A6E6A;      /* deep turquoise — buttons + links only (5.45:1 on base) */
  --line:rgba(30,42,39,.14);
  /* Type: 1.25 modular scale from an 18px body */
  --font-serif:"Fraunces",Georgia,"Times New Roman",serif;
  --font-sans:"DM Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --step--1:0.875rem; --step-0:1.125rem; --step-1:1.406rem; --step-2:1.758rem;
  --step-3:2.197rem; --step-4:2.747rem; --step-5:3.433rem; --step-6:4.292rem;
  /* Spacing: multiples of 8px */
  --s1:8px; --s2:16px; --s3:24px; --s4:32px; --s5:48px; --s6:64px; --s7:96px; --s8:128px;
  --measure:68ch;
  --radius:8px;
  --shadow:0 8px 24px rgba(30,42,39,.08);
  --t-fast:160ms; --t-med:240ms; --t-slow:300ms;
  --ease:cubic-bezier(.2,.7,.2,1);
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--base);color:var(--ink);font-family:var(--font-sans);font-size:var(--step-0);line-height:1.6;text-rendering:optimizeLegibility}
img{max-width:100%;height:auto;display:block}
h1,h2,h3{font-family:var(--font-serif);font-weight:400;line-height:1.1;letter-spacing:-0.015em;margin:0 0 var(--s3)}
h1{font-size:clamp(var(--step-4),6vw,var(--step-6));letter-spacing:-0.025em}
h2{font-size:clamp(var(--step-3),4vw,var(--step-4))}
h3{font-size:var(--step-2);line-height:1.2}
p{margin:0 0 var(--s3);max-width:var(--measure)}
a{color:var(--accent);text-underline-offset:3px;text-decoration-thickness:1px;transition:color var(--t-fast) var(--ease)}
a:hover{color:var(--ink)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px}
.site-header :focus-visible,.hero :focus-visible,.q-head :focus-visible{outline-color:var(--base)}
.eyebrow{font-family:var(--font-sans);font-size:var(--step--1);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 var(--s2)}
.lede{font-size:var(--step-1);line-height:1.5;color:var(--ink)}
.wrap{width:min(1200px,100% - var(--s4));margin-inline:auto}
.section{padding-block:var(--s7)}
.section--tint{background:var(--base-deep)}
.skip{position:absolute;left:var(--s2);top:-80px;background:var(--ink);color:var(--base);padding:var(--s1) var(--s2);border-radius:var(--radius);z-index:100;transition:top var(--t-fast)}
.skip:focus{top:var(--s2)}
/* Buttons — one style everywhere */
.btn{display:inline-flex;align-items:center;gap:var(--s1);font:500 var(--step-0)/1 var(--font-sans);padding:var(--s2) var(--s3);border-radius:var(--radius);background:var(--accent);color:var(--base);text-decoration:none;border:1px solid var(--accent);cursor:pointer;transition:background var(--t-med) var(--ease),color var(--t-med) var(--ease),transform var(--t-med) var(--ease)}
.btn:hover{background:var(--ink);border-color:var(--ink);color:var(--base);transform:translateY(-1px)}
.btn--ghost{background:transparent;color:var(--accent)}
.btn--ghost:hover{background:var(--accent);border-color:var(--accent)}
/* Header + nav */
.site-header{position:sticky;top:0;z-index:20;background:rgba(30,42,39,.96);backdrop-filter:saturate(1.2) blur(8px);border-bottom:1px solid rgba(246,243,238,.08)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);min-height:72px}
.brand{display:flex;align-items:center;gap:var(--s2);text-decoration:none;color:var(--base);font-family:var(--font-serif);font-size:var(--step-1)}
.brand img{width:56px;height:32px}
.nav ul{list-style:none;margin:0;padding:0;display:flex;align-items:center;gap:var(--s4)}
.nav a{color:var(--base);text-decoration:none;font-size:var(--step-0);padding-block:var(--s1);border-bottom:1px solid transparent;transition:border-color var(--t-med) var(--ease),color var(--t-med) var(--ease)}
.nav a:hover,.nav a[aria-current="page"]{border-bottom-color:var(--base)}
.nav a[aria-current="page"]{color:var(--base)}
.brand:hover{color:var(--base)}
.nav .btn{color:var(--base);padding:var(--s1) var(--s3);border-bottom:1px solid var(--accent)}
.nav .btn:hover,.nav .btn[aria-current="page"]{background:var(--base);border-color:var(--base);color:var(--ink)}
.nav-toggle{display:none}
@media (max-width:960px){
  .nav-toggle{display:inline-flex;font:500 var(--step-0)/1 var(--font-sans);background:none;border:1px solid rgba(246,243,238,.3);border-radius:var(--radius);padding:var(--s1) var(--s2);color:var(--base);cursor:pointer}
  .nav{position:absolute;inset:72px 0 auto 0;background:var(--ink);border-bottom:1px solid rgba(246,243,238,.08);display:none}
  .nav.is-open{display:block}
  .no-js .nav{display:block;position:static;border:0}
  .no-js .site-header .wrap{flex-wrap:wrap;padding-block:var(--s2)}
  .nav ul{flex-direction:column;align-items:flex-start;gap:var(--s1);padding:var(--s2) var(--s2) var(--s3)}
  .no-js .nav ul{flex-direction:row;flex-wrap:wrap;padding:0}
}
/* Page header used on inner pages */
.page-head{padding-block:var(--s7) var(--s5)}
.page-head p{font-size:var(--step-1);line-height:1.5}
/* Footer */
.site-footer{border-top:1px solid var(--line);padding-block:var(--s6) var(--s8)}
.site-footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:var(--s3);align-items:center}
.site-footer p{margin:0;color:var(--ink-soft);font-size:var(--step--1)}
.site-footer ul{list-style:none;display:flex;flex-wrap:wrap;gap:var(--s3);margin:0;padding:0;font-size:var(--step--1)}
/* Sign-in corner */
.signin-btn{position:fixed;right:var(--s2);bottom:var(--s2);z-index:30;font:500 var(--step--1)/1 var(--font-sans);padding:var(--s1) var(--s2);border-radius:var(--radius);border:1px solid var(--line);background:var(--base);color:var(--ink-soft);box-shadow:var(--shadow);cursor:pointer;transition:color var(--t-med) var(--ease),border-color var(--t-med) var(--ease)}
.signin-btn:hover{color:var(--accent);border-color:var(--accent)}
.signin-btn[data-state="in"]{color:var(--accent)}
.signin{border:1px solid var(--line);border-radius:var(--radius);padding:var(--s4);width:min(400px,100% - var(--s4));background:var(--base);color:var(--ink);box-shadow:var(--shadow)}
.signin::backdrop{background:rgba(30,42,39,.35)}
.signin h2{font-size:var(--step-2);margin-bottom:var(--s2)}
.field{display:grid;gap:var(--s1);margin-bottom:var(--s3)}
.field label{font-size:var(--step--1);font-weight:500;color:var(--ink-soft);letter-spacing:.04em}
.field input{font:400 var(--step-0)/1.4 var(--font-sans);padding:var(--s2);border:1px solid var(--line);border-radius:var(--radius);background:#fff;color:var(--ink);transition:border-color var(--t-fast)}
.field input:focus-visible{border-color:var(--accent);outline-offset:1px}
.signin-msg{min-height:1.6em;margin:0 0 var(--s2);font-size:var(--step--1);color:var(--ink-soft)}
.signin-actions{display:flex;gap:var(--s2);flex-wrap:wrap}
/* Gentle reveal on scroll (only when JS runs and motion is allowed) */
.js .reveal{opacity:0;transform:translateY(16px);transition:opacity var(--t-slow) var(--ease),transform var(--t-slow) var(--ease)}
.js .reveal.is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js .reveal{opacity:1;transform:none;transition:none}
  *{transition-duration:1ms!important;animation:none!important}
}
"""

SHARED_JS = """
/* ===== SHARED SCRIPT — keep identical on all pages ===== */
(function(){
  var d=document.documentElement; d.classList.remove('no-js'); d.classList.add('js');
  // Mobile nav
  var t=document.querySelector('.nav-toggle'), n=document.getElementById('site-nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('is-open');t.setAttribute('aria-expanded',o)});}
  // Scroll reveal
  var els=document.querySelectorAll('.reveal');
  var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!('IntersectionObserver' in window)||rm){els.forEach(function(e){e.classList.add('is-in')});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});els.forEach(function(e){io.observe(e)});}
  // Simple sign-in. NOTE: this is a static site, so this is a convenience gate only, not real security.
  var HASH='""" + PW_HASH + """';
  var KEY='ev-signed-in', btn=document.querySelector('.signin-btn'), dlg=document.getElementById('signin');
  if(!btn||!dlg)return;
  function get(){try{return sessionStorage.getItem(KEY)==='1'}catch(e){return false}}
  function set(v){try{v?sessionStorage.setItem(KEY,'1'):sessionStorage.removeItem(KEY)}catch(e){}}
  function paint(){var on=get();btn.textContent=on?'Signed in · Ezra':'Sign in';btn.dataset.state=on?'in':'out';d.classList.toggle('is-owner',on)}
  paint();
  var form=dlg.querySelector('form'), msg=dlg.querySelector('.signin-msg'), pw=dlg.querySelector('#signin-pw'),
      out=dlg.querySelector('.signin-out'), sub=dlg.querySelector('.signin-submit'), title=dlg.querySelector('#signin-title');
  function openD(){var on=get();title.textContent=on?'You\\u2019re signed in':'Sign in';pw.parentNode.hidden=on;sub.hidden=on;out.hidden=!on;msg.textContent='';pw.value='';
    if(dlg.showModal)dlg.showModal();else dlg.setAttribute('open','');setTimeout(function(){(on?out:pw).focus()},0)}
  function closeD(){if(dlg.close)dlg.close();else dlg.removeAttribute('open');btn.focus()}
  btn.addEventListener('click',openD);
  dlg.querySelector('.signin-cancel').addEventListener('click',closeD);
  out.addEventListener('click',function(){set(false);paint();closeD()});
  async function sha(s){var b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0')}).join('')}
  form.addEventListener('submit',async function(e){e.preventDefault();
    try{ if(await sha(pw.value)===HASH){set(true);paint();msg.textContent='Welcome back, Ezra.';setTimeout(closeD,600)}
         else{msg.textContent='That password didn\\u2019t match. Try again.';pw.select()} }
    catch(err){msg.textContent='Sign-in needs a secure (https) connection.'}
  });
})();
"""

NAV = [("index.html", "Home"), ("dreams.html", "Dreams"), ("sidequests.html", "Sidequests"), ("quotes.html", "Quotes"), ("training.html", "Training")]


def header(current):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a></li>' for h, l in NAV)
    cur = ' aria-current="page"' if current == "socials.html" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="images/logo-240.webp" width="56" height="32" alt="">Ezra Vernon</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{items}<li><a class="btn" href="socials.html"{cur}>Socials</a></li></ul>
    </nav>
  </div>
</header>"""


FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <p>Ezra Vernon · Live in the balance between two extremes.</p>
    <ul>
      <li><a href="https://www.instagram.com/ezrav_insta" rel="noopener">Instagram</a></li>
      <li><a href="https://ca.linkedin.com/in/ezra-vernon-a98a40343" rel="noopener">LinkedIn</a></li>
      <li><a href="https://strava.app.link/lBou8jZCg7b" rel="noopener">Strava</a></li>
    </ul>
  </div>
</footer>
<button class="signin-btn" type="button" data-state="out" aria-haspopup="dialog">Sign in</button>
<dialog class="signin" id="signin" aria-labelledby="signin-title">
  <form method="dialog" novalidate>
    <h2 id="signin-title">Sign in</h2>
    <div class="field"><label for="signin-pw">Password</label><input id="signin-pw" name="password" type="password" autocomplete="current-password" required></div>
    <p class="signin-msg" role="status" aria-live="polite"></p>
    <div class="signin-actions">
      <button class="btn signin-submit" type="submit">Sign in</button>
      <button class="btn btn--ghost signin-out" type="button" hidden>Sign out</button>
      <button class="btn btn--ghost signin-cancel" type="button">Close</button>
    </div>
  </form>
</dialog>"""

FAVICON = '<link rel="icon" type="image/png" sizes="64x64" href="images/favicon-64.png"><link rel="apple-touch-icon" href="images/apple-touch-icon.png">'


def page(fname, title, desc, body, page_css="", page_js="", fonts=FONTS, top_comment="", jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n' if jsonld else ""
    pjs = f"<script>\n/* ===== PAGE SCRIPT: {fname} ===== */\n{page_js}\n</script>\n" if page_js else ""
    html = f"""<!DOCTYPE html>
{top_comment}<html lang="en-CA" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1E2A27">
<script>document.documentElement.classList.replace('no-js','js')</script>
{FAVICON}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<style>{SHARED_CSS}</style>
<style>
/* ===== PAGE STYLES: {fname} ===== */
{page_css}
</style>
{ld}</head>
<body>
{header(fname)}
<main id="main">
{body}
</main>
{FOOTER}
<script>{SHARED_JS}</script>
{pjs}</body>
</html>
"""
    (OUT / fname).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- HOME
HOME_COMMENT = """<!--
HANDOVER NOTES — Ezra Vernon personal site (v1, 2026-11-08)
Pages: index.html (Home), dreams.html, sidequests.html, quotes.html, training.html, socials.html, 404.html; photos in images/.
Training data: data/activities.json + the log on training.html, generated from Ezra's COROS history (date, sport, time, distance, own titles only;
  no coordinates, place names, heart rate or calories). Refresh by asking Claude to pull new COROS activities.
Hosting plan: GitHub repo -> Vercel -> custom domain (Wix). Plain static HTML, no build step; Vercel serves 404.html automatically.
DESIGN RECIPE "Alpine field notebook": warm paper base, deep pine ink, one deep-turquoise accent (Ezra's favourite colour);
  Fraunces serif headings + DM Sans body; Home has stronger entrance motion (curtain/zoom hero, flying bird, word-by-word mantra); full-bleed meadow hero with text over it, dark header; one calm idea per section; mantra set large and centred.
  Quotes page only adds a third face (Caveat, handwritten) because Ezra asked for multiple font types there.
Colours: base #F6F3EE, tint #EDE7DE, ink #1E2A27, soft ink #5B6662, accent #1A6E6A. Logo pink is used only inside the logo image.
How to edit: the "SHARED STYLES" and "SHARED SCRIPT" blocks, header, footer and sign-in dialog must stay identical on every page.
  Page-specific CSS sits in the "PAGE STYLES" block. Change the nav/footer on every page.
Photos: meadow-{600,900,1220}.webp (Home hero background), meadow-wide-{800,1220}.webp (Dreams header), heather-{480,758}.webp (Quotes header background),
  frisbee-{800,1400}.webp (Home photos; credit Dan Tsuji Photography), car-{600,1000}.webp + belay-{600,1000}.webp (Home photos),
  logo-{240,480,960}.webp (header + Socials), favicon-64.png, apple-touch-icon.png. All EXIF stripped.
  To add/swap a photo: convert to WebP, strip metadata, export the same widths, update width/height/srcset/alt.
Sign-in: bottom-right button. The password is checked against a SHA-256 hash in the shared script; on a static site this is
  NOT real security (anyone can read the code), so never put private content behind it.
-->
"""

home_css = """
.hero{position:relative;min-height:min(88vh,880px);display:flex;align-items:flex-end;overflow:hidden;background:var(--ink);color:var(--base)}
.hero-bg{position:absolute;inset:0;margin:0}
.hero-bg img{width:100%;height:100%;object-fit:cover;object-position:50% 15%;transform:scale(1.1)}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,42,39,.1) 0%,rgba(30,42,39,.25) 30%,rgba(30,42,39,.72) 52%,rgba(30,42,39,.9) 68%,rgba(30,42,39,.92) 100%);pointer-events:none}
.hero .wrap{position:relative;z-index:1;padding-block:var(--s8) var(--s7)}
.hero h1{color:var(--base);margin-bottom:var(--s3);text-shadow:0 2px 24px rgba(30,42,39,.35)}
.hero .eyebrow{color:var(--base)}
.hero .lede{color:var(--base);margin:0;max-width:34ch}
.welcome{padding-bottom:var(--s5)}
.welcome h2{font-size:clamp(var(--step-4),6vw,var(--step-5))}
/* Photo strip below the welcome */
.photos{padding-top:0}
.photo-grid{display:grid;gap:var(--s3);grid-template-columns:1fr}
@media (min-width:760px){.photo-grid{grid-template-columns:1fr 1fr}.photo-grid .wide{grid-column:1 / -1}}
.photo{margin:0}
.photo .frame{overflow:hidden;border-radius:var(--radius);background:var(--base);aspect-ratio:3/4}
.photo.wide .frame{aspect-ratio:3/2}
.photo img{width:100%;height:100%;object-fit:cover;transition:transform var(--t-slow) var(--ease)}
.photo:hover img{transform:scale(1.03)}
.photo figcaption{margin-top:var(--s1);font-size:var(--step--1);color:var(--ink-soft)}
.about .wrap{display:grid;gap:var(--s4)}
@media (min-width:900px){.about .wrap{grid-template-columns:1fr 2fr;gap:var(--s7)}}
.sports{list-style:none;padding:0;margin:var(--s4) 0 0;display:flex;flex-wrap:wrap;gap:var(--s1)}
.sports li{border:1px solid var(--line);border-radius:999px;padding:var(--s1) var(--s2);font-size:var(--step--1)}
.sports li:first-child{border-color:var(--accent);color:var(--accent)}
.facts{display:grid;gap:var(--s4);margin:var(--s5) 0 0;grid-template-columns:1fr}
@media (min-width:760px){.facts{grid-template-columns:repeat(3,1fr)}}
.fact{border-top:1px solid var(--ink);padding-top:var(--s3)}
.fact dt{font-size:var(--step--1);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);margin-bottom:var(--s2)}
.fact dd{margin:0;font-family:var(--font-serif);font-size:var(--step-2);line-height:1.2}
.fact dd small{display:block;font-family:var(--font-sans);font-size:var(--step--1);color:var(--ink-soft);margin-top:var(--s1)}
.swatch{display:inline-block;width:24px;height:24px;border-radius:50%;background:#3FC1B5;vertical-align:-3px;margin-left:var(--s1);border:1px solid var(--line)}
.mantra{padding-block:var(--s8);text-align:center}
.mantra .eyebrow{margin-bottom:var(--s4)}
.mantra blockquote{margin:0 auto;max-width:18ch;font-family:var(--font-serif);font-style:italic;font-size:clamp(var(--step-4),7vw,var(--step-6));line-height:1.08;letter-spacing:-0.02em}
.mantra .rule{width:64px;height:1px;background:var(--accent);margin:var(--s5) auto 0;border:0}
.paths{display:grid;gap:var(--s3);grid-template-columns:1fr;margin-top:var(--s5)}
@media (min-width:760px){.paths{grid-template-columns:repeat(3,1fr)}}
.path{display:block;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:var(--radius);padding:var(--s4);background:var(--base);transition:border-color var(--t-med) var(--ease),transform var(--t-med) var(--ease),box-shadow var(--t-med) var(--ease)}
.path:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:var(--shadow);color:var(--ink)}
.path h3{margin-bottom:var(--s1)}
.path p{margin:0;color:var(--ink-soft);font-size:var(--step-0)}
.path span{display:inline-block;margin-top:var(--s2);color:var(--accent);font-weight:500}

/* ===== STRONGER MOTION — Home only (Ezra asked for more obvious animation here) ===== */
@media (prefers-reduced-motion:no-preference){
  .js .reveal{transform:translateY(48px);transition:opacity 700ms var(--ease),transform 700ms var(--ease)}
  .js .reveal.is-in{transform:none}
  /* Hero: headline lines rise in one after another */
  .js .hero .reveal{transform:none}
  .js .hero .reveal > *{opacity:0;transform:translateY(40px);transition:opacity 800ms var(--ease),transform 800ms var(--ease)}
  .js .hero .reveal.is-in > *{opacity:1;transform:none}
  .js .hero .reveal > :nth-child(2){transition-delay:150ms}
  .js .hero .reveal > :nth-child(3){transition-delay:300ms}

  /* Hero background: fades up from dark with a slow zoom-out, then parallax on scroll */
  .js .hero-bg{opacity:0;transition:opacity 1200ms var(--ease)}
  .js .hero-bg.is-in{opacity:1}
  .js .hero-bg img{transform:translateY(var(--py,0px)) scale(var(--sc,1.25));transition:transform 2200ms var(--ease);will-change:transform}
  .js .hero-bg.is-in img{--sc:1.1}
  .js .hero-bg.is-settled img{transition:none}
  /* Photos: rise in one after another */
  .js .photo.reveal:nth-child(2){transition-delay:150ms}.js .photo.reveal:nth-child(3){transition-delay:300ms}
  /* About: sport pills and favourites pop in one by one */
  .js .sports li,.js .fact{opacity:0;transform:translateY(24px);transition:opacity 600ms var(--ease),transform 600ms var(--ease)}
  .js .reveal.is-in .sports li,.js .reveal.is-in .fact{opacity:1;transform:none}
  .js .sports li:nth-child(1){transition-delay:200ms}.js .sports li:nth-child(2){transition-delay:280ms}
  .js .sports li:nth-child(3){transition-delay:360ms}.js .sports li:nth-child(4){transition-delay:440ms}
  .js .sports li:nth-child(5){transition-delay:520ms}
  .js .fact:nth-child(1){transition-delay:600ms}.js .fact:nth-child(2){transition-delay:750ms}.js .fact:nth-child(3){transition-delay:900ms}
  .js .swatch{transform:scale(0);transition:transform 500ms cubic-bezier(.3,1.6,.5,1) 1100ms}
  .js .reveal.is-in .swatch{transform:scale(1)}
  /* Mantra: words appear one at a time, then the line draws */
  .js .mantra .reveal{transform:none}
  .js .mantra .w{display:inline-block;opacity:0;transform:translateY(32px);filter:blur(8px);transition:opacity 700ms var(--ease),transform 700ms var(--ease),filter 700ms var(--ease);transition-delay:calc(var(--i) * 110ms + 150ms)}
  .js .mantra .is-in .w{opacity:1;transform:none;filter:none}
  .js .mantra .rule{width:0;transition:width 900ms var(--ease) 1200ms}
  .js .mantra .is-in .rule{width:64px}
  /* Cards: staggered */
  .js .path.reveal:nth-child(2){transition-delay:150ms}.js .path.reveal:nth-child(3){transition-delay:300ms}
}
"""

home_body = """<!-- HERO: photo as background, text over it -->
<section class="hero">
  <figure class="hero-bg">
    <img src="images/meadow-1220.webp" srcset="images/meadow-600.webp 600w, images/meadow-900.webp 900w, images/meadow-1220.webp 1220w"
         sizes="100vw" width="1220" height="1920" fetchpriority="high"
         alt="Alpine meadow full of white wildflowers below dark conifer forest and a rocky summit under a bright blue sky">
  </figure>
  <div class="wrap">
    <div class="reveal">
      <p class="eyebrow">Website designer · Scrambler · Ultra runner</p>
      <h1>Ezra Vernon</h1>
      <p class="lede">Getting outside, exploring, and stepping a little further out of my comfort zone every time.</p>
    </div>
  </div>
</section>

<!-- WELCOME -->
<section class="section welcome section--tint">
  <div class="wrap reveal">
    <h2>Welcome to my page!</h2>
    <p class="lede">A home for everything me.</p>
  </div>
</section>

<!-- PHOTOS -->
<section class="section photos section--tint" aria-label="Photos">
  <div class="wrap photo-grid">
    <figure class="photo wide reveal">
      <div class="frame"><img src="images/frisbee-1400.webp" srcset="images/frisbee-800.webp 800w, images/frisbee-1400.webp 1400w" sizes="(min-width:1240px) 1200px, 100vw"
        width="1400" height="934" loading="lazy" alt="Ultimate frisbee game on turf: a player in a white bucket hat and sunglasses lunges sideways to mark a thrower"></div>
    </figure>
    <figure class="photo reveal">
      <div class="frame"><img src="images/car-1000.webp" srcset="images/car-600.webp 600w, images/car-1000.webp 1000w" sizes="(min-width:760px) 50vw, 100vw"
        width="1000" height="1333" loading="lazy" alt="Car hatchback packed to the roof with backpacks, climbing shoes, a sleeping pad and a blue tarp"></div>
    </figure>
    <figure class="photo reveal">
      <div class="frame"><img src="images/belay-1000.webp" srcset="images/belay-600.webp 600w, images/belay-1000.webp 1000w" sizes="(min-width:760px) 50vw, 100vw"
        width="1000" height="1333" loading="lazy" alt="Close-up of a climber wearing mirrored belay glasses, looking down into the prisms"></div>
    </figure>
  </div>
</section>

<!-- ABOUT ME -->
<section class="section about" id="about">
  <div class="wrap">
    <div class="reveal"><p class="eyebrow">About me</p><h2>Outside, mostly.</h2></div>
    <div class="reveal">
      <p class="lede">I love getting outside, exploring, making new friends, and stepping out of my comfort zone!</p>
      <p>My favourite sport is skiing, but I love ultimate frisbee, soccer, rock climbing, and ultra running as well.</p>
      <ul class="sports" aria-label="Sports I love">
        <li>Skiing — favourite</li><li>Ultimate frisbee</li><li>Soccer</li><li>Rock climbing</li><li>Ultra running</li>
      </ul>
      <dl class="facts">
        <div class="fact"><dt>Favourite ice cream</dt>
          <dd><a href="https://www.benjerry.com/flavors/the-tonight-dough-ice-cream" rel="noopener">The Tonight Dough</a><small>Ben &amp; Jerry’s</small></dd></div>
        <div class="fact"><dt>All-time favourite colour</dt><dd>Turquoise<span class="swatch" aria-hidden="true"></span></dd></div>
        <div class="fact"><dt>Second biggest fear</dt><dd>Darkness</dd></div>
      </dl>
    </div>
  </div>
</section>

<!-- LIFE MANTRA -->
<section class="mantra section--tint" aria-labelledby="mantra-label">
  <div class="wrap reveal">
    <p class="eyebrow" id="mantra-label">Life mantra</p>
    <blockquote><p style="max-width:none;margin:0">Live in the balance between two extremes.</p></blockquote>
    <hr class="rule">
  </div>
</section>

<!-- WHERE TO NEXT -->
<section class="section">
  <div class="wrap">
    <p class="eyebrow reveal">Where to next</p>
    <h2 class="reveal">Plans, quests and late-night thoughts</h2>
    <div class="paths">
      <a class="path reveal" href="dreams.html"><h3>Future dreams</h3><p>Four peaks I want to stand on, from Tetrahedron to Tantalus.</p><span>Dreams →</span></a>
      <a class="path reveal" href="sidequests.html"><h3>Sidequests</h3><p>A 55.8 km Costco hot dog ultra, and learning guitar for camp.</p><span>Sidequests →</span></a>
      <a class="path reveal" href="quotes.html"><h3>Quotes</h3><p>Original daily reminders, mostly written late at night.</p><span>Quotes →</span></a>
    </div>
  </div>
</section>"""


home_js = """(function(){
  if(!window.matchMedia||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  // Mantra: wrap each word so it can animate in
  var q=document.querySelector('.mantra blockquote p');
  if(q){var words=q.textContent.trim().split(/\\s+/);q.setAttribute('aria-label',q.textContent.trim());
    q.innerHTML=words.map(function(w,i){return '<span class="w" aria-hidden="true" style="--i:'+i+'">'+w+'</span>'}).join(' ');}
  // Hero background: reveal on load, then parallax while scrolling
  var fig=document.querySelector('.hero-bg'),img=fig&&fig.querySelector('img');
  if(!fig)return;
  requestAnimationFrame(function(){requestAnimationFrame(function(){fig.classList.add('is-in')})});
  setTimeout(function(){fig.classList.add('is-settled');par()},2300);
  var tick=false,hero=fig.parentNode;
  function par(){var h=hero.offsetHeight,y=Math.min(Math.max(scrollY,0),h);img.style.setProperty('--py',Math.min(y*0.25,h*0.05).toFixed(1)+'px');tick=false}
  addEventListener('scroll',function(){if(fig.classList.contains('is-settled')&&!tick){tick=true;requestAnimationFrame(par)}},{passive:true});
})();"""

page("index.html", "Ezra Vernon — skiing, mountains and side quests",
     "Ezra Vernon's personal site: about me, the mountains I want to climb, side quests like a Costco ultra, and original quotes.",
     home_body, home_css, home_js, top_comment=HOME_COMMENT,
     jsonld={"@context": "https://schema.org", "@type": "Person", "name": "Ezra Vernon",
             "image": "images/meadow-1220.webp",
             "sameAs": ["https://www.instagram.com/ezrav_insta", "https://ca.linkedin.com/in/ezra-vernon-a98a40343"]})

# ---------------------------------------------------------------- DREAMS
dreams_css = """
.banner{margin:0;aspect-ratio:3/2;max-height:72vh;width:100%;overflow:hidden;background:var(--base-deep)}
.banner img{width:100%;height:100%;object-fit:cover;object-position:50% 30%}
@media (min-width:900px){.banner{aspect-ratio:21/9}}
.peaks{display:grid;gap:0}
.peak{display:grid;gap:var(--s3);padding-block:var(--s6);border-top:1px solid var(--line)}
.peak:last-child{border-bottom:1px solid var(--line)}
@media (min-width:900px){.peak{grid-template-columns:96px 1fr 1.6fr;gap:var(--s5);align-items:start}}
.peak .num{font-family:var(--font-serif);font-size:var(--step-3);color:var(--accent);line-height:1}
.peak h2{font-size:var(--step-4);margin-bottom:var(--s2)}
.peak .elev{font-size:var(--step--1);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);margin:0}
.peak .goal{border-left:2px solid var(--accent);padding-left:var(--s2);margin-top:var(--s3)}
.peak ul{padding-left:1.2em;margin:0 0 var(--s3);max-width:var(--measure)}
.peak li{margin-bottom:var(--s1)}
.join{padding-block:var(--s7)}
"""
dreams_body = """<section class="page-head">
  <div class="wrap reveal">
    <p class="eyebrow">Page 02</p>
    <h1>Future dreams</h1>
    <p>All of these are goals that I want to complete. They all have different timelines — feel free to reach out if you want to plan and join me for one of these adventures.</p>
  </div>
</section>
<figure class="banner">
  <img src="images/meadow-wide-1220.webp" srcset="images/meadow-wide-800.webp 800w, images/meadow-wide-1220.webp 1220w" sizes="100vw"
       width="1220" height="813" fetchpriority="high" alt="A rocky summit rising above forested slopes and a wildflower meadow under blue sky">
</figure>

<section class="section" aria-labelledby="mountains">
  <div class="wrap">
    <p class="eyebrow reveal" id="mountains">Mountains</p>
    <div class="peaks">
      <article class="peak reveal">
        <span class="num">01</span>
        <div><h2>Tetrahedron Peak 2.0</h2><p class="elev">1,739 m · highest in the Tetrahedron</p></div>
        <div>
          <ul><li>Features a class S-4.1 scramble near the summit.</li><li>I already summited this once, in summer 2025.</li></ul>
          <p class="goal"><strong>Goal:</strong> a return trip overnight, to witness sunrise or sunset at the top.</p>
        </div>
      </article>
      <article class="peak reveal">
        <span class="num">02</span>
        <div><h2>Mount Drew</h2><p class="elev">2,608 m · Squamish, BC</p></div>
        <div>
          <p>The notorious peak located in Squamish, BC.</p>
          <p>The highest peak, standing at a wild 2,608 metres, it has always been a dream of mine to summit. It is one of the biggest glaciers in this region, making it very dangerous to climb and requiring mountaineering experience.</p>
          <p>The whole range spans 1,100,000 acres and has many peaks inside the area.</p>
        </div>
      </article>
      <article class="peak reveal">
        <span class="num">03</span>
        <div><h2>Mount Tantalus</h2><p class="elev">2,603 m · Tantalus Range</p></div>
        <div>
          <p>The highest summit of the Tantalus Range, the wall of glaciated peaks you see across the Squamish Valley from the Sea to Sky Highway. The Squamish people call the range Tsewílx’.</p>
          <p>First climbed in 1911, it is a serious glacier-and-ridge objective: crevasses, bergschrunds and an exposed summit ridge, usually approached by helicopter or a long climb up from near sea level.</p>
        </div>
      </article>
      <article class="peak reveal">
        <span class="num">04</span>
        <div><h2>Mount Churchill</h2><p class="elev">No recorded climbs found</p></div>
        <div>
          <p>I can’t find any recorded climbs. I would love to be one of the first.</p>
          <p class="goal">If you have any information on this peak, please <a href="socials.html">let me know</a>!</p>
        </div>
      </article>
    </div>
  </div>
</section>
<section class="join section--tint">
  <div class="wrap reveal">
    <h2>Want in on one of these?</h2>
    <p>I’m always looking for good people to plan with.</p>
    <a class="btn" href="socials.html">Reach out <span aria-hidden="true">→</span></a>
  </div>
</section>"""
page("dreams.html", "Future dreams — Ezra Vernon",
     "Mountains Ezra Vernon wants to climb: Tetrahedron Peak (again), Mount Drew, Mount Tantalus and Mount Churchill.",
     dreams_body, dreams_css)

# ---------------------------------------------------------------- SIDEQUESTS
side_css = """
.quest{display:grid;gap:var(--s5)}
@media (min-width:900px){.quest{grid-template-columns:1fr 1fr;gap:var(--s7)}}
.stat{display:flex;gap:var(--s5);margin:var(--s4) 0}
.stat div{border-top:1px solid var(--ink);padding-top:var(--s2)}
.stat b{display:block;font-family:var(--font-serif);font-weight:400;font-size:var(--step-4);line-height:1}
.stat span{font-size:var(--step--1);color:var(--ink-soft);letter-spacing:.04em}
.rule-card{border:1px solid var(--line);border-radius:var(--radius);padding:var(--s3);background:var(--base)}
.rule-card p{margin:0}
.rule-card p+p{margin-top:var(--s1);color:var(--ink-soft);font-size:var(--step--1)}
.route{list-style:none;margin:0;padding:0;position:relative}
.route::before{content:"";position:absolute;left:11px;top:16px;bottom:16px;width:2px;background:repeating-linear-gradient(var(--accent) 0 8px,transparent 8px 16px)}
.route li{position:relative;padding:0 0 var(--s4) var(--s6)}
.route li:last-child{padding-bottom:0}
.route li::before{content:"";position:absolute;left:0;top:4px;width:24px;height:24px;border-radius:50%;background:var(--base);border:2px solid var(--accent)}
.route li.is-start::before{background:var(--accent)}
.route strong{display:block;font-family:var(--font-serif);font-weight:400;font-size:var(--step-2);line-height:1.2}
.route span{font-size:var(--step--1);color:var(--ink-soft)}
.skill{display:grid;gap:var(--s4)}
@media (min-width:900px){.skill{grid-template-columns:1fr 2fr;gap:var(--s7)}}
"""
side_body = """<section class="page-head">
  <div class="wrap reveal">
    <p class="eyebrow">Page 03</p>
    <h1>Sidequests</h1>
    <p>Smaller, stranger goals that sit alongside the big mountains.</p>
  </div>
</section>
<section class="section section--tint" aria-labelledby="costco">
  <div class="wrap quest">
    <div class="reveal">
      <p class="eyebrow">Running</p>
      <h2 id="costco">Vancouver Costco Ultra Marathon</h2>
      <p>A 55.8 km route starting in Burnaby, going to Brentwood, downtown, Bridgeport and Queensborough before ending back in Burnaby.</p>
      <div class="stat"><div><b>55.8</b><span>kilometres</span></div><div><b>5</b><span>Costcos</span></div><div><b>5</b><span>hot dogs</span></div></div>
      <div class="rule-card"><p><strong>Rule:</strong> eat a Costco hot dog at all 5 Costcos.</p><p>Condiments are optional.</p></div>
    </div>
    <ol class="route reveal" aria-label="Route">
      <li class="is-start"><strong>Burnaby</strong><span>Start · hot dog 1</span></li>
      <li><strong>Brentwood</strong><span>Hot dog 2</span></li>
      <li><strong>Downtown</strong><span>Hot dog 3</span></li>
      <li><strong>Bridgeport</strong><span>Hot dog 4</span></li>
      <li><strong>Queensborough</strong><span>Hot dog 5</span></li>
      <li class="is-start"><strong>Burnaby</strong><span>Finish</span></li>
    </ol>
  </div>
</section>
<section class="section" aria-labelledby="skills">
  <div class="wrap skill">
    <div class="reveal"><p class="eyebrow" id="skills">Skills</p><h2>Guitar</h2></div>
    <div class="reveal">
      <p class="lede">I want to learn how to play the guitar and get good enough that I can play for camping trips with friends.</p>
      <a class="btn btn--ghost" href="socials.html">Got a song I should learn?</a>
    </div>
  </div>
</section>"""
page("sidequests.html", "Sidequests — Ezra Vernon",
     "Ezra Vernon's sidequests: a 55.8 km Vancouver Costco ultra marathon with a hot dog at all five Costcos, and learning guitar.",
     side_body, side_css)

# ---------------------------------------------------------------- QUOTES
QUOTES = [
    ("What is life’s purpose?", "The purpose of my life is to find the balance between the multitude of events and emotions throughout the inevitable course of my life, and to live in the grey area of personal happiness.", "q-long"),
    (None, "Life is like the ocean; although you can’t control it, you can decide whether to sink or swim.", "q-hand"),
    (None, "Living in happiness sheds light on everything that is taken for granted.", "q-serif"),
    (None, "Confusion has a cost.", "q-caps"),
    (None, "The difference between I, and another, is a millimetre and a mile, all at the same time. Is this an illusion of difference? Or a signal of success within myself.", "q-split"),
    (None, "The world is an infinite number of perspectives, each one waiting for something to see from them.", "q-serif q-right"),
    (None, "Live in the balance between two extremes.", "q-mantra"),
]
q_css = """
.q-head{position:relative;color:var(--base);background:var(--ink);overflow:hidden;min-height:min(72vh,640px);display:flex;align-items:flex-end}
.q-head figure{position:absolute;inset:0;margin:0}
.q-head figure img{width:100%;height:100%;object-fit:cover;filter:blur(1px) saturate(1.05);transform:scale(1.02)}
.q-head::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,42,39,.45) 0%,rgba(30,42,39,.7) 55%,rgba(30,42,39,.9) 100%)}
.q-head .wrap{position:relative;z-index:1;padding-block:var(--s8) var(--s7)}
.q-head h1{color:var(--base)}
.q-head p{color:var(--base);font-size:var(--step-1);line-height:1.5;text-shadow:0 1px 12px rgba(30,42,39,.5)}
.q-head .eyebrow{color:var(--base)}
.hand{font-family:"Caveat","Segoe Print","Bradley Hand",cursive;font-weight:500}
.quotes{padding-block:var(--s7);overflow:hidden}
.quote{position:relative;margin:0 0 var(--s8);max-width:880px}
.quote p{max-width:none;margin:0}
.quote .mark{position:absolute;left:-8px;top:-56px;font-family:var(--font-serif);font-size:160px;line-height:1;color:var(--accent);opacity:.14;pointer-events:none;will-change:transform}
.quote footer{margin-top:var(--s2);font-size:var(--step--1);color:var(--ink-soft);letter-spacing:.12em;text-transform:uppercase}
.q-long .ask{font-family:var(--font-serif);font-size:clamp(var(--step-3),5vw,var(--step-5));line-height:1.05;letter-spacing:-0.02em;margin-bottom:var(--s3)}
.q-long .body{font-size:var(--step-1);line-height:1.6;max-width:60ch}
.q-hand p{font-family:"Caveat",cursive;font-size:clamp(var(--step-4),6vw,var(--step-6));line-height:1.05;color:var(--accent)}
.q-hand{margin-left:auto;max-width:760px}
.q-serif p{font-family:var(--font-serif);font-style:italic;font-size:clamp(var(--step-2),3.6vw,var(--step-4));line-height:1.25}
.q-right{margin-left:auto}
.q-caps p{font-family:var(--font-sans);font-weight:500;text-transform:uppercase;letter-spacing:.3em;font-size:clamp(var(--step-1),3vw,var(--step-3));line-height:1.3}
.q-caps{padding-block:var(--s5);border-block:1px solid var(--line);max-width:none}
.q-split p{font-family:var(--font-serif);font-size:clamp(var(--step-2),3.4vw,var(--step-3));line-height:1.3}
.q-split .mm{font-size:.5em;letter-spacing:.02em}
.q-split .mile{font-size:1.5em;font-style:italic;letter-spacing:.06em}
.q-mantra{max-width:none;text-align:center;padding-block:var(--s7);background:var(--base-deep);border-radius:var(--radius)}
.q-mantra p{font-family:var(--font-serif);font-style:italic;font-size:clamp(var(--step-4),7vw,var(--step-6));line-height:1.05;max-width:16ch;margin-inline:auto}
.q-mantra .mark{left:50%;margin-left:-40px;top:8px}
.more{text-align:center;font-size:var(--step-4);color:var(--ink-soft);margin:0 auto}
.more p{max-width:none;margin:0}
/* Varied entrances for the quotes (still short and calm) */
.js .quote.reveal{transform:translateX(-24px)}
.js .q-hand.reveal,.js .q-right.reveal{transform:translateX(24px)}
.js .q-caps.reveal{transform:none}
.js .q-mantra.reveal{transform:scale(.98)}
.js .quote.reveal.is-in{transform:none}
@media (prefers-reduced-motion:reduce){.js .quote.reveal{transform:none}}
"""

def q_html(ask, text, cls):
    if "q-long" in cls:
        inner = f'<p class="ask">{ask}</p><p class="body">{text}</p>'
    elif "q-split" in cls:
        inner = ('<p>The difference between I, and another, is a <span class="mm">millimetre</span> and a <span class="mile">mile</span>, '
                 'all at the same time. Is this an illusion of difference? Or a signal of success within myself.</p>')
    else:
        inner = f"<p>{text}</p>"
    return f'<blockquote class="quote reveal {cls}"><span class="mark" aria-hidden="true" data-drift>“</span>{inner}<footer>— Ezra Vernon</footer></blockquote>'

q_body = f"""<section class="q-head">
  <figure><img src="images/heather-758.webp" srcset="images/heather-480.webp 480w, images/heather-758.webp 758w" sizes="100vw"
      width="758" height="522" fetchpriority="high" alt="Pink mountain heather blooming among green needle-like leaves"></figure>
  <div class="wrap">
    <div>
      <p class="eyebrow">Page 04</p>
      <h1>Quotes</h1>
      <p>These quotes, or daily reminders, are all original pieces written by me (mostly late-night pieces), or are pieces that I enjoy, with the proper recognition that they deserve.</p>
    </div>
  </div>
</section>
<section class="quotes">
  <div class="wrap">
    {''.join(q_html(*q) for q in QUOTES)}
    <div class="more reveal"><p class="hand">More coming soon…</p></div>
  </div>
</section>"""
q_js = """(function(){
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var marks=[].slice.call(document.querySelectorAll('[data-drift]')),ticking=false;
  function upd(){var vh=window.innerHeight;marks.forEach(function(m,i){var r=m.parentNode.getBoundingClientRect();
    var p=(r.top+r.height/2-vh/2)/vh; m.style.transform='translateY('+(p*-40).toFixed(1)+'px) rotate('+(p*(i%2?6:-6)).toFixed(1)+'deg)'});ticking=false}
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(upd)}},{passive:true});upd();
})();"""
page("quotes.html", "Quotes — Ezra Vernon",
     "Original quotes and daily reminders by Ezra Vernon, mostly written late at night.",
     q_body, q_css, q_js, fonts=QUOTE_FONTS)

# ---------------------------------------------------------------- SOCIALS
s_css = """
.links{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.links a{display:grid;grid-template-columns:1fr auto;align-items:center;gap:var(--s3);padding-block:var(--s4);border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink);transition:padding var(--t-med) var(--ease),color var(--t-med) var(--ease)}
.links a:hover{padding-left:var(--s2);color:var(--accent)}
.links b{display:block;font-family:var(--font-serif);font-weight:400;font-size:clamp(var(--step-3),5vw,var(--step-5));line-height:1.1}
.links span{font-size:var(--step--1);color:var(--ink-soft)}
.links .arrow{font-size:var(--step-3);color:var(--accent);transition:transform var(--t-med) var(--ease)}
.links a:hover .arrow{transform:translateX(4px)}
.s-logo{width:160px;margin-bottom:var(--s4)}
"""
s_body = """<section class="page-head">
  <div class="wrap reveal">
    <img class="s-logo" src="images/logo-480.webp" width="160" height="91" alt="Ezra's pink bird logo">
    <p class="eyebrow">Page 06</p>
    <h1>Socials</h1>
    <p>Want to join an adventure, share beta on a peak, or just say hi? Find me here.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <ul class="links">
      <li class="reveal"><a href="https://www.instagram.com/ezrav_insta" rel="noopener"><div><b>Instagram</b><span>@ezrav_insta</span></div><span class="arrow" aria-hidden="true">↗</span></a></li>
      <li class="reveal"><a href="https://ca.linkedin.com/in/ezra-vernon-a98a40343" rel="noopener"><div><b>LinkedIn</b><span>Ezra Vernon</span></div><span class="arrow" aria-hidden="true">↗</span></a></li>
      <li class="reveal"><a href="https://strava.app.link/lBou8jZCg7b" rel="noopener"><div><b>Strava</b><span>Runs, rides and climbs</span></div><span class="arrow" aria-hidden="true">↗</span></a></li>
    </ul>
  </div>
</section>"""
page("socials.html", "Socials — Ezra Vernon",
     "Find Ezra Vernon on Instagram, LinkedIn and Strava.", s_body, s_css)

# ---------------------------------------------------------------- 404
nf_body = """<section class="page-head" style="padding-block:var(--s8)">
  <div class="wrap">
    <p class="eyebrow">404 · Off route</p>
    <h1>This trail doesn’t go anywhere.</h1>
    <p>The page you were looking for isn’t here. Head back to the trailhead or see what I’m planning next.</p>
    <p style="display:flex;gap:var(--s2);flex-wrap:wrap"><a class="btn" href="index.html">Back home</a><a class="btn btn--ghost" href="dreams.html">Future dreams</a></p>
  </div>
</section>"""
page("404.html", "Page not found — Ezra Vernon", "This page doesn't exist on Ezra Vernon's site.", nf_body)
exec(open(pathlib.Path(__file__).parent / "build_training.py").read())
print("built", sorted(p.name for p in OUT.glob("*.html")))
