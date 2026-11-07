# 小三英文拼字 · p3english

Cute, colourful **Primary 3 English spelling game** for Hong Kong kids — mobile & iPad friendly.

**Live:** https://p3english.chanplanet.workers.dev/

## Features

- **每日 10 個字** — same words for everyone on the same Hong Kong calendar day (`Asia/Hong_Kong`)
- Each word hides **2–5 letters**; fill the blanks with an on-screen keyboard
- **繁體中文（香港）** gloss for every item
- Illustrations from **Wikimedia Commons / Openverse** (CC-friendly), shown via same-origin `/api/img` proxy
- **Shareable PNG result card**
- Progress saved in `localStorage` for the same day
- **8 hearts**
- **Edge TTS** — word + example audio pre-generated with Microsoft `edge-tts` (`en-GB-SoniaNeural`), shipped as static MP3s under `/audio/w/` and `/audio/e/` (no Cloudflare Workers AI at runtime)

## Vocabulary source (EDB honesty)

Hong Kong’s Education Bureau does **not** publish a separate Primary 3–only English wordlist. Official indicative targets are about **1,000 words by end of KS1** and **2,000 by end of primary (KS2)**. The interactive Wordlists package (*Enhancing English Vocabulary Learning and Teaching at Primary Level*) is thematic/alphabetical and not a stable machine-readable download. The 2025 Primary English Language Curriculum Guide advises introducing vocabulary **in context**, not via rote grade lists.

This app uses a **curated P3-appropriate pool** (~500 spelling words, length mostly 4–10 letters) as a **KS1 upper / early KS2 bridge** — harder than P2, easier than P4–P5 — aligned with EDB primary themes (animals, food, school, body, clothes, weather, nature, transport, places, home, jobs, sports, imageable verbs). Prefer imageable items. **Not an official EDB dump**.

References:

- [EDB primary vocabulary resources](https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/resource%20pri_vocab.html)
- [Enhancing English Vocabulary Learning and Teaching at Primary Level](https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/Enhancing%20Eng%20Vocab%20at%20Pri%20Level.html)
- [Wordlists preamble](https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/Wordlists_preamble.html)
- [Primary English Language Curriculum Guide (2025)](https://www.edb.gov.hk/attachment/en/curriculum-development/kla/eng-edu/Curriculum%20Document/Pri_ELCG_Primary_1-6_2025.pdf)

## Develop

```bash
npm install
python3 scripts/build_words.py
python3 scripts/add_examples.py
python3 scripts/enrich_images.py
python3 -m venv .venv && .venv/bin/pip install edge-tts
.venv/bin/python scripts/generate_static_tts.py
npm run dev
```

## Deploy (Cloudflare Workers)

```bash
npm run build
npx wrangler deploy
```

- Worker name: **`p3english`**
- Expected URL: **https://p3english.chanplanet.workers.dev/**
- Daily seed key: `p3english-daily-YYYY-MM-DD`
