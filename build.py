#!/usr/bin/env python3
"""
Build the static site for ravikrali/resume.

Reads JSON from content/ and writes plain HTML to the repo root, so GitHub
Pages can serve it with no build step of its own.

    python build.py

Edit the JSON, re-run, commit. Nothing else to install.
"""

from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
POV_DIR = ROOT / "perspectives"

SITE_URL = "https://ravikrali.github.io/resume"
FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Fraunces:opsz,wght@9..144,300..700"
    "&family=Archivo:wght@400;500;600"
    "&family=IBM+Plex+Mono:wght@400;500"
    "&display=swap"
)

# Short labels for the role tags on perspective cards.
ROLE_SHORT = {
    "Enterprise AI Architect": "AI Architect",
    "Director, AI & Data Management": "Director, AI & Data",
    "Enterprise Data Architect": "Data Architect",
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def e(text) -> str:
    """Escape for HTML text/attribute context."""
    return html.escape(str(text), quote=True)


def load(name: str):
    with (CONTENT / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def paras(items, cls="") -> str:
    attr = f' class="{cls}"' if cls else ""
    return "\n".join(f"<p{attr}>{e(p)}</p>" for p in items)


def arrow(kind: str = "right") -> str:
    d = {
        "right": "M1 6h10M7 2l4 4-4 4",
        "down": "M6 1v10M2 7l4 4 4-4",
        "ext": "M3 9L9 3M4 3h5v5",
    }[kind]
    return (
        f'<svg class="arw" width="12" height="12" viewBox="0 0 12 12" fill="none" '
        f'aria-hidden="true"><path d="{d}" stroke="currentColor" stroke-width="1.4" '
        f'stroke-linecap="square"/></svg>'
    )


# --------------------------------------------------------------------------
# shared chrome
# --------------------------------------------------------------------------

def head(title: str, description: str, base: str, canonical: str, extra: str = "") -> str:
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d2340">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{base}assets/css/site.css">
<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def masthead(base: str, profile: dict, current: str = "") -> str:
    def mark(key: str) -> str:
        return ' aria-current="page"' if key == current else ""

    return f"""<header class="masthead">
  <div class="shell masthead__in">
    <a class="brand" href="{base}index.html">
      Ravi&nbsp;Rali
      <span class="brand__mark">Enterprise AI &amp; Data</span>
    </a>
    <nav class="navlinks" aria-label="Primary">
      <a href="{base}index.html#value">Value</a>
      <a href="{base}index.html#roadmap">Roadmap</a>
      <a href="{base}index.html#skills">Skills</a>
      <a class="nav-keep" href="{base}perspectives/index.html"{mark('pov')}>Perspectives</a>
      <a class="btn" href="{base}index.html#contact">Get in touch {arrow()}</a>
    </nav>
  </div>
</header>
"""


def footer(base: str, profile: dict) -> str:
    return f"""<footer class="footer">
  <div class="shell footer__in">
    <span>&copy; <span data-year>{date.today().year}</span> Ravi Kiran Rali</span>
    <span>Built as a static site &middot; <a href="{e(profile['github'])}/resume">source</a></span>
    <span><a href="{e(profile['linkedin'])}">LinkedIn</a> &middot; <a href="mailto:{e(profile['email'])}">Email</a></span>
  </div>
</footer>
<script src="{base}assets/js/site.js" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# index sections
# --------------------------------------------------------------------------

def hero(profile: dict) -> str:
    first, *rest = profile["name"].split(" ")
    surname = " ".join(rest)

    roles = "".join(f"<span>{e(r)}</span>" for r in profile["titles"])
    metrics = "".join(
        f"""<div class="metric">
          <div class="metric__fig">{e(m['figure'])}{f'<span class="unit">{e(m["unit"])}</span>' if m['unit'] else ''}</div>
          <p class="metric__label">{e(m['label'])}</p>
        </div>"""
        for m in profile["metrics"]
    )

    return f"""<section class="hero">
  <div class="shell">
    <div class="hero__grid">
      <div class="stagger">
        <p class="eyebrow">Enterprise Architecture &middot; AI &middot; Data Management</p>
        <h1 class="display hero__name">{e(first)} <span class="surname">{e(surname)}</span></h1>
        <div class="hero__roles">{roles}</div>
        <p class="hero__tagline">{e(profile['tagline'])}</p>
        <div class="hero__actions">
          <a class="btn" href="#roadmap">View the roadmap {arrow()}</a>
          <a class="btn btn--ghost" href="perspectives/index.html">Read my perspectives {arrow()}</a>
          <a class="btn btn--ghost" href="{e(profile['resumePdf'])}">Download CV {arrow('down')}</a>
        </div>
      </div>
      <figure class="hero__portrait">
        <img src="{e(profile['photo'])}" alt="Portrait of Ravi Kiran Rali" width="640" height="800">
        <figcaption class="hero__loc">{e(profile['location'])}</figcaption>
      </figure>
    </div>
    <div class="metrics">{metrics}</div>
  </div>
</section>
"""


def summary_and_value(profile: dict) -> str:
    cards = "".join(
        f"""<article class="value__card">
          <span class="value__num">{e(v['num'])}</span>
          <h3>{e(v['title'])}</h3>
          <p>{e(v['body'])}</p>
          <p class="value__proof">{e(v['proof'])}</p>
        </article>"""
        for v in profile["value"]
    )

    return f"""<section class="band" id="value">
  <div class="shell">
    <div class="summary__grid rise">
      <div>
        <p class="eyebrow">About</p>
      </div>
      <div class="summary__body">{paras(profile['summary'])}</div>
    </div>
    <div class="rise">
      <div class="band-head" style="margin-top:clamp(3rem,6vw,5rem)">
        <p class="eyebrow">What I bring</p>
        <h2 class="display">How I help organizations</h2>
      </div>
      <div class="value">{cards}</div>
    </div>
  </div>
</section>
"""


def roadmap(items: list) -> str:
    # --- ribbon: chronological, positioned by year with a minimum gap ------
    chrono = list(reversed(items))
    span_from, span_to = 1998, date.today().year
    positions, last = [], -99.0
    for it in chrono:
        pos = (int(it["yearShort"]) - span_from) / (span_to - span_from) * 100
        pos = max(pos, last + 5.0)
        positions.append(pos)
        last = pos
    over = positions[-1] - 100
    if over > 0:  # squeeze back inside the track
        positions = [p - over * (i / (len(positions) - 1)) for i, p in enumerate(positions)]

    dots = "".join(
        f'<button type="button" class="ribbon__dot" style="left:{pos:.2f}%" '
        f'data-target="{e(it["id"])}" data-year="{e(it["yearShort"])}" '
        f'aria-label="{e(it["org"])}, {e(it["years"])}"></button>'
        for it, pos in zip(chrono, positions)
    )

    # --- milestones grouped by era ----------------------------------------
    blocks, seen_era = [], None
    for it in items:
        if it["era"] != seen_era:
            seen_era = it["era"]
            blocks.append(f'<p class="rm__era">{e(seen_era)}</p>')

        outcomes = []
        for o in it["outcomes"]:
            metric = o.get("metric")
            unit = o.get("unit", "")
            cls = "rm__outcome" if metric else "rm__outcome rm__outcome--plain"
            fig = (
                f'{e(metric)}{f"<span class=\"u\">{e(unit)}</span>" if unit else ""}'
                if metric else ""
            )
            outcomes.append(
                f'<li class="{cls}">'
                f'<span class="rm__metric">{fig}</span>'
                f'<span>{e(o["text"])}</span></li>'
            )

        stack = "".join(f'<li class="chip">{e(s)}</li>' for s in it["stack"])
        links = "".join(
            f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{arrow("ext")} {e(l["label"])}</a>'
            for l in it.get("links", [])
        )
        links_block = f'<div class="rm__links">{links}</div>' if links else ""

        blocks.append(f"""<article class="rm__item" id="{e(it['id'])}">
  <button type="button" class="rm__head" aria-expanded="false" aria-controls="panel-{e(it['id'])}">
    <span class="rm__years">{e(it['years'])}</span>
    <span class="rm__title">
      <span class="rm__role">{e(it['role'])}</span>
      <span class="rm__org">{e(it['org'])} &middot; {e(it['location'])}</span>
    </span>
    <span class="rm__toggle" aria-hidden="true">{arrow('down')}</span>
  </button>
  <div class="rm__panel" id="panel-{e(it['id'])}">
    <div class="rm__panelin">
      <div class="rm__body">
        <div>
          <p class="rm__headline">{e(it['headline'])}</p>
          <p class="rm__context">{e(it['context'])}</p>
          <ul class="rm__outcomes">{''.join(outcomes)}</ul>
        </div>
        <div class="rm__aside">
          <div class="rm__note">
            <h4>Leadership</h4>
            <p>{e(it['leadership'])}</p>
          </div>
          <ul class="rm__stack">{stack}</ul>
          {links_block}
        </div>
      </div>
    </div>
  </div>
</article>""")

    return f"""<section class="band band--deep" id="roadmap">
  <div class="shell">
    <div class="band-head rise">
      <p class="eyebrow">The roadmap</p>
      <h2 class="display">Ten milestones across twenty-five years</h2>
      <p class="lede">From building a BI practice to architecting an enterprise AI platform over a global
      clinical trial portfolio. Each milestone describes what I built, the results, and my responsibilities.
      Select any milestone to expand it.</p>
    </div>

    <div class="ribbon rise" role="group" aria-label="Career timeline shortcuts">
      <div class="ribbon__line" aria-hidden="true"></div>
      <div class="ribbon__track">{dots}</div>
      <div class="ribbon__caps"><span>1998 &middot; Practice</span><span>Warehouse</span><span>Risk &amp; big data</span><span>Cloud</span><span>{date.today().year} &middot; Agentic</span></div>
    </div>

    <div class="rm" data-roadmap>
      {''.join(blocks)}
    </div>
  </div>
</section>
"""


def skills(data: dict) -> str:
    pillars = []
    for p in data["pillars"]:
        groups = "".join(
            f"""<div class="skillgroup">
              <h4>{e(g['name'])}</h4>
              <ul class="skilllist">{''.join(f'<li>{e(i)}</li>' for i in g['items'])}</ul>
            </div>"""
            for g in p["groups"]
        )
        pillars.append(f"""<section class="pillar">
  <p class="pillar__kicker">{e(p['kicker'])}</p>
  <h3>{e(p['title'])}</h3>
  <p class="pillar__lede">{e(p['lede'])}</p>
  {groups}
</section>""")

    return f"""<section class="band" id="skills">
  <div class="shell">
    <div class="band-head rise">
      <p class="eyebrow">Capability</p>
      <h2 class="display">Technical expertise and leadership experience</h2>
      <p class="lede">Senior roles in this field require someone who can discuss architecture in detail with
      engineers and investment priorities with executives. That is the work I have done for the last decade.</p>
    </div>
    <div class="pillars rise">{''.join(pillars)}</div>
  </div>
</section>
"""


def pov_teaser(povs: list) -> str:
    cards = "".join(pov_card(p, base="perspectives/") for p in povs)
    return f"""<section class="band band--deep" id="perspectives">
  <div class="shell">
    <div class="band-head rise">
      <p class="eyebrow">Points of view</p>
      <h2 class="display">My perspective on twelve common enterprise AI and data leadership challenges</h2>
      <p class="lede">Postings for an Enterprise AI Architect, a Director of AI &amp; Data Management, or an
      Enterprise Data Architect tend to ask for the same capabilities. These short articles explain the principles
      I use when making architecture and leadership decisions.</p>
    </div>
    <div class="povgrid rise">{cards}</div>
  </div>
</section>
"""


def pov_card(p: dict, base: str = "") -> str:
    tags = "".join(
        f'<li class="tag">{e(ROLE_SHORT.get(r, r))}</li>' for r in p["roles"]
    )
    return f"""<a class="povcard" href="{base}{e(p['slug'])}.html">
  <span class="povcard__top"><span class="povcard__num">{e(p['num'])}</span><span>Read {arrow()}</span></span>
  <h3>{e(p['title'])}</h3>
  <p class="povcard__req">&ldquo;{e(p['requirement'])}&rdquo;</p>
  <ul class="povcard__tags">{tags}</ul>
</a>"""


def contact(profile: dict) -> str:
    return f"""<section class="band contact" id="contact">
  <div class="shell contact__grid">
    <div class="rise">
      <p class="eyebrow">Contact</p>
      <h2>Let&rsquo;s discuss your data and AI architecture</h2>
      <p>Open to Enterprise AI Architect, Director of AI &amp; Data Management, and Enterprise Data Architect
      roles, permanent or advisory, remote or Raleigh-based.</p>
    </div>
    <div class="contact__list rise">
      <a href="mailto:{e(profile['email'])}"><span><span class="k">Email</span><br>{e(profile['email'])}</span>{arrow()}</a>
      <a href="{e(profile['linkedin'])}" target="_blank" rel="noopener"><span><span class="k">LinkedIn</span><br>/in/ravirali</span>{arrow('ext')}</a>
      <a href="{e(profile['resumePdf'])}"><span><span class="k">Curriculum vitae</span><br>PDF, one page</span>{arrow('down')}</a>
      <a href="{e(profile['github'])}" target="_blank" rel="noopener"><span><span class="k">GitHub</span><br>Published strategy notes</span>{arrow('ext')}</a>
    </div>
  </div>
</section>
"""


def credentials(profile: dict) -> str:
    rows = "".join(
        f"""<div class="cred">
          <strong>{e(c['title'])}</strong>
          <span>{e(c['org'])}</span>
          <time>{e(c['year'])}</time>
        </div>"""
        for c in profile["credentials"]
    )
    return f"""<section class="band" id="credentials">
  <div class="shell">
    <div class="band-head rise">
      <p class="eyebrow">Credentials</p>
      <h2 class="display">Education and professional credentials</h2>
    </div>
    <div class="creds rise">{rows}</div>
  </div>
</section>
"""


def jsonld(profile: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile["name"],
        "jobTitle": profile["titles"][0],
        "email": f"mailto:{profile['email']}",
        "url": SITE_URL,
        "sameAs": [profile["linkedin"], profile["github"]],
        "address": {"@type": "PostalAddress", "addressLocality": "Raleigh", "addressRegion": "NC", "addressCountry": "US"},
        "description": profile["tagline"],
        "knowsAbout": [
            "Enterprise Architecture", "Data Governance", "Master Data Management",
            "Agentic AI", "Retrieval-Augmented Generation", "Knowledge Graphs",
            "Snowflake", "Databricks", "TOGAF",
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


# --------------------------------------------------------------------------
# perspective pages
# --------------------------------------------------------------------------

def pov_page(p: dict, prev: dict | None, nxt: dict | None, profile: dict) -> str:
    sections = "".join(
        f"<section><h2>{e(s['h'])}</h2>{paras(s['p'])}</section>"
        for s in p["sections"]
    )
    apply_items = "".join(f"<li>{e(i)}</li>" for i in p["apply"])
    signal_items = "".join(f"<li>{e(i)}</li>" for i in p["signals"])
    roles = " &middot; ".join(e(r) for r in p["roles"])
    links = "".join(
        f'<a class="sourcelink" href="{e(l["url"])}" target="_blank" rel="noopener">{arrow("ext")} {e(l["label"])}</a>'
        for l in p.get("links", [])
    )

    def pager_cell(item, label, empty_cls=""):
        if not item:
            return f'<a class="is-empty" href="#"><span class="k">{label}</span><span class="t">&mdash;</span></a>'
        return (
            f'<a href="{e(item["slug"])}.html"><span class="k">{label}</span>'
            f'<span class="t">{e(item["title"])}</span></a>'
        )

    canonical = f"{SITE_URL}/perspectives/{p['slug']}.html"
    return (
        head(
            f"{p['title']} — Ravi Rali",
            p["standfirst"],
            "../",
            canonical,
        )
        + masthead("../", profile, current="pov")
        + f"""<main id="main">
<section class="povhero">
  <div class="shell">
    <p class="eyebrow"><a href="index.html" style="text-decoration:none">Perspectives</a></p>
    <div class="povhero__num" aria-hidden="true">{e(p['num'])}</div>
    <h1>{e(p['title'])}</h1>
    <p class="povhero__stand">{e(p['standfirst'])}</p>
    <div class="povmeta">
      <span>{roles}</span>
      <span>Point of view</span>
    </div>
  </div>
</section>

<section class="shell" style="padding-bottom:clamp(3rem,7vw,6rem)">
  <div class="reqcard">
    <p class="reqcard__k">The requirement this answers</p>
    <p class="reqcard__v">&ldquo;{e(p['requirement'])}&rdquo;</p>
  </div>

  <p class="position">{e(p['position'])}</p>

  <div class="prose">{sections}</div>

  <div class="twoup">
    <div class="twoup__col">
      <h3>How I apply it</h3>
      <ul class="ticklist">{apply_items}</ul>
    </div>
    <div class="twoup__col">
      <h3>What good looks like</h3>
      <ul class="ticklist">{signal_items}</ul>
    </div>
  </div>

  {links}

  <nav class="pager" aria-label="More perspectives">
    {pager_cell(prev, 'Previous')}
    {pager_cell(nxt, 'Next')}
  </nav>
</section>
</main>
"""
        + footer("../", profile)
    )


def pov_index(povs: list, profile: dict) -> str:
    cards = "".join(pov_card(p) for p in povs)
    return (
        head(
            "Perspectives — Ravi Rali",
            "Short points of view on AI strategy, data governance, MDM, agentic AI, "
            "architecture governance, and developing architects.",
            "../",
            f"{SITE_URL}/perspectives/index.html",
        )
        + masthead("../", profile, current="pov")
        + f"""<main id="main">
<section class="povhero">
  <div class="shell">
    <p class="eyebrow">Points of view</p>
    <h1>Some points of view on frequently asked questions</h1>
    <p class="povhero__stand">Twelve short pieces on the requirements that recur in Enterprise AI Architect,
    Director of AI &amp; Data Management, and Enterprise Data Architect postings. Each one takes about three
    minutes to read and sets out the principles I apply.</p>
    <div class="povmeta"><span>12 pieces</span><span>~3 min each</span><span>Updated {date.today().strftime('%B %Y')}</span></div>
  </div>
</section>
<section class="shell" style="padding-bottom:clamp(4rem,8vw,7rem)">
  <div class="povgrid">{cards}</div>
</section>
</main>
"""
        + footer("../", profile)
    )


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def build() -> None:
    profile = load("profile.json")
    rm_items = load("roadmap.json")
    skill_data = load("skills.json")
    povs = load("perspectives.json")

    POV_DIR.mkdir(exist_ok=True)

    index = (
        head(
            f"{profile['name']} — {profile['titles'][0]}",
            profile["tagline"],
            "",
            f"{SITE_URL}/",
            extra=jsonld(profile),
        )
        + masthead("", profile)
        + '<main id="main">'
        + hero(profile)
        + summary_and_value(profile)
        + roadmap(rm_items)
        + skills(skill_data)
        + pov_teaser(povs)
        + credentials(profile)
        + contact(profile)
        + "</main>"
        + footer("", profile)
    )
    (ROOT / "index.html").write_text(index, encoding="utf-8")

    (POV_DIR / "index.html").write_text(pov_index(povs, profile), encoding="utf-8")
    for i, p in enumerate(povs):
        prev = povs[i - 1] if i > 0 else None
        nxt = povs[i + 1] if i < len(povs) - 1 else None
        (POV_DIR / f"{p['slug']}.html").write_text(
            pov_page(p, prev, nxt, profile), encoding="utf-8"
        )

    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    print(f"index.html + perspectives/index.html + {len(povs)} perspective pages")


if __name__ == "__main__":
    build()
