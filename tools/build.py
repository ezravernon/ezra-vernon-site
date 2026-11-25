#!/usr/bin/env python3
"""Generates the static pages for ezra-vernon/. The OUTPUT is plain HTML (no build step needed to host it);
this script only exists so the shared header/footer/styles stay byte-identical on every page."""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "site"

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
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:104px} /* keeps focused/linked items clear of the fixed header */
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
.hero :focus-visible,.q-head :focus-visible{outline-color:var(--base)}
.site-header :focus-visible{outline-color:var(--hc)}
.eyebrow{font-family:var(--font-sans);font-size:var(--step--1);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 var(--s2)}
.lede{font-size:var(--step-1);line-height:1.5;color:var(--ink)}
.wrap{width:min(1200px,100% - var(--s4));margin-inline:auto}
.section{padding-block:var(--s7)}
.section--tint{background:var(--base-deep)}
.skip{position:absolute;left:var(--s2);top:-80px;background:var(--ink);color:var(--base);padding:var(--s1) var(--s2);border-radius:var(--radius);z-index:100;transition:top var(--t-fast)}
.skip:focus{top:var(--s2)}
/* Visually hidden, still read by screen readers */
.vh{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip-path:inset(50%);white-space:nowrap;border:0}
/* Buttons — one style everywhere */
.btn{display:inline-flex;align-items:center;gap:var(--s1);font:500 var(--step-0)/1 var(--font-sans);padding:var(--s2) var(--s3);border-radius:var(--radius);background:var(--accent);color:var(--base);text-decoration:none;border:1px solid var(--accent);cursor:pointer;transition:background var(--t-med) var(--ease),color var(--t-med) var(--ease),transform var(--t-med) var(--ease)}
.btn:hover{background:var(--ink);border-color:var(--ink);color:var(--base);transform:translateY(-1px)}
.btn--ghost{background:transparent;color:var(--accent)}
.btn--ghost:hover{background:var(--accent);border-color:var(--accent)}
/* Header — a floating "island": a rounded glass bar sitting just below the top edge of every page.
   data-tone="light" = light links on dark glass (over a dark photo header: Home, Quotes); data-tone="dark" = pine links on paper glass.
   The shared script flips the tone to match whatever is behind the island. Pages are grouped into small drop-down menus. */
.site-header{--hc:var(--ink);--hc-line:rgba(30,42,39,.22);--hc-glass:rgba(246,243,238,.8);--hc-edge:rgba(30,42,39,.1);--hc-panel:var(--base);--hc-hover:rgba(30,42,39,.07);--hc-soft:var(--ink-soft);
  position:fixed;top:var(--s2);left:0;right:0;z-index:20;width:min(1120px,100% - var(--s3));margin-inline:auto;
  background:var(--hc-glass);-webkit-backdrop-filter:saturate(1.4) blur(16px);backdrop-filter:saturate(1.4) blur(16px);
  border:1px solid var(--hc-edge);border-radius:32px;box-shadow:0 10px 30px rgba(30,42,39,.1);
  transition:background var(--t-slow) var(--ease),border-color var(--t-slow) var(--ease),box-shadow var(--t-slow) var(--ease)}
.site-header[data-tone="light"]{--hc:var(--base);--hc-line:rgba(246,243,238,.35);--hc-glass:rgba(30,42,39,.4);--hc-edge:rgba(246,243,238,.16);--hc-panel:#24322E;--hc-hover:rgba(246,243,238,.12);--hc-soft:rgba(246,243,238,.72);box-shadow:0 10px 30px rgba(0,0,0,.16)}
.site-header.is-scrolled{box-shadow:0 14px 36px rgba(30,42,39,.16)}
.site-header .wrap{width:auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0 var(--s2);min-height:62px;padding-inline:var(--s3) 10px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--hc);font-family:var(--font-serif);font-size:1.3rem;transition:color var(--t-slow) var(--ease)}
.brand img{width:49px;height:28px}
.brand:hover{color:var(--hc)}
.brand,.nav a,.nav-group-btn,.nav .nav-signin{white-space:nowrap}
.nav ul{list-style:none;margin:0;padding:0}
.nav > ul{display:flex;align-items:center;gap:2px}
/* Every item is a soft pill; hover and the current page get a faint fill */
.nav a,.nav-group-btn,.nav .nav-signin{display:inline-flex;align-items:center;gap:8px;font:400 1rem/1.2 var(--font-sans);color:var(--hc);text-decoration:none;background:transparent;border:0;border-radius:999px;padding:10px 16px;margin:0;cursor:pointer;transition:background var(--t-med) var(--ease),color var(--t-slow) var(--ease)}
.nav a:hover,.nav-group-btn:hover,.nav .nav-signin:hover,.nav-group.is-open > .nav-group-btn{background:var(--hc-hover);color:var(--hc)}
.nav a[aria-current="page"],.nav-group-btn.is-current{background:var(--hc-hover);font-weight:500}
.nav-group-btn::after{content:"";width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-2px) rotate(45deg);transition:transform var(--t-med) var(--ease)}
.nav-group.is-open > .nav-group-btn::after{transform:translateY(1px) rotate(225deg)}
/* Drop-down panel */
.nav-group{position:relative}
.nav-sub{position:absolute;top:calc(100% + 14px);left:50%;min-width:248px;padding:6px;background:var(--hc-panel);border:1px solid var(--hc-edge);border-radius:20px;box-shadow:0 18px 40px rgba(30,42,39,.18);
  opacity:0;visibility:hidden;transform:translate(-50%,-6px);transition:opacity var(--t-med) var(--ease),transform var(--t-med) var(--ease),visibility 0s linear var(--t-med)}
