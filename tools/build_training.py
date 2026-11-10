# Training page builder — exec'd from build.py (shares page(), OUT, json, pathlib).
# Source: tools/coros/activities.tsv, pulled from Ezra's COROS account. Only date, sport, duration, distance/sets,
# Ezra's own activity titles and average heart rate (Ezra asked for HR) are kept. No coordinates, place names or calories reach the site.
import collections, datetime as _dt, html as _html

SPORT = {100: ("Run", "running"), 101: ("Indoor run", "running"), 102: ("Trail run", "running"),
         104: ("Hike", "hiking"), 200: ("Ride", "other"), 402: ("Strength", "strength"), 700: ("Rowing", "other"),
         800: ("Indoor climb", "climbing"), 801: ("Bouldering", "climbing"), 802: ("Outdoor climb", "climbing"),
         900: ("Walk", "other"), 1003: ("Soccer", "soccer"), 1100: ("Ultimate", "ultimate"), 500: ("Ski", "skiing")}
FILTERS = [("all", "All"), ("running", "Running"), ("hiking", "Hiking"), ("climbing", "Climbing"),
           ("ultimate", "Ultimate"), ("soccer", "Soccer"), ("strength", "Strength"), ("skiing", "Skiing"), ("other", "Other")]
# Recordings that are clearly not the sport they're labelled as (e.g. a car drive logged as frisbee).
EXCLUDE = {("2026-05-26", 1100, "1:25:33")}
import zoneinfo
UPDATED = _dt.datetime.now(zoneinfo.ZoneInfo("America/Vancouver")).date().isoformat()  # date the page was rebuilt

def secs(t):
    n = [int(x) for x in t.split(":")]
    return n[0] * 3600 + n[1] * 60 + n[2] if len(n) == 3 else n[0] * 60 + n[1]

