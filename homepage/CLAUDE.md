# Prolifics website: two home page builds and the website decisions deck

Handoff for any Claude session that picks this up. Read this file first, then README.md.
Last updated 22 November 2026 by the session that built it (Mac Gangumalla's Claude Code).

## What this is

Static HTML builds of a new home page for Prolifics (prolifics.ai today, founded 1978 as JYACC in New York).
Menu items and inner page paths are copied from the reference site https://prolifics-website.vercel.app.

| Build | Preview (noindex) | Builder | Output |
|---|---|---|---|
| Version 1: 48 year hero, editorial | https://prolifics-home-preview.vercel.app | `src/build_home.py` | `dist/` |
| Version 2: Kyndryl pattern, Satya Bolli hero | https://prolifics-home-v2.vercel.app | `src/build_k.py` | `dist-k/` |
| Website decisions deck (5 pages, PDF) | n/a | `deck/build_deck.py` | `deck/out/` |

Both previews redirect inner pages (/services/..., /solutions/..., /about, /contact) to the reference site through
`vercel.json`, so links work on the preview. On the real site the relative paths resolve to the real pages.

## People

- Mac Gangumalla builds this and works through Mani Kona (fractional practice leader). No Lemniscate branding.
- Satya Bolli: Chairman and Managing Director. Chetan: sales head (surname not confirmed, write "Chetan").

## Decisions Mac made (do not reopen)

1. Design: not "Claude default". No navy or blue tint on photos, no generic card grids. Full color photography.
   "Abstract" means realistic, metaphorical photos (pottery, chess, watchmaking, looms, balancing stones),
   never 3D renders or fantasy images.
2. Version 1 hero: the big photo-filled 48 stays, but do not over-emphasize years. No year counters, no giant years.
   The timeline labels are themes (Founded, Dev tools, Integration, Data, Quality, Salesforce, SAP, AI).
3. Client logos: two scrolling rows, evenly spaced and optically sized (`src/logoutil.py`). No "Source:" lines on stats.
4. Case studies on version 1: three featured image cards (Sarvam voice-agents pattern: hovered card widens),
   then six text cards (logo, stat, short detail, "Read the case study"). No images on the six.
5. Version 2: rolling banners (five), real partner logos, Satya's official portrait.
6. Both builds are responsive and checked at 375, 768, 1024, 1440, 1920, 2560 and 3840 px.
7. IBM and SAP credentials (21 Nov 2026, replacing the 20 Nov "stands apart" section): Mac asked not to highlight
   it much. Both home pages carry a quiet "Recognized by IBM and SAP" strip (version 1 after the stats band,
   version 2 after "Who we are"): certifications and accolades only, no big headline, photos, stats or approach
   steps. IBM: Platinum Business Partner, IBM Partner Plus, original watsonx beta partner, 2025 Sustainability
   Award, 2019 Beacon Award (version 1 only; version 2 leaves the awards to its Industry recognition section). SAP:
   Gold Partner through Castaliaz, Center of Excellence, RISE and GROW with SAP.
   Source of every claim: the docstring in `src/standing.py`.
8. Website direction (deck): move off WordPress to this static build; prolifics.com becomes the primary domain
   again (registered 1996), prolifics.ai stays as the AI brand with page-by-page 301s; prolifics.si is taken.
   GCC Conclave in the second or third week of December 2026, 10 to 15 GCC leaders, Satya speaking.
9. Version 1 is approved (22 Nov 2026). Mac felt the black hero took the charm out of it, so `src/palette.css`
   (loaded last) moves the hero to a light warm white ground with the full color 48, keeps the header white,
   and uses the Prolifics navy family (#00184A, #002463) for every dark surface instead of near black.
10. Inner pages for approval before the full revamp (22 Nov 2026), consulting style (KPMG, Bain, BCG): white
   ground, left-hand section titles, breadcrumbs and a sticky in-page nav on every page, navy feature bands.
   Built: /services, /services/salesforce (practice template), /services/agentforce (service detail template
   with sidebar), /industries, /industries/healthcare (industry template). Copy is the reference site's,
   enhanced only with sourced material from content.py (case studies, group firms, engagement models).
   Case study metrics too small to lead a card (WEAK in build_pages.py) show the story instead.
11. Mac's review of /services/salesforce (22 Nov 2026): it read blank and bland, needed clients, more capability depth,
   industries served, and the industry on every case study. Version 2 adds the client logo grid, a sourced "why now"
   band, "what agents change", a nine-service tab explorer, six industry tiles with proof, six named prolifics.ai
   Salesforce stories with industry tags, and a client quote. Data in `src/sf_data.json` (from the GTM microsite).
   Industry photos must be full color: the GTM brochure crops are navy-toned, do not use them.
13. Full site built (22 Nov 2026, Mac: "build the rest"): all 109 reference URLs plus the home page, 110 pages, in
   `src/build_site.py`. Copy comes from `src/ref.json` (`src/extract_ref.py` parses ../ref/*.html, downloaded from
   the reference sitemap). Templates: practice (7, Salesforce stays custom), service detail with sidebar (60+),
   solutions landing and 16 solutions, industries (7, Healthcare stays custom), about, leadership, careers,
   locations, social impact, ESG, partnerships, resources with a filterable case study library, 3 guides, contact.
   Proof comes from `src/cases.py` (published case studies only; metrics only where the case study states them;
   ServiceNow has none by rule). Thin reference pages get the standard approach, FAQ, engagement models and
   practice case studies added. The contact form validates but is not connected (HubSpot embed pending).
   The partnerships copy "Platinum-level partnerships" was replaced: never claim partner tiers beyond IBM's.
14. 23 Nov 2026, Mac: Solutions removed from the site immediately: no nav item, mega menu, home section, footer column,
   related-solution links or /solutions pages. dist/vercel.json redirects /solutions and /solutions/* to /services.
   The SOLUTIONS data stays in content.py, unused.
15. Group company pages (23 Nov 2026): /group plus /group/enable-consulting, /castaliaz, /prolifics-testing,
   /tier-2-consulting, built from each firm's live site (GROUP_PAGES in pages_content.py, sources per claim).
   Partner tiers and certification counts stay out even where a firm's own site states them. Group logos
   (src/brand/group) replace icons wherever the group is listed. Tier 2 Consulting added to GROUP.
16. Client wall by industry (23 Nov 2026): WALL in content.py, Featured plus five industries, up to 11 logos and a
   150+ tile, with a starred note that clientele spans Prolifics and its group companies. "group/..." logos are
   clients published on prolifics-testing.com (src/brand/clients/group/sources.json).
17. Source and builds go to Google Drive from 23 Nov 2026 (Drive replaces GitHub; the GitHub repo is an archive):
   My Drive/Client Decks 2026/Prolifics/Website 2026/Source code (current). Commit locally, do not push.
12. Client logos are a static even grid, not a marquee (Mac, 22 Nov 2026, harvey.ai customer wall as the reference):
   `logo_grid()` in build_home.py with `src/logogrid.css`, 6 columns, 4 at tablet, 3 on phones.

## House rules for everything written

American English. No em or en dashes (builders print a count, it must be 0). No exclamation marks. No pricing.
Every number needs a source (company figures from prolifics.ai; case study metrics from the linked case studies;
deck figures from `deck/research.md`). Real logo files only. Prolifics brand: navy #001F5B, cyan #00AEEF,
Inter Tight and Inter on the web, Arial in decks. Never claim partner tiers, certification counts or a ServiceNow
case study. Satya's quote is from prolifics.ai/leadership; do not invent quotes for other leaders.

## Layout

| Path | What |
|---|---|
| `src/content.py` | All copy and data: menu, practices, solutions, industries, stats, eras, case studies (CASES), partners |
| `src/build_home.py` | Version 1 page builder; also exports header, drawer and footer used by version 2 |
| `src/build_k.py` | Version 2 page builder (hero banners, recognition, stories, people, partners, FAQ) |
| `src/home.css`, `src/home-v4.css` | Version 1 styles (v4 file holds logos, sprint ruler, case studies, responsive pass) |
| `src/k.css`, `src/k-hero.css` | Version 2 styles (k-hero holds the rolling banner, partner logos, responsive pass) |
| `src/home.js`, `src/k.js` | Behavior: mega menus, 48 hero, practice rows, case study cards, banners, counters |
| `src/standing.py`, `src/standing.css` | IBM and SAP credentials strip, shared by both versions |
| `src/palette.css` | Light hero and navy dark surfaces for version 1 and the inner pages (22 Nov 2026) |
| `src/build_pages.py`, `src/pages_content.py` | Inner pages: builder and copy (sources in the docstring) |
| `src/pages.css`, `src/pages.js` | Inner page styles; scroll spy for the sub navigation and sidebar |
| `src/optimize.py` | Ships only the photos a page uses, as WebP sized per use |
| `src/logoutil.py` | Trims PNG logo margins, recolors white-only SVGs, optically balanced logo sizes |
| `src/icons.py` | Prolifics line icon set |
| `src/img2/` | Photography (Unsplash, free license). Source page for every file: `src/img2-sources.json` |
| `src/people/` | Official leadership photos from prolifics.ai/leadership (two files are unnamed: do not label them) |
| `src/partners/` | Partner logos; `sources.json` lists where each came from; `raw/` holds the originals |
| `src/brand/` | Prolifics logos, favicon, client logos (`clients/logos.json` lists sources) |
| `deck/` | Decisions deck builder, research with sources, screenshots, PDF |

## Build

Requirements: Python 3.9+, Pillow, Google Chrome (only for the deck PDF), Vercel CLI for deploys.

```
python3 src/build_home.py      # version 1 into dist/   (add --final to drop the noindex meta tag)
python3 src/build_k.py         # version 2 into dist-k/ (add --final to drop noindex)
python3 deck/build_deck.py     # deck PDF into deck/out/
python3 src/build_site.py      # all inner pages into dist/ (run after build_home.py, which wipes dist/)
python3 src/extract_ref.py     # only when the reference site changes: re-download ../ref/*.html first
```
Each builder prints byte size and the dash and exclamation counts. Both must be 0.

## Deploy and share

```
cd dist && vercel deploy --prod --yes --name prolifics-home-preview
cd dist-k && vercel deploy --prod --yes --name prolifics-home-v2
```
Both carry X-Robots-Tag noindex. Source code lives on GitHub (from 20 Nov 2026): private repo
git@github.com:lemniscate-growth-hq/prolifics-website.git, remote `origin`, push over SSH. Commit and push after
changes. Drive gets packages and decks only (My Drive/Client Decks 2026/Prolifics), not the source.
Do not email Mac about builds.

## Gotchas

- The class name `dt` is used by the mobile drawer. Version 2 banner dots are `kdot`. Do not reuse `dt`.
- Hero portrait and circle on version 2 live in one `.sat-wrap` anchored to the content column. Do not position
  them against the viewport, it breaks on wide screens.
- Headless Chrome screenshots freeze CSS transitions and counters mid-way; check numbers in a real browser.
- Lazy-loaded images do not load in headless iframe captures; blank tiles there are not bugs.

## Open items

- More photos of Satya Bolli (stage, events) would strengthen version 2; prolifics.ai has only one portrait.
- Every page is built; `dist/vercel.json` has no redirects any more, only the noindex header.
- HubSpot forms (22 Nov 2026): 10 forms in the Prolifics portal 8077126 named "Website 2026: <practice>" (AI and Data,
  FDE AI Engineering, Salesforce, ServiceNow, SAP and ERP, Application and Cloud, Business Transformation, Quality
  Engineering, Solutions, General Contact), cloned from "Prolifics new contact form" and restyled for white pages.
  IDs live in FORMS in build_pages.py; build_site.py picks the form per page path. The original form's settings were
  kept: no reCAPTCHA, and "Create new contacts for email addresses" is off (flagged to Mac).
  The Claude HubSpot connector is the Aavenir portal and cannot write forms: edit Prolifics forms in the Chrome
  profile signed in to Prolifics Global (Browser 2).
- HubSpot form embed codes and GA4 for the launch.
- Mobile PageSpeed scores (the public API was rate limited on 19 Nov 2026).
- Conclave date, city and venue. Satya's speaker slot and the run of show are proposals.
- Intealth logo file is the "ECFMG, a Division of Intealth" version.