.nav-sub::before{content:"";position:absolute;left:0;right:0;top:-16px;height:16px} /* keeps hover alive across the gap */
.nav-group.is-open .nav-sub{opacity:1;visibility:visible;transform:translate(-50%,0);transition-delay:0s}
.nav-sub a{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;border-radius:14px;padding:10px 14px}
.nav-sub small{font-size:var(--step--1);color:var(--hc-soft);font-weight:400}
/* Sign in looks like the other links (it is a button because it opens a dialog) */
.no-js .nav-signin-item{display:none}
.nav .btn{color:var(--base);background:var(--accent);border:1px solid var(--accent);border-radius:999px;padding:10px 20px;margin-left:6px;font-weight:500}
.nav .btn:hover,.nav .btn[aria-current="page"]{background:var(--ink);border-color:var(--ink);color:var(--base)}
.site-header[data-tone="light"] .nav .btn:hover,.site-header[data-tone="light"] .nav .btn[aria-current="page"]{background:var(--base);border-color:var(--base);color:var(--ink)}
/* Without JavaScript the groups are simply shown inline */
.no-js .nav-group-btn{display:none}
.no-js .nav-sub{position:static;display:flex;opacity:1;visibility:visible;transform:none;min-width:0;padding:0;background:none;border:0;box-shadow:none}
.no-js .nav-sub small{display:none}
/* Pages that start with a paper header leave room for the island */
main > .page-head:first-child{padding-top:calc(78px + var(--s7))}
.nav-toggle{display:none}
@media (max-width:900px){
  .site-header{width:calc(100% - var(--s2));top:var(--s1)}
  .site-header .wrap{min-height:0;padding-inline:var(--s2) 8px}
  .brand{min-height:58px}
  .site-header.menu-open{background:var(--hc-panel)}
  .nav-toggle{display:inline-flex;font:500 1rem/1 var(--font-sans);background:none;border:1px solid var(--hc-line);border-radius:999px;padding:10px 18px;color:var(--hc);cursor:pointer;transition:color var(--t-slow) var(--ease),border-color var(--t-slow) var(--ease)}
  .nav{display:none;width:100%;padding:4px 0 12px}
  .nav.is-open{display:block}
  .nav > ul{flex-direction:column;align-items:stretch;gap:2px}
  .nav a,.nav-group-btn,.nav .nav-signin{width:100%;justify-content:space-between;font-size:var(--step-0);padding:12px 14px}
  .nav-sub{position:static;display:none;opacity:1;visibility:visible;transform:none;min-width:0;padding:0 0 4px 12px;background:none;border:0;box-shadow:none}
  .nav-sub::before{display:none}
  .nav-group.is-open .nav-sub{display:block;transform:none}
  .nav .btn{justify-content:center;margin:8px 0 0}
  .no-js .nav{display:block}
  .no-js .nav > ul{flex-direction:row;flex-wrap:wrap}
  .no-js .nav-sub{display:flex;padding:0}
}
/* Page header used on inner pages */
.page-head{padding-block:var(--s7) var(--s5)}
.page-head p{font-size:var(--step-1);line-height:1.5}
/* Footer */
.site-footer{border-top:1px solid var(--line);padding-block:var(--s6)}
.site-footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:var(--s3);align-items:center}
.site-footer p{margin:0;color:var(--ink-soft);font-size:var(--step--1)}
.site-footer ul{list-style:none;display:flex;flex-wrap:wrap;gap:var(--s1) var(--s3);margin:0;padding:0;font-size:var(--step--1)}
.site-footer a{display:inline-block;padding-block:4px}
.site-footer .legal{margin-top:var(--s3);padding-top:var(--s3);border-top:1px solid var(--line)}
.site-footer .legal a{color:var(--ink-soft)}
.site-footer .legal a:hover,.site-footer .legal a[aria-current="page"]{color:var(--ink)}
/* Sign in (in the menu) -> password gate -> secret section (everything here is black with white type) */
.signin,.vault{--v-ink:#fff;--v-soft:rgba(255,255,255,.62);--v-line:rgba(255,255,255,.14);background:#000;color:var(--v-ink);font-family:var(--font-sans)}
.signin{border:1px solid var(--v-line);border-radius:12px;padding:var(--s5) var(--s4) var(--s4);width:min(420px,100% - var(--s4));box-shadow:0 24px 64px rgba(0,0,0,.5)}
.signin::backdrop{background:rgba(0,0,0,.72);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.signin h2,.vault h1,.vault h2,.vault h3{font-family:var(--font-sans);font-weight:500;color:var(--v-ink);letter-spacing:-0.03em}
.signin h2{font-size:var(--step-2);margin-bottom:var(--s1)}
.signin .sub{color:var(--v-soft);font-size:var(--step--1);margin:0 0 var(--s4)}
.field{display:grid;gap:var(--s1);margin-bottom:var(--s3)}
.field label{font-size:var(--step--1);font-weight:500;color:var(--v-soft);letter-spacing:.14em;text-transform:uppercase}
.field input{font:400 var(--step-0)/1.4 var(--font-sans);padding:var(--s2);border:1px solid var(--v-line);border-radius:var(--radius);background:#0d0d0d;color:#fff;transition:border-color var(--t-fast)}
.field input:focus-visible{border-color:#fff;outline:2px solid #fff;outline-offset:2px}
.field input[aria-invalid="true"]{border-color:#fff}
.signin-msg{min-height:1.6em;margin:0 0 var(--s2);font-size:var(--step--1);color:var(--v-soft)}
.signin-actions{display:flex;gap:var(--s2);flex-wrap:wrap}
.v-btn{font:500 var(--step--1)/1 var(--font-sans);letter-spacing:.04em;padding:var(--s2) var(--s3);border-radius:999px;border:1px solid #fff;background:#fff;color:#000;cursor:pointer;transition:background var(--t-med) var(--ease),color var(--t-med) var(--ease),border-color var(--t-med) var(--ease)}
.v-btn:hover{background:transparent;color:#fff}
.v-btn--ghost{background:transparent;color:#fff;border-color:var(--v-line)}
.v-btn--ghost:hover{border-color:#fff}
.v-btn[disabled]{opacity:.5;cursor:wait}
.signin :focus-visible,.vault :focus-visible{outline-color:#fff}
.vault{position:fixed;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;padding:0;border:0;overflow-y:auto}
.vault[open]{animation:vault-in 500ms var(--ease)}
@keyframes vault-in{from{opacity:0}to{opacity:1}}
.vault::backdrop{background:#000}
html:has(.vault[open]){overflow:hidden}
.vault-bar{position:sticky;top:0;z-index:2;background:#000;border-bottom:1px solid var(--v-line)}
.vault-bar .wrap{display:flex;align-items:center;justify-content:space-between;gap:var(--s2);min-height:72px}
.vault-tag{font-size:var(--step--1);font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--v-soft);margin:0;display:flex;align-items:center;gap:var(--s1)}
.vault-tag::before{content:"";width:6px;height:6px;border-radius:50%;background:#fff}
.vault-bar div{display:flex;gap:var(--s1)}
.vault-body{width:min(880px,100% - var(--s4));margin-inline:auto;padding-block:var(--s7) var(--s8)}
.vault-body h1{font-size:clamp(var(--step-4),7vw,var(--step-6));line-height:1;letter-spacing:-0.045em;margin-bottom:var(--s3)}
.vault-body h2{font-size:clamp(var(--step-2),3.4vw,var(--step-3));margin:var(--s7) 0 var(--s2)}
.vault-body h3{font-size:var(--step-1);margin:var(--s4) 0 var(--s1)}
.vault-body p,.vault-body li{color:var(--v-soft);font-size:var(--step-0);line-height:1.7}
.vault-body .lede{color:var(--v-ink);font-size:var(--step-1);line-height:1.5}
.vault-body ul,.vault-body ol{padding-left:1.2em;margin:0 0 var(--s3)}
.vault-body a{color:#fff;text-decoration-color:rgba(255,255,255,.4)}
.vault-body a:hover{text-decoration-color:#fff}
.vault-body hr{border:0;border-top:1px solid var(--v-line);margin:var(--s7) 0}
.vault-body .eyebrow{color:var(--v-soft);letter-spacing:.24em}
.v-tabs{position:sticky;top:72px;z-index:1;display:flex;gap:var(--s1);overflow-x:auto;scrollbar-width:none;background:#000;padding-block:var(--s2);margin:calc(-1 * var(--s5)) 0 var(--s6);border-bottom:1px solid var(--v-line)}
.v-tabs::-webkit-scrollbar{display:none}
.v-tab{flex:none;font:500 var(--step--1)/1 var(--font-sans);letter-spacing:.04em;padding:var(--s1) var(--s2);border-radius:999px;border:1px solid transparent;background:none;color:var(--v-soft);cursor:pointer;transition:color var(--t-fast),border-color var(--t-fast),background var(--t-fast)}
.v-tab:hover{color:#fff}
.v-tab[aria-selected="true"]{background:#fff;color:#000}
.v-panel[hidden]{display:none}
.v-panel:focus-visible{outline-offset:8px}
.v-panel > .lede{margin-bottom:var(--s5)}
.v-entry{padding-block:var(--s6);border-top:1px solid var(--v-line);scroll-margin-top:150px}
.v-entry h2{margin:0 0 var(--s3);display:flex;flex-wrap:wrap;align-items:center;gap:var(--s2)}
.vault-body .v-entry .eyebrow{margin-bottom:var(--s1)}
.v-badge{font:500 var(--step--1)/1 var(--font-sans);letter-spacing:.14em;text-transform:uppercase;border:1px solid #fff;border-radius:999px;padding:6px var(--s1)}
.v-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:var(--s3);margin:0 0 var(--s3)}
.v-meta div{border-top:1px solid var(--v-line);padding-top:var(--s1)}
.v-meta dt{font-size:var(--step--1);letter-spacing:.14em;text-transform:uppercase;color:var(--v-soft);margin-bottom:4px}
.v-meta dd{margin:0;color:#fff}
.vault-body .v-watch{display:flex;flex-wrap:wrap;gap:var(--s1) var(--s2);align-items:baseline;color:#fff;font-variant-numeric:tabular-nums;border:1px solid var(--v-line);border-radius:var(--radius);padding:var(--s2);max-width:none}
.v-watch span{font-size:var(--step--1);letter-spacing:.14em;text-transform:uppercase;color:var(--v-soft)}
.v-photos{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--s2);margin:var(--s4) 0}
.v-photo{margin:0}
.v-frame{background:#111;border-radius:var(--radius);overflow:hidden}
.v-frame img{width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity var(--t-slow) var(--ease)}
.v-frame img.is-in{opacity:1}
.v-photo figcaption{margin-top:var(--s1);font-size:var(--step--1);color:var(--v-soft)}
.v-body blockquote{margin:0 0 var(--s3);padding-left:var(--s2);border-left:2px solid #fff;color:#fff}
.v-body code{font-size:.9em;background:#141414;padding:2px 6px;border-radius:4px}
.vault-body .v-empty{border:1px dashed var(--v-line);border-radius:var(--radius);padding:var(--s4);max-width:none}
.vault-body .v-stamp{margin-top:var(--s7);font-size:var(--step--1);color:rgba(255,255,255,.4)}
/* Gentle reveal on scroll (only when JS runs and motion is allowed) */
.js .reveal{opacity:0;transform:translateY(16px);transition:opacity var(--t-slow) var(--ease),transform var(--t-slow) var(--ease)}
.js .reveal.is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js .reveal{opacity:1;transform:none;transition:none}
  *{transition-duration:1ms!important;animation:none!important}
}
/* Windows high-contrast / forced colours: states that rely on a background fill get a visible border instead */
@media (forced-colors:active){
  .btn,.v-btn,.chip,.v-tab,.nav-toggle{border:1px solid ButtonText}
  .nav a[aria-current="page"],.chip[aria-pressed="true"],.v-tab[aria-selected="true"]{outline:2px solid Highlight;outline-offset:2px}
  .site-header,.nav-sub{background:Canvas;border:1px solid CanvasText;-webkit-backdrop-filter:none;backdrop-filter:none}
  .nav-group-btn.is-current{outline:2px solid Highlight;outline-offset:2px}
}
"""

SHARED_JS = """
/* ===== SHARED SCRIPT — keep identical on all pages ===== */
(function(){
  var d=document.documentElement; d.classList.remove('no-js'); d.classList.add('js');
  // Mobile nav
  var hd=document.querySelector('.site-header'), t=document.querySelector('.nav-toggle'), n=document.getElementById('site-nav');
  var groups=[].slice.call(document.querySelectorAll('.nav-group')), mob=window.matchMedia('(max-width:900px)');
  function grp(g,o){g.classList.toggle('is-open',o);g.querySelector('.nav-group-btn').setAttribute('aria-expanded',o)}
  function closeGroups(except){groups.forEach(function(g){if(g!==except)grp(g,false)})}
  function menu(o){n.classList.toggle('is-open',o);t.setAttribute('aria-expanded',o);hd.classList.toggle('menu-open',o);
    if(o)groups.forEach(function(g){if(g.querySelector('.is-current'))grp(g,true)});else closeGroups()}
  if(t&&n){t.addEventListener('click',function(){menu(!n.classList.contains('is-open'))})}
  // Drop-down groups: click/tap or keyboard opens; on a desktop mouse, hovering opens too
  groups.forEach(function(g){var b=g.querySelector('.nav-group-btn'),tm;
    b.addEventListener('click',function(){var o=!g.classList.contains('is-open')||(!mob.matches&&Date.now()-(g._hov||0)<700);if(!mob.matches)closeGroups(g);grp(g,o)});
    g.addEventListener('mouseenter',function(e){if(mob.matches||e.pointerType==='touch')return;clearTimeout(tm);if(!g.classList.contains('is-open'))g._hov=Date.now();closeGroups(g);grp(g,true)});
    g.addEventListener('mouseleave',function(){if(mob.matches)return;tm=setTimeout(function(){grp(g,false)},180)});
    g.addEventListener('focusout',function(e){if(!mob.matches&&!g.contains(e.relatedTarget))grp(g,false)});});
  document.addEventListener('click',function(e){if(!mob.matches&&!e.target.closest('.nav-group'))closeGroups()});
  // Escape closes an open drop-down (focus back to its button), then the mobile menu
  document.addEventListener('keydown',function(e){if(e.key!=='Escape'||document.querySelector('dialog[open]'))return;
    var g=groups.filter(function(x){return x.classList.contains('is-open')&&x.contains(document.activeElement)})[0];
    if(g&&!mob.matches){grp(g,false);g.querySelector('.nav-group-btn').focus();return}
    if(t&&n&&n.classList.contains('is-open')){var inside=n.contains(document.activeElement);menu(false);if(inside)t.focus()}
    else closeGroups()});
  // Island tone: light links while a dark photo header ([data-dark-head]) is behind it
  if(hd){var dark=document.querySelector('[data-dark-head]'),busy=false;
    function hdr(){var y=window.scrollY||0,r=hd.getBoundingClientRect();hd.classList.toggle('is-scrolled',y>8);
      if(dark)hd.dataset.tone=dark.getBoundingClientRect().bottom>r.top+r.height/2?'light':'dark';busy=false}
    addEventListener('scroll',function(){if(!busy){busy=true;requestAnimationFrame(hdr)}},{passive:true});addEventListener('resize',hdr);hdr();}
  // Scroll reveal
  var els=document.querySelectorAll('.reveal');
  var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!('IntersectionObserver' in window)||rm){els.forEach(function(e){e.classList.add('is-in')});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});els.forEach(function(e){io.observe(e)});}
  // Secret section. Its content lives in data/secret.json, encrypted (AES-256-GCM, key from the password via PBKDF2-SHA256),
  // so nothing private is readable in the page source. Wrong password = decryption fails. Made with tools/secret.py.
  var btn=document.querySelector('.signin-btn'), dlg=document.getElementById('signin'), vault=document.getElementById('vault');
  if(!btn||!dlg||!vault)return;
  var KEY='ev-vault', body=vault.querySelector('.vault-body'), form=dlg.querySelector('form'), msg=dlg.querySelector('.signin-msg'),
      pw=dlg.querySelector('#signin-pw'), sub=dlg.querySelector('.signin-submit'), blob=null;
  function b64(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)})}
  function load(){return blob||(blob=fetch('data/secret.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error('load');return r.json()}).catch(function(e){blob=null;throw e}))}
  function getK(){try{return sessionStorage.getItem(KEY)}catch(e){return null}}
  function setK(v){try{v?sessionStorage.setItem(KEY,v):sessionStorage.removeItem(KEY)}catch(e){}}
  async function derive(p,j){var m=await crypto.subtle.importKey('raw',new TextEncoder().encode(p),'PBKDF2',false,['deriveBits']);
    return new Uint8Array(await crypto.subtle.deriveBits({name:'PBKDF2',hash:'SHA-256',salt:b64(j.salt),iterations:j.iter},m,256))}
  async function open(raw,j){var k=await crypto.subtle.importKey('raw',raw,'AES-GCM',false,['decrypt']);
    return new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM',iv:b64(j.iv)},k,b64(j.ct)))}
  // Tabs + encrypted photos inside the secret section (each photo has its own key, carried inside the encrypted page)
  function pics(scope){scope.querySelectorAll('img[data-k]').forEach(async function(im){var k=im.dataset.k;im.removeAttribute('data-k');
    try{var r=await fetch('data/secret/p/'+im.dataset.p+'.bin');if(!r.ok)throw 0;var b=new Uint8Array(await r.arrayBuffer());
      var key=await crypto.subtle.importKey('raw',b64(k),'AES-GCM',false,['decrypt']);
      var pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:b.slice(0,12)},key,b.slice(12));
      im.src=URL.createObjectURL(new Blob([pt],{type:'image/webp'}));im.classList.add('is-in')}catch(e){im.alt='Photo couldn\\u2019t load';im.classList.add('is-err')}})}
  function tab(id){var pn=document.getElementById(id);if(!pn)return;
    body.querySelectorAll('[data-panel]').forEach(function(x){x.hidden=x!==pn});
    body.querySelectorAll('[data-tab]').forEach(function(t){var on=t.dataset.tab===id;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1});pics(pn)}
  // Screen-reader semantics for the tabs (added here so they also apply to an already-encrypted page): tablist/tab/tabpanel + arrow keys
  function tabsAria(){var tl=body.querySelector('.v-tabs');if(!tl)return;tl.setAttribute('role','tablist');tl.setAttribute('aria-label','Secret sections');
    body.querySelectorAll('[data-tab]').forEach(function(t){t.setAttribute('role','tab');t.id='tab-'+t.dataset.tab;t.setAttribute('aria-controls',t.dataset.tab);t.tabIndex=t.getAttribute('aria-selected')==='true'?0:-1});
    body.querySelectorAll('[data-panel]').forEach(function(p){p.setAttribute('role','tabpanel');p.setAttribute('aria-labelledby','tab-'+p.id);p.tabIndex=0})}
  body.addEventListener('keydown',function(e){var c=e.target.closest&&e.target.closest('[data-tab]');if(!c)return;
    var all=[].slice.call(body.querySelectorAll('[data-tab]')),i=all.indexOf(c),k=e.key,
        j=k==='ArrowRight'?(i+1)%all.length:k==='ArrowLeft'?(i-1+all.length)%all.length:k==='Home'?0:k==='End'?all.length-1:-1;
    if(j<0)return;e.preventDefault();tab(all[j].dataset.tab);all[j].focus();vault.scrollTop=0});
  body.addEventListener('click',function(e){var t=e.target.closest('[data-tab]');if(t){tab(t.dataset.tab);vault.scrollTop=0;return}
    var g=e.target.closest('[data-goto]');if(g){e.preventDefault();tab(g.dataset.goto);var x=document.getElementById(g.getAttribute('href').slice(1));if(x)x.scrollIntoView({block:'start'})}});
  function show(html){body.innerHTML=html;tabsAria();var first=body.querySelector('[data-panel]:not([hidden])');if(first)pics(first);if(dlg.open)dlg.close();if(vault.showModal)vault.showModal();else vault.setAttribute('open','');
    vault.scrollTop=0;setTimeout(function(){vault.querySelector('.vault-close').focus()},0)}
  // Focus goes back to Sign in, or to the Menu button when Sign in is tucked inside the closed mobile menu
  function back(){var el=btn.offsetParent?btn:t;if(el)el.focus()}
  function hide(){if(vault.close)vault.close();else vault.removeAttribute('open');back()}
  function gate(){msg.textContent='';pw.value='';pw.removeAttribute('aria-invalid');sub.disabled=false;if(dlg.showModal)dlg.showModal();else dlg.setAttribute('open','');setTimeout(function(){pw.focus()},0)}
  btn.addEventListener('click',async function(){var k=getK();if(t&&n&&n.classList.contains('is-open')&&t.offsetParent)menu(false);
    if(k){try{show(await open(b64(k),await load()));return}catch(e){setK(null)}}
    gate()});
  dlg.querySelector('.signin-cancel').addEventListener('click',function(){dlg.close()});
  dlg.addEventListener('close',function(){if(!vault.open)back()});
  pw.addEventListener('input',function(){pw.removeAttribute('aria-invalid')});
  vault.querySelector('.vault-close').addEventListener('click',hide);
  vault.querySelector('.vault-lock').addEventListener('click',function(){setK(null);body.innerHTML='';hide()});
  vault.addEventListener('close',back);
  form.addEventListener('submit',async function(e){e.preventDefault();if(!pw.value){msg.textContent='Enter the password.';return}
    if(!window.crypto||!crypto.subtle){msg.textContent='This needs a secure (https) connection.';return}
    sub.disabled=true;msg.textContent='Unlocking\\u2026';var j;
    try{j=await load()}catch(err){msg.textContent='Couldn\\u2019t load the secret section. Check your connection.';sub.disabled=false;return}
    try{var raw=await derive(pw.value.trim().toLowerCase(),j),html=await open(raw,j);setK(btoa(String.fromCharCode.apply(null,raw)));show(html)}
    catch(err){msg.textContent='That password didn\\u2019t match. Try again.';pw.setAttribute('aria-invalid','true');pw.select()}
    sub.disabled=false});
})();
"""

# Pages that open with a dark photo header: the header starts with light links there
DARK_HEAD_PAGES = {"index.html", "quotes.html"}

# Main menu. A tuple with a list is a drop-down group: (label, [(href, label, short description), ...])
NAV = [
    ("index.html", "Home"),
    ("Adventures", [("dreams.html", "Dreams", "Peaks I want to stand on"),
                    ("sidequests.html", "Sidequests", "Costco ultra, guitar and more"),
                    ("training.html", "Training", "Every run, hike and climb")]),
    ("Writing", [("quotes.html", "Quotes", "Late-night reminders"),
                 ("thoughts.html", "Thoughts", "What\u2019s on my mind")]),
]


def header(current):
    def cur(h):
        return ' aria-current="page"' if h == current else ""
    parts = []
    for a, b in NAV:
        if isinstance(b, list):
            gid = "nav-" + a.lower()
            here = " is-current" if any(h == current for h, _, _ in b) else ""
            subs = "".join(f'<li><a href="{h}"{cur(h)}>{l}<small>{d}</small></a></li>' for h, l, d in b)
            parts.append(f'<li class="nav-group"><button class="nav-group-btn{here}" type="button" aria-expanded="false" aria-controls="{gid}">{a}</button>'
                         f'<ul class="nav-sub" id="{gid}">{subs}</ul></li>')
        else:
            parts.append(f'<li><a href="{a}"{cur(a)}>{b}</a></li>')
    items = "".join(parts)
    tone = "light" if current in DARK_HEAD_PAGES else "dark"
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header" data-tone="{tone}">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="images/logo-240.webp" width="56" height="32" alt="">Ezra Vernon</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{items}<li class="nav-signin-item"><button class="nav-signin signin-btn" type="button" aria-haspopup="dialog" aria-controls="signin">Sign in</button></li><li><a class="btn" href="socials.html"{cur("socials.html")}>Socials</a></li></ul>
    </nav>
  </div>
</header>"""


LEGAL = [("privacy.html", "Privacy"), ("terms.html", "Terms"), ("cookies.html", "Cookies"), ("accessibility.html", "Accessibility")]


def footer(current):
    legal = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a></li>' for h, l in LEGAL)
    return FOOTER.replace("{legal}", legal)


FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <p>Ezra Vernon · Live in the balance between two extremes.</p>
    <ul>
      <li><a href="https://www.instagram.com/ezrav_insta" rel="noopener">Instagram</a></li>
      <li><a href="https://ca.linkedin.com/in/ezra-vernon-a98a40343" rel="noopener">LinkedIn</a></li>
      <li><a href="https://strava.app.link/lBou8jZCg7b" rel="noopener">Strava</a></li>
    </ul>
  </div>
  <nav class="wrap legal" aria-label="Legal">
    <ul>{legal}</ul>
  </nav>
</footer>
<dialog class="signin" id="signin" aria-labelledby="signin-title">
  <form method="dialog" novalidate>
    <h2 id="signin-title">Sign in</h2>
    <p class="sub">Private section. Password only.</p>
    <div class="field"><label for="signin-pw">Password</label><input id="signin-pw" name="password" type="password" autocomplete="current-password" aria-describedby="signin-msg" required></div>
    <p class="signin-msg" id="signin-msg" role="status" aria-live="polite"></p>
    <div class="signin-actions">
      <button class="v-btn signin-submit" type="submit">Unlock</button>
      <button class="v-btn v-btn--ghost signin-cancel" type="button">Close</button>
    </div>
  </form>
</dialog>
<dialog class="vault" id="vault" aria-label="Secret section">
  <div class="vault-bar"><div class="wrap">
    <p class="vault-tag">Secret</p>
    <div><button class="v-btn v-btn--ghost vault-lock" type="button">Lock</button><button class="v-btn vault-close" type="button">Close</button></div>
  </div></div>
  <div class="vault-body"></div>
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
{footer(fname)}
<script>{SHARED_JS}</script>
{pjs}</body>
</html>
"""
    (OUT / fname).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- HOME
HOME_COMMENT = """<!--
HANDOVER NOTES — Ezra Vernon personal site (v1, 2026-11-08)
Pages: index.html (Home), dreams.html, sidequests.html, quotes.html, thoughts.html, training.html, socials.html, 404.html; photos in images/.
Thoughts: thoughts.html is built from tools/thoughts/thoughts.json, filled from Ezra's Notion "Thoughts" database by the Saturday update (rows with Hide ticked are left out).
Policies: privacy.html, terms.html, cookies.html, accessibility.html, linked from the footer of every page.
Training data: data/activities.json + the log on training.html, generated from Ezra's COROS history (date, sport, time, distance, own titles only;
  no coordinates, place names, heart rate or calories). Refresh by asking Claude to pull new COROS activities.
Hosting plan: GitHub repo -> Vercel -> custom domain (Wix). Plain static HTML, no build step; Vercel serves 404.html automatically.
DESIGN RECIPE "Alpine field notebook": warm paper base, deep pine ink, one deep-turquoise accent (Ezra's favourite colour);
  Fraunces serif headings + DM Sans body; Home has stronger entrance motion (curtain/zoom hero, flying bird, word-by-word mantra); looping vertical video hero (Ezra's Venice Grand Canal boat clip; shown whole, never cropped or zoomed; last second cross-fades into the first so it loops seamlessly) with text over it; transparent header whose links switch light/dark to suit the background (frosted once scrolled); one calm idea per section; mantra set large and centred.
  Quotes page only adds a third face (Caveat, handwritten) because Ezra asked for multiple font types there.
Colours: base #F6F3EE, tint #EDE7DE, ink #1E2A27, soft ink #5B6662, accent #1A6E6A. Logo pink is used only inside the logo image.
How to edit: the "SHARED STYLES" and "SHARED SCRIPT" blocks, header, footer and sign-in dialog must stay identical on every page.
  Page-specific CSS sits in the "PAGE STYLES" block. Change the nav/footer on every page.
Hero video (from IMG_1798.MOV): hero-mobile.mp4 (720x1280, phones), hero-desktop.mp4 (1080x1920), hero-poster.webp (first frame, shown while loading), hero-backdrop.webp (blurred still behind the video on wide screens).
Photos: meadow-{600,900,1220}.webp (no longer used on Home), meadow-wide-{800,1220}.webp (Dreams header), heather-{480,758}.webp (Quotes header background),
  frisbee-{800,1400}.webp (Home photos; credit Dan Tsuji Photography), car-{600,1000}.webp + belay-{600,1000}.webp (Home photos),
  logo-{240,480,960}.webp (header + Socials), favicon-64.png, apple-touch-icon.png. All EXIF stripped.
  To add/swap a photo: convert to WebP, strip metadata, export the same widths, update width/height/srcset/alt.
Sign-in: the "Sign in" item in the menu opens a password prompt; the right password decrypts data/secret.json and shows the
  blacked-out secret section. The content is encrypted (AES-GCM, PBKDF2 key), so it is not readable in the source.
  Content comes from Ezra's Notion "Summit Log" database and is re-encrypted with a NEW password every Saturday by the weekly update (tools/secret.py, tools/SECRET.md).
-->
"""

home_css = """
/* Gallery: masonry columns of photos; click one to open it large (lightbox). Until photos are added
   (tools/add_photos.py) it shows soft placeholder tiles. */
.gallery-head{text-align:center;margin-bottom:var(--s5)}
.gallery-head h2{margin-bottom:0}
.gallery-head p{margin-inline:auto}
.gallery{columns:2;column-gap:var(--s2)}
@media (min-width:760px){.gallery{columns:3;column-gap:var(--s3)}}
.g-item{break-inside:avoid;margin:0 0 var(--s2);display:block;width:100%}
@media (min-width:760px){.g-item{margin-bottom:var(--s3)}}
.g-item button{display:block;width:100%;padding:0;border:0;background:none;cursor:zoom-in;border-radius:14px;overflow:hidden}
.g-item img{display:block;width:100%;height:auto;transition:transform 600ms var(--ease)}
.g-item button:hover img{transform:scale(1.03)}
.g-item figcaption{font-size:var(--step--1);color:var(--ink-soft);padding-top:8px}
.g-ph{display:grid;place-items:center;align-content:center;gap:10px;border-radius:14px;background:rgba(30,42,39,.05);border:1px dashed rgba(30,42,39,.2);color:var(--ink-soft);font-size:var(--step--1)}
.g-ph svg{width:34px;height:34px;opacity:.55}
.lightbox{padding:0;border:0;background:transparent;max-width:100vw;max-height:100vh;width:100vw;height:100vh;color:var(--base)}
.lightbox::backdrop{background:rgba(20,28,26,.92)}
.lightbox figure{margin:0;height:100%;display:grid;place-items:center;align-content:center;gap:var(--s2);padding:var(--s6) var(--s3)}
.lightbox img{max-width:min(100%,1600px);max-height:calc(100vh - 160px);width:auto;height:auto;border-radius:10px}
.lightbox figcaption{font-size:var(--step--1);color:rgba(246,243,238,.8);text-align:center}
.lb-btn{position:fixed;width:48px;height:48px;border-radius:50%;border:1px solid rgba(246,243,238,.3);background:rgba(246,243,238,.08);color:var(--base);font-size:1.4rem;line-height:1;cursor:pointer;display:grid;place-items:center}
.lb-btn:hover{background:rgba(246,243,238,.18)}
.lb-close{top:var(--s2);right:var(--s2)}
.lb-prev{left:var(--s2);top:50%;transform:translateY(-50%)}
.lb-next{right:var(--s2);top:50%;transform:translateY(-50%)}
.lightbox :focus-visible{outline-color:var(--base)}
.hero{position:relative;min-height:min(88vh,880px);display:flex;align-items:flex-end;overflow:hidden;background:var(--ink);color:var(--base)}
/* The hero video is vertical and always shown whole ("contain", no zoom). On phones the hero takes the video's
   9:16 shape so it fills edge to edge; on wider screens a blurred still of the scene fills the sides. */
.hero-bg{position:absolute;inset:0;margin:0;background:#3d6f8c url(images/hero-backdrop.webp) center/cover no-repeat}
.hero-bg video{display:block;width:100%;height:100%;object-fit:contain;object-position:50% 50%}
@media (max-width:600px){.hero{min-height:0;aspect-ratio:9/16}}
/* Small pause/play control for the looping background video (bottom-right of the hero) */
.hero-pause{position:absolute;right:var(--s3);bottom:var(--s3);z-index:2;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;cursor:pointer;
  background:rgba(30,42,39,.35);border:1px solid rgba(246,243,238,.35);color:var(--base);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);transition:background var(--t-med) var(--ease)}
.hero-pause:hover{background:rgba(30,42,39,.6)}
.hero-pause span{width:12px;height:14px;border-left:4px solid currentColor;border-right:4px solid currentColor}
.hero-pause[aria-pressed="true"] span{width:0;height:0;border:0;border-left:13px solid currentColor;border-top:8px solid transparent;border-bottom:8px solid transparent;margin-left:4px}
.no-js .hero-pause{display:none}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,42,39,.35) 0%,rgba(30,42,39,0) 16%,rgba(30,42,39,0) 55%,rgba(30,42,39,.55) 82%,rgba(30,42,39,.72) 100%);pointer-events:none}
.hero .wrap{position:relative;z-index:1;padding-block:var(--s8) var(--s7)}
.hero h1{color:var(--base);margin-bottom:0;text-shadow:0 2px 24px rgba(30,42,39,.35)}
.hero .eyebrow{color:var(--base)}
.hero .lede{color:var(--base);margin:0;max-width:34ch}
/* Photo strip below the hero */
.photo-grid{display:grid;gap:var(--s3);grid-template-columns:1fr}
@media (min-width:760px){.photo-grid{grid-template-columns:1fr 1fr}.photo-grid .wide{grid-column:1 / -1}}
.photo{margin:0}
.photo .frame{overflow:hidden;border-radius:var(--radius);background:var(--base);aspect-ratio:3/4}
.photo.wide .frame{aspect-ratio:3/2}
.photo img{width:100%;height:100%;object-fit:cover;transition:transform var(--t-slow) var(--ease)}
.photo:hover img{transform:scale(1.03)}
.photo figcaption{margin-top:var(--s1);font-size:var(--step--1);color:var(--ink-soft)}
.about .wrap{display:grid;gap:var(--s3);justify-items:center;text-align:center;max-width:62rem;margin-inline:auto}
.about .wrap > *{width:100%}
.about .wrap p{margin-inline:auto}
.roles span{white-space:nowrap}
.roles{font-family:var(--font-serif);font-size:clamp(1.15rem,5.2vw,var(--step-2));line-height:1.2;color:var(--accent);margin-bottom:0}
.sports{list-style:none;padding:0;margin:var(--s4) 0 0;display:flex;flex-wrap:wrap;justify-content:center;gap:var(--s1)}
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
<section class="hero" data-dark-head>
  <figure class="hero-bg">
    <video autoplay muted loop playsinline preload="auto" poster="images/hero-poster.webp" aria-hidden="true" tabindex="-1">
      <source src="images/hero-mobile.mp4" type="video/mp4" media="(max-width:600px)">
      <source src="images/hero-desktop.mp4" type="video/mp4">
    </video>
  </figure>
  <button class="hero-pause" type="button" aria-pressed="false" aria-label="Pause background video"><span aria-hidden="true"></span></button>
  <div class="wrap">
    <div class="reveal">
      <h1>Welcome to my page</h1>
    </div>
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
    <div class="reveal"><p class="eyebrow">About me</p><p class="roles"><span>Website designer ·</span> <span>Scrambler ·</span> <span>Ultra runner</span></p></div>
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

<!--GALLERY-->

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
  // Gallery lightbox: open a photo large; arrows / buttons step through, Esc or the close button shuts it
  var lb=document.getElementById('lightbox'),items=[].slice.call(document.querySelectorAll('.g-item button'));
  if(!lb||!items.length)return;
  var li=lb.querySelector('img'),lc=lb.querySelector('figcaption'),at=0,from;
  function show(i){at=(i+items.length)%items.length;var b=items[at];li.src=b.dataset.full;li.alt=b.querySelector('img').alt;lc.textContent=b.dataset.caption||'';lc.hidden=!b.dataset.caption}
  items.forEach(function(b,i){b.addEventListener('click',function(){from=b;show(i);lb.showModal()})});
  lb.querySelector('.lb-close').addEventListener('click',function(){lb.close()});
  lb.querySelector('.lb-prev').addEventListener('click',function(){show(at-1)});
  lb.querySelector('.lb-next').addEventListener('click',function(){show(at+1)});
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.tagName==='FIGURE')lb.close()});
  lb.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(at-1);if(e.key==='ArrowRight')show(at+1)});
  lb.addEventListener('close',function(){if(from)from.focus()});
})();
(function(){
  // Background video: loops on its own; the button pauses/plays it, and reduced-motion users start paused
  var img=document.querySelector('.hero-bg video'),pb=document.querySelector('.hero-pause');
  if(!img)return;
  function vid(play){if(play){var pr=img.play();if(pr&&pr.catch)pr.catch(function(){})}else img.pause();
    if(pb){pb.setAttribute('aria-pressed',!play);pb.setAttribute('aria-label',(play?'Pause':'Play')+' background video')}}
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){img.removeAttribute('autoplay');vid(false)}
  if(pb)pb.addEventListener('click',function(){vid(img.paused)});
})();
(function(){
  if(!window.matchMedia||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  // Mantra: wrap each word so it can animate in
  var q=document.querySelector('.mantra blockquote p');
  if(q){var full=q.textContent.trim(),words=full.split(/\\s+/);
    q.innerHTML='<span class="vh">'+full+'</span>'+words.map(function(w,i){return '<span class="w" aria-hidden="true" style="--i:'+i+'">'+w+'</span>'}).join(' ');}
  // Hero background: reveal on load, then parallax while scrolling
  var fig=document.querySelector('.hero-bg'),img=fig&&fig.querySelector('video');
  if(!fig)return;
  requestAnimationFrame(function(){requestAnimationFrame(function(){fig.classList.add('is-in')})});
  setTimeout(function(){fig.classList.add('is-settled');par()},2300);
  var tick=false,hero=fig.parentNode;
  function par(){var h=hero.offsetHeight,y=Math.min(Math.max(scrollY,0),h);img.style.setProperty('--py',Math.min(y*0.25,h*0.05).toFixed(1)+'px');tick=false}
  addEventListener('scroll',function(){if(fig.classList.contains('is-settled')&&!tick){tick=true;requestAnimationFrame(par)}},{passive:true});
})();"""

def gallery_html():
    src = OUT / "data" / "gallery.json"
    photos = json.loads(src.read_text(encoding="utf-8")).get("photos", []) if src.exists() else []
    def esc(t):
        return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    if photos:
        tiles = "\n".join(
            f'    <figure class="g-item reveal"><button type="button" data-full="images/gallery/{p["src"]}-1600.webp"'
            f' data-caption="{esc(p.get("caption", ""))}" aria-label="Open photo larger">'
            f'<img src="images/gallery/{p["src"]}-800.webp" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async" alt="{esc(p.get("alt", ""))}">'
            f'</button>' + (f'<figcaption>{esc(p["caption"])}</figcaption>' if p.get("caption") else "") + '</figure>'
            for p in photos)
        box = ('\n<dialog class="lightbox" id="lightbox" aria-label="Photo viewer">\n'
               '  <figure><img src="" alt=""><figcaption hidden></figcaption></figure>\n'
               '  <button class="lb-btn lb-close" type="button" aria-label="Close">&times;</button>\n'
               '  <button class="lb-btn lb-prev" type="button" aria-label="Previous photo">&#8249;</button>\n'
               '  <button class="lb-btn lb-next" type="button" aria-label="Next photo">&#8250;</button>\n'
               '</dialog>')
    else:
        icon = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">'
                '<path d="M3 19l6-9 4 6 3-4 5 7z"/><circle cx="17" cy="6" r="2"/></svg>')
        tiles = "\n".join(f'    <div class="g-item g-ph reveal" style="aspect-ratio:{r}">{icon}<span>Photo coming soon</span></div>'
                          for r in ("4/5", "3/2", "1/1", "3/4", "3/2", "4/5"))
        box = ""
    return ('<!-- GALLERY (photos come from site/data/gallery.json; add them with tools/add_photos.py) -->\n'
            '<section class="section" id="gallery" aria-labelledby="gallery-title">\n'
            '  <div class="wrap">\n'
            '    <div class="gallery-head reveal"><p class="eyebrow">Gallery</p><h2 id="gallery-title">Moments from outside</h2></div>\n'
            '    <div class="gallery">\n' + tiles + '\n    </div>\n  </div>\n</section>' + box)


home_body = home_body.replace("<!--GALLERY-->", gallery_html())

page("index.html", "Ezra Vernon — skiing, mountains and side quests",
     "Ezra Vernon's personal site: about me, the mountains I want to climb, side quests like a Costco ultra, and original quotes.",
     home_body, home_css, home_js, top_comment=HOME_COMMENT,
     jsonld={"@context": "https://schema.org", "@type": "Person", "name": "Ezra Vernon",
             "image": "images/hero-poster.webp",
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
          <p>The highest summit of the Tantalus Range, the wall of glaciated peaks you see across the Squamish Valley from the Sea to Sky Highway. The Squamish people call the range <span lang="squ">Tsewílx’</span>.</p>
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

q_body = f"""<section class="q-head" data-dark-head>
  <figure><img src="images/heather-758.webp" srcset="images/heather-480.webp 480w, images/heather-758.webp 758w" sizes="100vw"
      width="758" height="522" fetchpriority="high" alt="Pink mountain heather blooming among green needle-like leaves"></figure>
  <div class="wrap">
    <div>
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

# ---------------------------------------------------------------- LEGAL (privacy, terms, cookies, accessibility)
# POLICY_UPDATED is written by hand: change it only when the wording of a policy changes, so the weekly rebuild leaves these pages untouched.
# If the site ever gains analytics, ads, embeds, a contact form or accounts, the Privacy and Cookie pages must be rewritten first.
POLICY_UPDATED = "November 14, 2026"
legal_css = """
.legal-head .updated{font-size:var(--step--1);color:var(--ink-soft);margin:0}
.prose{padding-block:0 var(--s7)}
.prose > .wrap > *{max-width:var(--measure)}
.prose h2{font-size:var(--step-3);margin:var(--s6) 0 var(--s2)}
.prose h3{font-size:var(--step-1);font-family:var(--font-sans);font-weight:500;letter-spacing:0;margin:var(--s4) 0 var(--s1)}
.prose ul{padding-left:1.2em;margin:0 0 var(--s3)}
.prose li{margin-bottom:var(--s1)}
.prose .short{border:1px solid var(--line);border-left:2px solid var(--accent);border-radius:var(--radius);background:var(--base-deep);padding:var(--s3) var(--s4)}
.prose .short h2{font-size:var(--step-1);font-family:var(--font-sans);font-weight:500;letter-spacing:0;margin:0 0 var(--s2)}
.prose .short ul,.prose .short p:last-child{margin-bottom:0}
.prose .short li:last-child{margin-bottom:0}
.prose .table-scroll{overflow-x:auto;margin:0 0 var(--s3);max-width:none}
.prose table{border-collapse:collapse;width:100%;min-width:560px;font-size:var(--step--1);line-height:1.5}
.prose caption{text-align:left;color:var(--ink-soft);padding-bottom:var(--s1)}
.prose th,.prose td{text-align:left;vertical-align:top;padding:var(--s2);border-bottom:1px solid var(--line)}
.prose thead th{font-weight:500;letter-spacing:.08em;text-transform:uppercase;font-size:.8125rem;color:var(--ink-soft);border-bottom-color:var(--ink)}
.prose tbody th{font-weight:500}
.prose code{white-space:nowrap;font-size:.9em;background:var(--base-deep);padding:2px 6px;border-radius:4px}
"""


def legal_page(fname, title, desc, h1, lede, body):
    page(fname, f"{title} — Ezra Vernon", desc, f"""<section class="page-head legal-head">
  <div class="wrap">
    <p class="eyebrow">The fine print</p>
    <h1>{h1}</h1>
    <p>{lede}</p>
    <p class="updated">Last updated {POLICY_UPDATED}</p>
  </div>
</section>
<section class="prose">
  <div class="wrap">
{body}
  </div>
</section>""", legal_css)


legal_page("privacy.html", "Privacy policy",
           "How Ezra Vernon's personal site handles your information: no accounts, no analytics, no ads and no cookies.",
           "Privacy policy", "What this site does, and doesn’t do, with information about you.", """    <div class="short">
      <h2>The short version</h2>
      <ul>
        <li>This is a personal site. It has no accounts, forms, newsletter, comments, analytics or ads.</li>
        <li>I don’t collect, sell or share personal information about visitors.</li>
        <li>The site sets no cookies. Two outside services are involved in showing you the pages: the host (Vercel) and the fonts (Google Fonts). Both see your IP address, as any web server does.</li>
      </ul>
    </div>

    <h2>Who runs this site</h2>
    <p>This is the personal website of Ezra Vernon, based in Victoria, British Columbia, Canada. “I” and “me” on this page mean Ezra. To reach me about anything here, use the links on the <a href="socials.html">Socials page</a>.</p>

    <h2>What I collect</h2>
    <p>Nothing directly. There is nowhere on this site to type in your name, email address or any other details, and I don’t run analytics, advertising or tracking tools, so I have no record of who visits or what they look at.</p>

    <h2>What happens automatically when you visit</h2>
    <h3>Hosting (Vercel)</h3>
    <p>The site is hosted by Vercel Inc. To send you a page, Vercel’s servers receive your IP address, your browser and device type, the page you asked for and the time of the request. Vercel uses this to deliver the site and to protect it from abuse, and keeps technical logs for a limited time. As the site owner I can see limited request logs in my hosting dashboard; I don’t use them to identify anyone. See <a href="https://vercel.com/legal/privacy-policy" rel="noopener">Vercel’s privacy policy</a>.</p>
    <h3>Fonts (Google Fonts)</h3>
    <p>The typefaces are loaded from Google Fonts. When your browser fetches them, Google receives your IP address, your browser type and the address of the page that asked for the font. Google says the Fonts service sets no cookies and limits what it keeps. See <a href="https://developers.google.com/fonts/faq/privacy" rel="noopener">Google Fonts’ privacy notes</a>.</p>

    <h2>The private section</h2>
    <p>“Sign in” in the menu opens a private, password-protected part of the site that is meant for me. The password is checked inside your browser and is never sent to me or to a server. If the password is right, your browser keeps a temporary key in its session storage so the section stays unlocked until you close the tab or press “Lock”. The <a href="cookies.html">Cookie policy</a> has the details.</p>

    <h2>My own data and photos</h2>
    <p>The <a href="training.html">Training log</a> shows my own activities from my watch. Routes and locations are left out on purpose.</p>
    <p>Some photos include other people. If you appear in a photo here and would like it taken down, tell me and I will remove it.</p>

    <h2>Links and getting in touch</h2>
    <p>This site links to other sites, including Instagram, LinkedIn and Strava. Once you follow a link, or message me on one of those platforms, that platform’s own privacy policy applies. I use what you send me only to reply to you.</p>

    <h2>Where information is processed</h2>
    <p>Vercel and Google run servers in the United States and other countries, so the technical information described above may be processed outside Canada and be subject to the laws of those places.</p>

    <h2>Your choices</h2>
    <ul>
      <li>You can browse every public page without giving any information about yourself.</li>
      <li>Because I don’t hold personal information about visitors, there is nothing for me to look up, correct or delete. Requests about server or font logs go to Vercel or Google.</li>
      <li>If you have messaged me through a social platform, you can delete that conversation there, or ask me to delete my copy.</li>
    </ul>

    <h2>Changes</h2>
    <p>If the site changes in a way that affects your privacy (for example, if I ever add a contact form or visitor statistics), I will update this page and the date at the top before the change goes live.</p>""")

legal_page("terms.html", "Terms and conditions",
           "The terms for using Ezra Vernon's personal site: content ownership, outdoor-activity disclaimer, links and liability.",
           "Terms and conditions", "The ground rules for using this site. By using it, you agree to them.", """    <div class="short">
      <h2>The short version</h2>
      <ul>
        <li>This is a personal site, shared for interest and fun. Nothing on it is professional advice.</li>
        <li>The mountains and challenges described here are dangerous. What you do outdoors is your own decision and your own risk.</li>
        <li>The writing, quotes, photos and logo belong to me unless credited to someone else. Please ask before reusing them.</li>
      </ul>
    </div>

    <h2>About these terms</h2>
    <p>This website is run by Ezra Vernon, an individual based in Victoria, British Columbia, Canada. These terms apply to everyone who visits. If you don’t agree with them, please don’t use the site.</p>

    <h2>Personal content, not advice</h2>
    <p>Everything here is my own experience, plans and opinions. I try to be accurate, but I make no promise that anything on the site is complete, correct or current. Elevations, route notes, distances and training figures in particular may be wrong or out of date.</p>

    <h2>Outdoor activities are at your own risk</h2>
    <p>Scrambling, mountaineering, glacier travel, skiing, climbing and long-distance running can cause serious injury or death. Nothing on this site is a guide, a route description, instruction or a recommendation that you attempt anything. Conditions change, and what I describe may not match what you find. If you head out, you are responsible for your own research, training, equipment and decisions, and for getting qualified instruction or a guide where it is needed.</p>
    <p>If we make plans together through this site or my social accounts, each person takes part at their own risk.</p>

    <h2>Who owns the content</h2>
    <p>Unless credited otherwise, the text, original quotes, photos, bird logo and design of this site are © Ezra Vernon, all rights reserved. The ultimate frisbee photo on the Home page is by Dan Tsuji Photography.</p>
    <p>You are welcome to link to the site and to quote a short passage, including one of my quotes, as long as you credit me by name. Please ask first before copying photos, the logo or longer pieces, or using anything commercially.</p>

    <h2>Using the site fairly</h2>
    <ul>
      <li>Don’t try to break, overload or interfere with the site.</li>
      <li>The private section behind “Sign in” is not public. Don’t try to get into it unless I have given you the password.</li>
      <li>Don’t pass off my content as your own, or use my name or logo in a way that suggests I endorse something.</li>
    </ul>

    <h2>Links to other sites</h2>
    <p>The site links to websites I don’t control, such as Instagram, LinkedIn, Strava and others. I’m not responsible for their content or for how they handle your information.</p>

    <h2>No warranty</h2>
    <p>The site is provided “as is” and “as available”. I don’t promise that it will always be online, free of errors or suitable for any particular purpose, and I may change or remove any part of it at any time.</p>

    <h2>Limit of liability</h2>
    <p>To the fullest extent the law allows, I am not liable for any loss, injury or damage that results from using this site or relying on anything on it. Nothing in these terms takes away rights you have by law that cannot be limited.</p>

    <h2>Privacy</h2>
    <p>How the site handles information is covered in the <a href="privacy.html">Privacy policy</a> and the <a href="cookies.html">Cookie policy</a>.</p>

    <h2>Governing law</h2>
    <p>These terms are governed by the laws of British Columbia and the federal laws of Canada that apply there. Any dispute will be dealt with by the courts of British Columbia.</p>

    <h2>Changes and contact</h2>
    <p>I may update these terms from time to time; the date at the top shows the latest version. Questions are welcome through the <a href="socials.html">Socials page</a>.</p>""")

legal_page("cookies.html", "Cookie policy",
           "Ezra Vernon's personal site sets no cookies. What is stored in your browser, when, and why there is no cookie banner.",
           "Cookie policy", "What this site stores in your browser, which is almost nothing.", """    <div class="short">
      <h2>The short version</h2>
      <ul>
        <li>This site sets no cookies, and uses no analytics, advertising or tracking.</li>
        <li>One item is kept in your browser, and only if you unlock the private section with the correct password.</li>
        <li>That is why there is no cookie banner: there is nothing here that needs your consent.</li>
      </ul>
    </div>

    <h2>What cookies are</h2>
    <p>Cookies are small text files a website saves in your browser, often to remember you or to follow what you do across pages and sites. Browsers also offer similar tools, such as “local storage” and “session storage”. This page covers all of them.</p>

    <h2>What this site stores on your device</h2>
    <div class="table-scroll" role="region" aria-label="Items stored in your browser" tabindex="0">
      <table>
        <caption>Everything this site stores in your browser</caption>
        <thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">When it is set</th><th scope="col">What it is for</th><th scope="col">How long it lasts</th></tr></thead>
        <tbody><tr><th scope="row"><code>ev-vault</code></th><td>Session storage (not a cookie)</td><td>Only after you choose “Sign in” and enter the correct password</td><td>Keeps the private section unlocked as you move between pages</td><td>Until you close the tab or press “Lock”</td></tr></tbody>
      </table>
    </div>
    <p>This item is needed for a feature you have asked for, it never leaves your browser, and it is not used to track you. If you never sign in, the site stores nothing at all.</p>

    <h2>Other services</h2>
    <ul>
      <li><strong>Vercel (hosting)</strong> does not set cookies when it serves these pages normally. If its security systems suspect automated or abusive traffic, they may show a short browser check and set a short-lived security cookie so you are not checked again straight away.</li>
      <li><strong>Google Fonts</strong> delivers the typefaces. Google says the Fonts service sets no cookies. It does receive your IP address, as explained in the <a href="privacy.html">Privacy policy</a>.</li>
      <li><strong>Links to other sites</strong> such as Instagram, LinkedIn and Strava: those sites use their own cookies once you are on them, under their own policies. Nothing from them is embedded here.</li>
    </ul>

    <h2>Why there is no cookie banner</h2>
    <p>Consent banners are for cookies and trackers that are not essential, such as analytics and advertising. This site has none. If I ever add something that does need your permission, I will update this page and ask before anything is stored.</p>

    <h2>Clearing what is stored</h2>
    <p>Pressing “Lock” in the private section, or closing the tab, removes the stored item. You can also clear site data for this site at any time in your browser’s privacy settings.</p>""")

legal_page("accessibility.html", "Accessibility",
           "Accessibility statement for Ezra Vernon's personal site: what has been done, known limits, and how to report a problem.",
           "Accessibility", "I want everyone to be able to read and use this site, whatever device or assistive technology they use.", """    <h2>What I’m aiming for</h2>
    <p>The site is built to follow the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA.</p>

    <h2>What’s in place</h2>
    <ul>
      <li>Every page works with a keyboard alone, with a visible focus outline and a “Skip to content” link.</li>
      <li>Headings, landmarks, lists and tables are marked up so screen readers can navigate by them.</li>
      <li>Photos have text descriptions. Purely decorative images are hidden from assistive technology.</li>
      <li>Text and controls meet AA colour contrast, and nothing relies on colour alone.</li>
      <li>Pages reflow on small screens and when zoomed, without sideways scrolling.</li>
      <li>Animations are switched off when your device is set to reduce motion.</li>
      <li>The charts on the <a href="training.html">Training log</a> have the same numbers available as a table and a list.</li>
    </ul>

    <h2>Known limits</h2>
    <ul>
      <li>I check the site with automated accessibility tests and by keyboard. It has not had a professional audit or testing with every screen reader.</li>
      <li>The charts on the Training log are drawn as graphics. Each bar and slice has a text label, but the table and list are the easier way to read the data.</li>
      <li>Some text sits over photographs. It has a dark overlay behind it, but contrast can vary a little with the photo.</li>
      <li>Sites I link to, such as Instagram, LinkedIn and Strava, are outside my control.</li>
    </ul>

    <h2>Tell me about a problem</h2>
    <p>If something on this site is hard to use or doesn’t work with your setup, please let me know through the <a href="socials.html">Socials page</a>, and tell me the page and what went wrong. I will do my best to fix it.</p>""")


# ---------------------------------------------------------------- THOUGHTS (public; source tools/thoughts/thoughts.json, filled weekly from Notion)
import importlib.util as _ilu, re as _re, datetime as _dt
_spec = _ilu.spec_from_file_location("site_secret", pathlib.Path(__file__).parent / "secret.py")
_sec = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_sec)
_tsrc = pathlib.Path(__file__).parent / "thoughts" / "thoughts.json"
_thoughts = json.loads(_tsrc.read_text(encoding="utf-8")).get("thoughts", []) if _tsrc.exists() else []
_thoughts = [t for t in _thoughts if (t.get("body_md") or "").strip()]
_thoughts.sort(key=lambda t: t.get("date") or "", reverse=True)

def _thought(t, i):
    md = _re.sub(r"\s*(?:<br\s*/?>\s*){2,}\s*", "\n\n", t.get("body_md") or "")   # Notion's double line breaks -> paragraphs
    d = _sec.nice_date(t.get("date"))
    iso = (t.get("date") or "")[:10]
    when = f'<p class="eyebrow"><time datetime="{iso}">{d}</time></p>' if d else ""
    title = f'<h2>{_sec.esc(t["name"])}</h2>' if t.get("name") else ""
    return f'<article class="thought reveal" id="t-{_sec.slug(t.get("name") or "thought")}-{i}">{when}{title}<div class="t-body">{_sec.markdown(md)}</div></article>'

t_css = """
.thoughts{padding-block:0 var(--s8)}
.thought{padding-block:var(--s5);border-top:1px solid var(--line);max-width:var(--measure)}
.thought .eyebrow{margin-bottom:var(--s1)}
.thought h2{font-size:var(--step-2);margin:0 0 var(--s2)}
.t-body p,.t-body li{font-size:var(--step-0);line-height:1.7}
.t-body p:last-child{margin-bottom:0}
.t-body h2,.t-body h3,.t-body h4{font-size:var(--step-1);margin:var(--s4) 0 var(--s1)}
.t-body blockquote{margin:0 0 var(--s3);padding-left:var(--s2);border-left:2px solid var(--accent)}
.t-body ul,.t-body ol{padding-left:1.2em;margin:0 0 var(--s3)}
.t-empty{border:1px dashed var(--line);border-radius:var(--radius);padding:var(--s4);color:var(--ink-soft)}
"""
_n = len(_thoughts)
t_body = f"""<section class="page-head">
  <div class="wrap reveal">
    <h1>Thoughts</h1>
    <p>Things I’ve been thinking about.</p>
  </div>
</section>
<section class="thoughts">
  <div class="wrap">
    {"".join(_thought(t, i) for i, t in enumerate(_thoughts)) or '<p class="t-empty">No thoughts yet. Check back soon.</p>'}
  </div>
</section>"""
page("thoughts.html", "Thoughts — Ezra Vernon",
     "Thoughts and reflections from Ezra Vernon, written as they come.", t_body, t_css)

# ---------------------------------------------------------------- 404
nf_body = """<section class="page-head" style="padding-bottom:var(--s8)">
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
