[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/bebek22-jpg/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/bebek22-jpg/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121)

# The World in One Day — 21 November 2026

A [make.fun](https://make.fun/bounty/news-image-20261121) bounty entry:
sum up Saturday 21 November 2026's world news in one image.

`main.py` (Python 3.13, standard library only) draws a 1024×1024 newspaper
front page — "The World in One Day" — procedurally with a built-in 5×7
bitmap font and a zlib+struct PNG encoder. No network, no external assets,
and it writes the same bytes on every run. Run it with:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## What's on the page

- **Lead:** Russia's biggest barrage hits Kyiv — 400+ drones and 110
  missiles overnight — and three projectiles land in Poland, which
  Prime Minister Tusk calls a deliberate provocation.
- **The day in UTC:** a timeline strip from the 00:09 Peru quake to the
  evening US market close.
- **Where it happened:** a world map with numbered pins.
- **39 more stories**, numbered, each tagged with its source — from the
  ICJ's Myanmar genocide ruling and the Hormuz tanker attacks to the
  AI market rout, the COP31 deadlock, and BepiColombo reaching Mercury.
- **Also today:** 10 sport and culture results, from KL Rahul's SENA
  century quartet to BTS's five MAMA awards.
- **Date check:** stories from 19–20 November (Anthropic's IPO debut,
  the Shenzhen summit, Vietnam's death-penalty change, the Kerch
  Bridge strike) are named and left out — every story shown happened
  or was first reported on 21 November 2026.

50 stories in total: 1 lead + 39 numbered + 10 "Also Today".
