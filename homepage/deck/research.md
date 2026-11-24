# Prolifics website deck: sourced research

Compiled 19 November 2026. Every number below was opened at the linked URL or produced by a command run on 19 November 2026. Anything not confirmed is marked UNVERIFIED.

## A. WordPress security

| Fact | Number | Source | Date |
|---|---|---|---|
| New WordPress ecosystem vulnerabilities disclosed in 2025 | 11,334, up 42% on 2024 | [Patchstack, State of WordPress Security in 2026](https://patchstack.com/whitepaper/state-of-wordpress-security-in-2026/) | Page updated 25 February 2026 |
| Share of 2025 vulnerabilities in plugins / themes / core | 91% plugins, 9% themes, 6 in core (all low priority) | Same Patchstack 2026 report | 25 February 2026 |
| 2025 vulnerabilities with no fix by public disclosure | 46% | Same Patchstack 2026 report | 25 February 2026 |
| Weighted median time to first exploit, heavily targeted vulnerabilities | 5 hours; about half of high-impact vulnerabilities exploited within 24 hours | Same Patchstack 2026 report | 25 February 2026 |
| New WordPress ecosystem vulnerabilities disclosed in 2024 | 7,966 (96% plugins, 4% themes, 7 core) | [Patchstack, State of WordPress Security in 2025](https://patchstack.com/whitepaper/state-of-wordpress-security-in-2025/) | Page updated 14 March 2025 |
| 2024 vulnerabilities exploitable with no login | 43% | Same Patchstack 2025 report | 14 March 2025 |
| 2024 vulnerabilities unfixed at disclosure | 33% | Same Patchstack 2025 report | 14 March 2025 |
| Wordfence count of WordPress vulnerabilities published in 2024 (counts per CVE, so lower than Patchstack) | 8,223, about 68% more than 2023 | [Wordfence 2024 Annual WordPress Security Report (PDF), p. 8](https://www.wordfence.com/wp-content/uploads/2025/04/2024-Annual-WordPress-Security-Report-by-Wordfence.pdf) | April 2025 |
| Share of infected CMS sites that were WordPress (Sucuri remediation data) | 95.5%; 39.1% of CMS installs were outdated at infection | [Sucuri 2023 Hacked Website and Malware Threat Report](https://sucuri.net/reports/2023-hacked-website-report/) | 2023 data, published mid 2024 (no newer Sucuri edition found) |
| WordPress share of all websites / of sites with a known CMS | 38.5% of all websites; 57.4% CMS market share | [W3Techs, WordPress usage](https://w3techs.com/technologies/details/cm-wordpress) | Updated daily, read 19 November 2026 |

Caveat for the slide: Sucuri's share reflects its own cleanup sample and partly reflects WordPress popularity; the report itself says it does not mean other platforms are more secure. Use it with the market share number next to it.

## B. Bot traffic and automated attacks

| Fact | Number | Source | Date |
|---|---|---|---|
| Bad bots as share of all internet traffic, 2025 | 40%; all automated traffic 53%; good bots 13% | [Help Net Security on the Thales 2026 Bad Bot Report](https://www.helpnetsecurity.com/2026/04/30/thales-ai-driven-bot-traffic-rise-report/) | 30 April 2026 |
| Bot attacks aimed at APIs, 2025 | 27% | Same article | 30 April 2026 |
| Bad bots as share of all internet traffic, 2024 | 37% (up from 32% in 2023); bots 51% of all traffic, above human traffic for the first time in a decade | [Thales press release, 2025 Imperva Bad Bot Report](https://cpl.thalesgroup.com/about-us/newsroom/2025-imperva-bad-bot-report-ai-internet-traffic) | 15 April 2025 |
| Password attacks (brute force, credential stuffing) blocked against WordPress sites, 2024 | Over 55 billion, from nearly 136 million attacking IPs | [Wordfence 2024 Annual Report (PDF)](https://www.wordfence.com/wp-content/uploads/2025/04/2024-Annual-WordPress-Security-Report-by-Wordfence.pdf) | April 2025 |
| Same report: other blocked malicious requests, 2024 | Over 54 billion logged; 9 billion XSS and 1.1 billion SQL injection attempts blocked | Same PDF | April 2025 |

Note: the Wordfence report also says password attacks on WordPress declined through 2024 while vulnerability exploitation rose. Do not present login attacks as rising.

UNVERIFIED: Wordfence quarterly figures for 2025 and Q1 2026 (19.2B in Q3 2025, 13.8B in Q4 2025, 16B+ in Q1 2026) appeared in search results, but wordfence.com blocked automated page loads, so I could not open them.

UNVERIFIED: Thales 2026 report primary PDF not opened; figures above come from Help Net Security's coverage.

## C. Static or custom builds

| Fact | Source | Date |
|---|---|---|
| Google's web.dev says static rendering "achieves a consistently fast TTFB" and offers a fast FCP plus lower TBT and INP when client JavaScript is kept small; server rendering on each request can increase TTFB | [web.dev, Rendering on the Web](https://web.dev/articles/rendering-on-the-web) | Updated 5 January 2026 |
| Google recommends server-side permanent redirects (301 or 308) for a domain move, with client-side redirects only "as a last resort" | [Google Search Central, Site moves with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes) | Read 19 November 2026 |

No vendor-neutral source with a measured attack surface reduction figure for static sites was found. State the point qualitatively: a static build has no PHP runtime, no login page, no database and no plugins on the public server.

## D. Domains and current stack (commands run 19 November 2026)

**whois**

| Domain | Created | Registrar | Notes |
|---|---|---|---|
| prolifics.com | 25 July 1996 | Network Solutions, LLC | Expires 24 July 2028. Registrant address 5 Hanover Sq, 20th Fl, New York, NY |
| prolifics.ai | 9 October 2025 | GoDaddy.com, LLC | Expires 9 October 2027. Registrant hidden behind Domains By Proxy |
| prolifics.si | 8 October 2026 | OpusDNS | Registered. Registrant shown only as handle O1632466 (owner not disclosed). Expires 8 October 2027. Nameservers dns-parking.com; serves a "Something remarkable is coming" holding page in English and Slovenian. Owner UNVERIFIED |

So prolifics.com is 30 years old (registered 1996); prolifics.ai is just over 1 year old.

**HTTP behavior (`curl -sIL`)**

- `http://prolifics.com` returns a 301 to `https://prolifics.com/`, which then returns **200**, not a redirect.
- `https://www.prolifics.com` returns **200** with a 10 KB holding page titled "We're now Prolifics.ai" ("Prolifics.com is now Prolifics.ai ... Please update your bookmarks"), canonical set to prolifics.ai, and a third-party JavaScript geo-redirect script. There is no server-side 301 to prolifics.ai.
- Deep links on the old domain return **404** (tested `https://www.prolifics.com/services` and `/blog/anything-old`). Any legacy backlinks to inner prolifics.com pages currently land on a 404.
- Both domains: `server: nginx`, no `x-powered-by` header.

**WordPress signals on prolifics.ai (plain GET/HEAD only)**

- Response header `link: <https://prolifics.ai/wp-json/>; rel="https://api.w.org/"` (WordPress REST API).
- `/wp-json/` 200, `/wp-login.php` 200 (public login page reachable), `/readme.html` 200, `/xmlrpc.php` 403 (blocked), `/wp-includes/js/jquery/jquery.min.js` 200.
- Core asset query strings show WordPress version 7.1.5 publicly.
- Theme: Themify Ultra. Plugins visible in home page HTML: themify-ptb, popup-maker, the-events-calendar, events-grid-plugin, litespeed-cache, builder-button, builder-bg-video-slider (7 or more plugins on the home page alone).
- No generator meta tag.

## E. Home page performance

**PageSpeed Insights API: not available.** Both calls (prolifics.ai and prolifics-home-preview.vercel.app) and one retry returned HTTP 429 "Quota exceeded ... Queries per day" with a quota limit of 0 for unauthenticated calls. Performance score, LCP, TBT and CLS are UNVERIFIED. To fill these in, run PageSpeed Insights at pagespeed.web.dev by hand or call the API with a key.

**HTML document (`curl -w "%{size_download} %{time_total}"`)**

| Page | HTML transferred (compressed) | HTML uncompressed | Total time |
|---|---|---|---|
| prolifics.ai/ | 42,263 bytes | 191,658 bytes | 1.21 s |
| prolifics-home-preview.vercel.app/ | 27,840 bytes | 137,595 bytes | 0.10 s |

**Full page load (resources the browser requested, each re-fetched with curl using a Chrome user agent; desktop, not a Lighthouse run)**

| Page | Requests | Total transferred | JavaScript | Images | Script tags | Hosts contacted |
|---|---|---|---|---|---|---|
| prolifics.ai/ | 47 (plus tracking beacons) | about 2.1 MB | about 990 KB | about 840 KB | 44 | 20 |
| prolifics-home-preview.vercel.app/ | 29 | about 5.1 MB | 0 KB external | about 5.1 MB | 3 | 2 |

Findings to handle before using these on a slide:
- The preview ships far less JavaScript (no jQuery, no Google tag stack, no HubSpot embeds), but its images are heavier: 28 JPEGs, the largest 637 KB (e2015.jpg) and 541 KB (e1978.jpg). Many are CSS backgrounds that loaded on first view. Convert to WebP or AVIF and resize before claiming a page weight win.
- prolifics.ai serves a 720 KB uncompressed SVG (our-partnership.svg) and three Google tag scripts (two gtag IDs plus GTM) at about 170 to 200 KB each.

## F. GCCs in India

| Fact | Number | Source | Date |
|---|---|---|---|
| GCCs in India, FY26 | 2,117 GCCs across 3,728 units, about 2.36 million employees, $98.4 billion market revenue | [Nasscom and Zinnov press release, "GCC Value Orbit" (PDF)](https://d3r3sr3o54kk15.cloudfront.net/s3fs-public/media_pdf/GCC%20Report_Press%20Release.pdf) | 6 May 2026 |
| 2030 projection (earlier report, FY24 base of about 1,700 GCCs, 1.9 million people, $64.6 billion) | 2,100 to 2,200 GCCs, 2.5 to 2.8 million people, $99 to $105 billion | [Republic World on the Nasscom and Zinnov 5 year report](https://www.republicworld.com/business/india-s-global-centre-market-to-grow-to-105-billion-by-2030-says-nasscom-zinnov-report) | 11 September 2024 |

The FY26 count (2,117) already sits inside the 2030 range. Business Today calls it the 2030 target hit four years early ([Business Today, 7 May 2026](https://www.businesstoday.in/technology/news/story/the-big-boom-how-indias-gcc-story-hits-2030-target-4-years-early-530265-2026-05-07)). No new 2030 projection appears in the 2026 release.

UNVERIFIED: a NewsBytes headline claiming "3.5 million by 2030" does not match Nasscom's own figures. Do not use it.

## G. "SI" terminology among US buyers

Skipped. No reputable source on a rising trend was found. Google Trends would need to be checked by hand.
