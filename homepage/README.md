# Prolifics website builds

Two static home page builds for the new Prolifics site, plus the website decisions deck. Start with CLAUDE.md:
decisions, house rules, layout, build and deploy commands. The project is self-contained: all paths are
relative to this folder.

- Version 1 (48 year hero): https://prolifics-home-preview.vercel.app, built by `python3 src/build_home.py` into `dist/`
- Version 2 (Kyndryl pattern, Satya Bolli hero): https://prolifics-home-v2.vercel.app, built by `python3 src/build_k.py` into `dist-k/`
- Decisions deck: `python3 deck/build_deck.py` writes `deck/out/Prolifics Website and GCC Conclave - Decisions.pdf`

Content lives in `src/content.py`. Photos are in `src/img2` (sources in `src/img2-sources.json`), leadership photos
in `src/people`, partner logos in `src/partners`, Prolifics and client logos in `src/brand`.
Both builders convert photos to WebP and ship only what each page uses.

Requirements: Python 3.9+, Pillow; Google Chrome for the deck PDF; Vercel CLI to deploy.
