# ravikrali/resume

Personal CV site for **Ravi Kiran Rali** — Enterprise AI Architect · Director, AI & Data Management · Enterprise Data Architect.

Static HTML/CSS/JS. No frameworks, no npm, no CI. GitHub Pages can serve the repo root as-is.

---

## What's on the site

| Section | Where |
| --- | --- |
| Summary, value proposition, headline metrics | `index.html#value` |
| Career **roadmap** — 10 milestones, click any one to expand | `index.html#roadmap` |
| Skills — technical depth and people/management, side by side | `index.html#skills` |
| 12 **point-of-view** pages answering common job requirements | `perspectives/` |
| Credentials | `index.html#credentials` |
| **Writing** — recent LinkedIn articles and posts, each with a short description | `index.html#writing` |
| Contact | `index.html#contact` |

## Editing the content

All copy lives in `content/*.json`. Nothing is hard-coded in the HTML.

| File | Controls |
| --- | --- |
| `content/profile.json` | Name, titles, tagline, summary, metrics strip, four value cards, credentials, contact |
| `content/roadmap.json` | Roadmap milestones — role, org, dates, context, outcomes, leadership note, tech stack, links |
| `content/skills.json` | The two skill pillars and their groups |
| `content/perspectives.json` | The 12 perspective pages |
| `content/writing.json` | LinkedIn articles and posts listed in the Writing section |

Then regenerate:

```bash
python build.py
```

That rewrites `index.html`, `perspectives/index.html` and the 12 perspective pages. Python 3.9+, standard library only — nothing to install.

### Adding a roadmap milestone

Append an object to `content/roadmap.json`. Items render newest-first, so put new roles at the top. Required keys: `id`, `years`, `yearShort`, `role`, `org`, `location`, `era`, `headline`, `context`, `outcomes`, `leadership`, `stack`, `links`.

An outcome with a `metric` renders the number large in accent red; one without renders as a plain bullet. Keep three or four metric outcomes per role at most — they lose force in a crowd.

`era` groups milestones under a divider, and `yearShort` positions the dot on the timeline ribbon.

### Adding a LinkedIn article or post

Add an object to the **top** of `content/writing.json` (newest first) and rebuild:

```json
{
  "kind": "Article",
  "date": "Sep 2026",
  "dateFull": "3 September 2026",
  "title": "Post title as published",
  "description": "Two or three sentences on what the piece argues.",
  "url": "https://www.linkedin.com/pulse/...",
  "source": { "label": "Full note", "url": "https://ravikrali.github.io/..." }
}
```

`kind` is a free-text label rendered as a small tag, so `Article`, `Post`, `Dashboard`, or `Talk` all work. `source` is optional and points at the longer write-up behind the item; omit the key entirely if there isn't one. `linkLabel` is also optional and overrides the default "Read on LinkedIn" on the primary link, which is how the StratHub360 entry reads "Open StratHub360".

### Adding a perspective

Append to `content/perspectives.json` and rebuild. The slug becomes the filename, and previous/next paging is derived from array order.

## Design

| Token | Value | Use |
| --- | --- | --- |
| `--paper` | `#e4eaf3` | Page background, light bluish grey |
| `--navy` | `#0d2340` | Foreground text, dark navy |
| `--flame` | `#d62606` | Buttons, actions, metrics, accents |

Typography is Fraunces (display), Archivo (body) and IBM Plex Mono (metadata), loaded from Google Fonts. Everything else is in `assets/css/site.css`, organised in numbered sections.

`assets/js/site.js` has no dependencies and handles four things: the sticky masthead, scroll reveals, the roadmap accordion, and the footer year. Without JavaScript the roadmap panels render open, so no content is ever unreachable.

The site prints cleanly — `Ctrl/Cmd + P` on the home page gives a readable document with every roadmap panel expanded.

## Publishing

Live at **<https://ravikrali.github.io/resume/>**.

GitHub Pages is configured to deploy from the `main` branch, root folder. Every push to `main` republishes within a minute or so — there is no workflow to maintain. `.nojekyll` is committed so GitHub serves the files directly instead of running them through Jekyll.

Deploying a content change is therefore:

```bash
python build.py
git add -A && git commit -m "Update copy" && git push
```

### Custom domain

Add a `CNAME` file at the repo root containing the bare domain, point a `CNAME` DNS record at `ravikrali.github.io`, then set the domain under *Settings → Pages*.

## Local preview

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>.