def fmt_dur(sec):
    h, m = divmod(sec // 60, 60)
    return f"{h}h {m:02d}m" if h else f"{m} min"

acts = []
src = pathlib.Path(__file__).resolve().parent / "coros" / "activities.tsv"
for line in src.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"):
        continue
    date, code, dur, dist, hr, title = (line.split("\t") + ["", ""])[:6]
    code = int(code)
    if (date, code, dur) in EXCLUDE:
        continue
    label, group = SPORT.get(code, ("Activity", "other"))
    meters = sets = None
    if dist.endswith(" km"):
        meters = round(float(dist[:-3]) * 1000)
    elif dist.endswith(" m"):
        meters = int(dist[:-2])
    elif dist.startswith("sets "):
        sets = int(dist[5:])
    a = {"date": date, "sport": label, "group": group, "seconds": secs(dur), "hr": int(hr)}
    if meters is not None: a["meters"] = meters
    if sets is not None: a["sets"] = sets
    if title.strip(): a["title"] = title.strip()
    acts.append(a)
acts.sort(key=lambda a: a["date"], reverse=True)  # stable: keeps COROS same-day order
(OUT / "data").mkdir(exist_ok=True)
(OUT / "data" / "activities.json").write_text(json.dumps({"updated": UPDATED, "source": "COROS", "activities": acts}, indent=1), encoding="utf-8")

# ---- figures
runs = [a for a in acts if a["group"] == "running" and a.get("meters")]
total_h = sum(a["seconds"] for a in acts) / 3600
run_km = sum(a["meters"] for a in runs) / 1000
longest_run = max(runs, key=lambda a: a["meters"])
hikes = [a for a in acts if a["group"] == "hiking"]
longest_hike = max(hikes, key=lambda a: a["seconds"])
months = collections.OrderedDict()
first = _dt.date.fromisoformat(min(a["date"] for a in acts)).replace(day=1)
last = _dt.date.fromisoformat(max(a["date"] for a in acts)).replace(day=1)
d = first
while d <= last:
    months[d.strftime("%Y-%m")] = 0.0
    d = (d.replace(day=28) + _dt.timedelta(days=4)).replace(day=1)
for a in acts:
    months[a["date"][:7]] += a["seconds"] / 3600
busiest = max(months, key=months.get)
avg_hr = sum(a["hr"] * a["seconds"] for a in acts) / sum(a["seconds"] for a in acts)  # time-weighted
hardest = max((a for a in acts if a["seconds"] >= 20 * 60), key=lambda a: a["hr"])
# ---- activity mix (pie). Colour follows the group, fixed slot order (validated palette, 6 slots incl. wrap-around pair)
MIX = [("running", "Running", "#2a78d6"), ("strength", "Strength", "#eb6834"), ("hiking", "Hiking", "#1baf7a"),
       ("ultimate", "Ultimate", "#eda100"), ("soccer", "Soccer", "#e87ba4"), ("other", "Other", "#008300")]
MIX_OF = {"climbing": "other", "skiing": "other"}  # small groups fold into Other for the pie only
mix = []
for g, label, col in MIX:
    items = [a for a in acts if MIX_OF.get(a["group"], a["group"]) == g]
    if items:
        mix.append((g, label, col, items))
mname = lambda k, fmt="%B": _dt.date.fromisoformat(k + "-01").strftime(fmt)
dnice = lambda s: _dt.date.fromisoformat(s).strftime("%b %-d, %Y")

def pace(a):
    if a["group"] != "running" or not a.get("meters") or a["meters"] < 1000:
        return ""
    p = a["seconds"] / (a["meters"] / 1000)
    if p > 15 * 60:  # watch left running through stops — pace isn't meaningful
        return ""
    return f"{int(p // 60)}:{int(p % 60):02d} /km"

def amount(a):
    if a.get("meters"):
        return f"{a['meters'] / 1000:.2f} km" if a["meters"] >= 1000 else f"{a['meters']} m"
    if a.get("sets"):
        return f"{a['sets']} sets"
    return ""

# ---- monthly chart (single series → no legend; title names it; table + log carry the numbers)
W, H, PADL, PADB, PADT = 720, 260, 40, 32, 16
keys = list(months)
ymax = max(10, int((max(months.values()) + 9) // 10 * 10))
bw = (W - PADL) / len(keys)
bars, grid = [], []
for v in range(0, ymax + 1, 10):
    y = PADT + (H - PADT - PADB) * (1 - v / ymax)
    grid.append(f'<line x1="{PADL}" x2="{W}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/><text x="{PADL - 8}" y="{y + 4:.1f}" class="ytick">{v}</text>')
for i, k in enumerate(keys):
    v = months[k]
    h = (H - PADT - PADB) * v / ymax
    x = PADL + i * bw + bw * 0.22
    w = bw * 0.56
    y0 = H - PADB
    r = min(4, w / 2, h)
    path = (f"M{x:.1f},{y0} V{y0 - h + r:.1f} Q{x:.1f},{y0 - h:.1f} {x + r:.1f},{y0 - h:.1f} "
            f"H{x + w - r:.1f} Q{x + w:.1f},{y0 - h:.1f} {x + w:.1f},{y0 - h + r:.1f} V{y0} Z") if h > 0 else ""
    n = sum(1 for a in acts if a["date"].startswith(k))
    tip = f"{mname(k)} {k[:4]}: {v:.1f} hours · {n} activities"
    bars.append(f'<g class="bar" tabindex="0" role="img" aria-label="{tip}" data-tip="{tip}">'
                f'<rect x="{PADL + i * bw:.1f}" y="{PADT}" width="{bw:.1f}" height="{H - PADT - PADB}" class="hit"/>'
                f'<path d="{path}"/><text x="{PADL + i * bw + bw / 2:.1f}" y="{H - 10}" class="xtick">{mname(k, "%b")}</text></g>')
chart_svg = (f'<svg viewBox="0 0 {W} {H}" class="chart" aria-labelledby="chart-title" role="group">'
             f'{"".join(grid)}<line x1="{PADL}" x2="{W}" y1="{H - PADB}" y2="{H - PADB}" class="axis"/>{"".join(bars)}</svg>')
table_rows = "".join(f"<tr><th scope=\"row\">{mname(k)} {k[:4]}</th><td>{months[k]:.1f}</td><td>{sum(1 for a in acts if a['date'].startswith(k))}</td></tr>" for k in keys)

import math
CX = CY = 120; R = 112
slices, legend, ang = [], [], -math.pi / 2
total = len(acts)
for g, label, col, items in mix:
    n = len(items); frac = n / total; a2 = ang + frac * 2 * math.pi
    large = 1 if frac > 0.5 else 0
    x1, y1 = CX + R * math.cos(ang), CY + R * math.sin(ang)
    x2, y2 = CX + R * math.cos(a2), CY + R * math.sin(a2)
    pct = round(frac * 100)
    ghr = round(sum(a["hr"] * a["seconds"] for a in items) / sum(a["seconds"] for a in items))
    sub = sorted({a["sport"] for a in items})
    tip = f"{label}: {pct}% · {n} activities · avg {ghr} bpm"
    # label on the slice where it fits
    mid = (ang + a2) / 2
    lbl = (f'<text x="{CX + R * .64 * math.cos(mid):.1f}" y="{CY + R * .64 * math.sin(mid) + 5:.1f}" class="slice-label"'
           f'{" style=\"fill:#0b0b0b\"" if col == "#eda100" else ""}>{pct}%</text>') if frac >= 0.06 else ""
    slices.append(f'<g class="slice" tabindex="0" role="img" aria-label="{tip}" data-tip="{tip}">'
                  f'<path d="M{CX},{CY} L{x1:.2f},{y1:.2f} A{R},{R} 0 {large} 1 {x2:.2f},{y2:.2f} Z" fill="{col}"/>{lbl}</g>')
    legend.append(f'<li><span class="sw" style="background:{col}" aria-hidden="true"></span><span class="lg-name">{label}'
                  f'{"<small>" + ", ".join(sub) + "</small>" if len(sub) > 1 else ""}</span>'
                  f'<span class="lg-n">{n}</span><span class="lg-pct">{pct}%</span><span class="lg-hr">{ghr} bpm</span></li>')
    ang = a2
pie_svg = f'<svg viewBox="0 0 240 240" class="pie" role="group" aria-labelledby="mix-title">{"".join(slices)}</svg>'

# ---- log grouped by month
groups = collections.OrderedDict()
for a in acts:
    groups.setdefault(a["date"][:7], []).append(a)
log = []
for k, items in groups.items():
    rows = []
    for a in items:
        name = _html.escape(a.get("title") or a["sport"])
        meta = " · ".join(x for x in (amount(a), pace(a), f'{a["hr"]} bpm avg') if x)
        tag = f'<span class="tag">{a["sport"]}</span>' if a.get("title") else ""
        dt = _dt.date.fromisoformat(a["date"])
        rows.append(f'<li class="act" data-group="{a["group"]}"><time datetime="{a["date"]}"><b>{dt.day}</b><span>{dt.strftime("%a")}</span></time>'
                    f'<div class="what"><strong>{name}</strong>{tag}</div>'
                    f'<div class="how"><span>{fmt_dur(a["seconds"])}</span><span class="meta">{meta}</span></div></li>')
    log.append(f'<section class="month" aria-labelledby="m-{k}"><h3 id="m-{k}">{mname(k)} <span>{k[:4]}</span></h3><ol class="acts">{"".join(rows)}</ol></section>')
present = {a["group"] for a in acts}
chips = "".join(f'<button type="button" class="chip" data-filter="{f}" aria-pressed="{"true" if f == "all" else "false"}">{l}</button>'
                for f, l in FILTERS if f == "all" or f in present)

t_css = """
.stats{display:grid;gap:var(--s3);grid-template-columns:repeat(2,1fr);margin:0}
@media (min-width:900px){.stats{grid-template-columns:repeat(4,1fr)}}
.stat-tile{border-top:1px solid var(--ink);padding-top:var(--s2)}
.stat-tile dt{font-size:var(--step--1);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft)}
.stat-tile dd{margin:var(--s1) 0 0;font-family:var(--font-serif);font-size:clamp(var(--step-3),4vw,var(--step-5));line-height:1}
.stat-tile dd small{display:block;font-family:var(--font-sans);font-size:var(--step--1);color:var(--ink-soft);margin-top:var(--s1);line-height:1.4}
.highlights{display:grid;gap:var(--s3);grid-template-columns:1fr;margin-top:var(--s5)}
@media (min-width:760px){.highlights{grid-template-columns:repeat(3,1fr)}}
.hl{border:1px solid var(--line);border-radius:var(--radius);padding:var(--s3);background:var(--base)}
.hl p{margin:0}
.hl .eyebrow{margin-bottom:var(--s1)}
.hl .big{font-family:var(--font-serif);font-size:var(--step-2);line-height:1.2}
.hl .sub{color:var(--ink-soft);font-size:var(--step--1);margin-top:var(--s1)}
.chart-wrap{position:relative;margin-top:var(--s3)}
.chart{width:100%;height:auto;display:block;overflow:visible}
.chart .grid{stroke:var(--line);stroke-width:1}
.chart .axis{stroke:var(--ink-soft);stroke-width:1}
.chart .ytick{font:400 12px var(--font-sans);fill:var(--ink-soft);text-anchor:end}
.chart .xtick{font:400 12px var(--font-sans);fill:var(--ink-soft);text-anchor:middle}
.chart .bar path{fill:var(--accent);transition:opacity var(--t-fast) var(--ease)}
.chart .bar .hit{fill:transparent}
.chart:hover .bar path{opacity:.45}
.chart .bar:hover path,.chart .bar:focus path{opacity:1}
.chart .bar:focus{outline:none}
.chart .bar:focus-visible .hit{stroke:var(--accent);stroke-width:2}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:var(--base);font-size:var(--step--1);padding:var(--s1) var(--s2);border-radius:var(--radius);white-space:nowrap;transform:translate(-50%,-100%);opacity:0;transition:opacity var(--t-fast)}
.tip.on{opacity:1}
details.data{margin-top:var(--s3);font-size:var(--step--1)}
details.data summary{cursor:pointer;color:var(--accent)}
details.data table{border-collapse:collapse;margin-top:var(--s2);min-width:min(420px,100%)}
details.data th,details.data td{text-align:left;padding:var(--s1) var(--s2);border-bottom:1px solid var(--line);font-weight:400}
details.data td{font-variant-numeric:tabular-nums}
.filters{display:none;flex-wrap:wrap;gap:var(--s1);margin-bottom:var(--s4)}
.js .filters{display:flex}
.chip{font:500 var(--step--1)/1 var(--font-sans);padding:var(--s1) var(--s2);border-radius:999px;border:1px solid var(--line);background:var(--base);color:var(--ink);cursor:pointer;transition:border-color var(--t-fast),background var(--t-fast),color var(--t-fast)}
.chip:hover{border-color:var(--accent)}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--base)}
.count{color:var(--ink-soft);font-size:var(--step--1);margin:0 0 var(--s4)}
.month{margin-bottom:var(--s5)}
.month h3{font-size:var(--step-2);padding-bottom:var(--s1);border-bottom:1px solid var(--ink);margin-bottom:0;position:sticky;top:72px;background:var(--base);z-index:2;padding-top:var(--s2)}
.month h3 span{color:var(--ink-soft)}
.acts{list-style:none;margin:0;padding:0}
.act{display:grid;grid-template-columns:56px 1fr;gap:var(--s1) var(--s3);padding-block:var(--s2);border-bottom:1px solid var(--line);align-items:center}
@media (min-width:760px){.act{grid-template-columns:64px 1fr auto}}
.act[hidden],.month[hidden]{display:none}
.act time{display:flex;flex-direction:column;line-height:1.1;grid-row:span 2}
@media (min-width:760px){.act time{grid-row:auto}}
.act time b{font-family:var(--font-serif);font-weight:400;font-size:var(--step-2)}
.act time span{font-size:var(--step--1);color:var(--ink-soft)}
.what{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s1) var(--s2)}
.what strong{font-weight:500}
.tag{font-size:var(--step--1);border:1px solid var(--line);border-radius:999px;padding:0 var(--s1);color:var(--ink-soft)}
.how{display:flex;gap:var(--s2);font-variant-numeric:tabular-nums;font-size:var(--step-0)}
@media (min-width:760px){.how{justify-content:flex-end;text-align:right}}
.how .meta{color:var(--ink-soft)}
.source{color:var(--ink-soft);font-size:var(--step--1)}
@media (min-width:760px){.highlights{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1100px){.highlights{grid-template-columns:repeat(4,1fr)}}
/* Activity mix pie: the one place the site uses more than its single accent (Ezra asked for colour here) */
.mix{display:grid;gap:var(--s5);align-items:center;margin-top:var(--s3)}
@media (min-width:900px){.mix{grid-template-columns:minmax(240px,360px) 1fr;gap:var(--s7)}}
.pie{width:100%;max-width:360px;height:auto;display:block;overflow:visible}
.pie path{stroke:var(--base-deep);stroke-width:2;stroke-linejoin:round;transition:opacity var(--t-fast) var(--ease),transform var(--t-med) var(--ease);transform-origin:120px 120px}
.pie:hover .slice path{opacity:.5}
.pie .slice:hover path,.pie .slice:focus path{opacity:1;transform:scale(1.03)}
.pie .slice:focus{outline:none}
.pie .slice:focus-visible path{stroke:var(--ink)}
.slice-label{font:500 13px var(--font-sans);fill:#fff;text-anchor:middle;pointer-events:none}
.legend{list-style:none;margin:0;padding:0}
.legend li{display:grid;grid-template-columns:16px 1fr 48px 48px 80px;gap:var(--s2);align-items:baseline;padding-block:var(--s1);border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
.legend li.head{font-size:var(--step--1);color:var(--ink-soft);letter-spacing:.04em}
.legend .sw{width:16px;height:16px;border-radius:4px;align-self:center}
.legend .lg-name small{display:block;font-size:var(--step--1);color:var(--ink-soft)}
.legend .lg-n,.legend .lg-pct,.legend .lg-hr{text-align:right}
.legend .lg-hr{color:var(--ink-soft);white-space:nowrap}
"""

t_body = f"""<section class="page-head">
  <div class="wrap reveal">
    <p class="eyebrow">Page 05</p>
    <h1>Training log</h1>
    <p>Data and activities from my watch. Updated {_dt.date.fromisoformat(UPDATED).strftime('%B %-d, %Y')}.</p>
  </div>
</section>

<section class="section section--tint" aria-labelledby="totals" style="padding-top:var(--s6)">
  <div class="wrap">
    <h2 id="totals" class="eyebrow">Since {mname(keys[0])} {keys[0][:4]}</h2>
    <dl class="stats reveal">
      <div class="stat-tile"><dt>Activities</dt><dd>{len(acts)}</dd></div>
      <div class="stat-tile"><dt>Hours moving</dt><dd>{total_h:.0f}</dd></div>
      <div class="stat-tile"><dt>Kilometres run</dt><dd>{run_km:.0f}<small>road + trail</small></dd></div>
      <div class="stat-tile"><dt>Avg heart rate</dt><dd>{avg_hr:.0f}<small>bpm, across all activity time</small></dd></div>
    </dl>
    <div class="highlights">
      <div class="hl reveal"><p class="eyebrow">Longest run</p><p class="big">{_html.escape(longest_run.get('title', longest_run['sport']))}</p><p class="sub">{longest_run['meters']/1000:.2f} km · {fmt_dur(longest_run['seconds'])} · {dnice(longest_run['date'])}</p></div>
      <div class="hl reveal"><p class="eyebrow">Longest day out</p><p class="big">{fmt_dur(longest_hike['seconds'])} hiking</p><p class="sub">{longest_hike['meters']/1000:.1f} km · {dnice(longest_hike['date'])}</p></div>
      <div class="hl reveal"><p class="eyebrow">Busiest month</p><p class="big">{mname(busiest)} {busiest[:4]}</p><p class="sub">{months[busiest]:.1f} hours · {sum(1 for a in acts if a['date'].startswith(busiest))} activities</p></div>
      <div class="hl reveal"><p class="eyebrow">Hardest effort</p><p class="big">{hardest['hr']} bpm average</p><p class="sub">{_html.escape(hardest.get('title', hardest['sport']))} · {amount(hardest)} · {fmt_dur(hardest['seconds'])} · {dnice(hardest['date'])}</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="chart-title">
  <div class="wrap">
    <h2 id="chart-title" style="font-size:var(--step-3)">Hours per month</h2>
    <div class="chart-wrap reveal">{chart_svg}<div class="tip" aria-hidden="true"></div></div>
    <details class="data"><summary>Show as a table</summary>
      <table><thead><tr><th scope="col">Month</th><th scope="col">Hours</th><th scope="col">Activities</th></tr></thead><tbody>{table_rows}</tbody></table>
    </details>
  </div>
</section>

<section class="section section--tint" aria-labelledby="mix-title">
  <div class="wrap">
    <h2 id="mix-title" style="font-size:var(--step-3)">Activity mix</h2>
    <p>Share of all {total} activities, by sport.</p>
    <div class="mix">
      <div class="chart-wrap reveal">{pie_svg}<div class="tip" aria-hidden="true"></div></div>
      <ul class="legend reveal"><li class="head" aria-hidden="true"><span></span><span>Sport</span><span class="lg-n">Count</span><span class="lg-pct">Share</span><span class="lg-hr">Avg HR</span></li>{"".join(legend)}</ul>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="log-title">
  <div class="wrap">
    <h2 id="log-title" style="font-size:var(--step-3)">Every activity</h2>
    <div class="filters" role="group" aria-label="Filter by sport">{chips}</div>
    <p class="count" aria-live="polite">{len(acts)} activities</p>
    {"".join(log)}
    <p class="source">Data from my COROS watch. Heart rate is the average for each activity. Routes and locations are left out on purpose.</p>
  </div>
</section>"""

t_js = """(function(){
  // Sport filter
  var chips=[].slice.call(document.querySelectorAll('.chip')),acts=[].slice.call(document.querySelectorAll('.act')),
      months=[].slice.call(document.querySelectorAll('.month')),count=document.querySelector('.count');
  chips.forEach(function(c){c.addEventListener('click',function(){
    var f=c.dataset.filter,n=0;
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c)});
    acts.forEach(function(a){var on=f==='all'||a.dataset.group===f;a.hidden=!on;if(on)n++});
    months.forEach(function(m){m.hidden=!m.querySelector('.act:not([hidden])')});
    count.textContent=n+(n===1?' activity':' activities');
  })});
  // Chart tooltips (bars + pie slices)
  [].forEach.call(document.querySelectorAll('.chart-wrap'),function(wrap){
  var tip=wrap.querySelector('.tip');if(!tip)return;
  function show(b){var r=b.querySelector('path').getBoundingClientRect(),w=wrap.getBoundingClientRect();
    if(!r.height){r=b.getBoundingClientRect()}
    tip.textContent=b.dataset.tip;tip.style.left=(r.left-w.left+r.width/2)+'px';tip.style.top=(r.top-w.top-8)+'px';tip.classList.add('on')}
  [].forEach.call(wrap.querySelectorAll('.bar,.slice'),function(b){
    b.addEventListener('mouseenter',function(){show(b)});b.addEventListener('focus',function(){show(b)});
    b.addEventListener('mouseleave',function(){tip.classList.remove('on')});b.addEventListener('blur',function(){tip.classList.remove('on')});
  });});
})();"""

page("training.html", "Training log — Ezra Vernon",
     "Every run, hike, climb, ultimate and soccer session from Ezra Vernon's COROS watch, newest first, with monthly totals.",
     t_body, t_css, t_js)
