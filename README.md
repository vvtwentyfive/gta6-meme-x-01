# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/vvtwentyfive/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/vvtwentyfive/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 WANTED-poster meme for the make.fun bounty: the make.fun ghost is wanted by the Leonida Police Department for stealing 13 years (2013–2026) — 2 delays, 214 GB, $79.99, 5 sick days booked for launch week. The reward was already paid in full by my AI agent on make.fun. The meme is posted on X from a public account; this repository hands in the post's address via POST.json, and `main.ts` copies it to the output directory for the house to read.

The poster is rendered entirely in code (`render-meme.py`, PIL): the ghost is drawn from primitives following the make.fun press-kit description — white ghost, thick black outline, four-point sparkle eyes, small round hands, magenta star coin on a magenta disc — and every line of text is code-rendered, never AI-drawn.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=073t4skd&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
