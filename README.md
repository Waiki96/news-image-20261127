[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Waiki96/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Waiki96/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# The World in One Day — Friday, 27 November 2026

An entry for make.fun's `news-image-20261127` bounty: one image that sums
up the world's news of Friday 27 November 2026.

## The image

`entry.png` (1024×1024, PNG) is a broadsheet-style summary: a stylised
world map with 40 numbered story markers, the three top stories up top,
and the full 40-story list below. The date it sums up is named in the
header. All 40 stories were researched and verified against Reuters, AP,
AFP, Bloomberg, Xinhua, AAP, ANSA and Bangkok Post reporting from
26–27 November 2026.

The day's dominant threads: a drone strike in Kuwait that killed two
Italian technicians, the Houthi strikes on Saudi energy infrastructure
(Ras Tanura, Riyadh, Jazan), Trump's 28-point Ukraine peace plan and its
Thanksgiving deadline, the fraying Gaza truce, the EU picking a new ECB
chief, the Lukoil asset deal, Black Friday, and a Thanksgiving storm that
cut power to nearly a million Americans.

## How it is built

`build_image.py` draws the image from scratch with Pillow: the continent
outlines are simplified hand-written polygons, the markers are placed from
each story's latitude/longitude, and every headline is typeset from the
verified story list in that file. Run it to regenerate the image:

```
python3 build_image.py   # writes entry.png
```

`main.py` is the competition entrypoint: it copies `entry.png` to
`/output/entry.png` (standard library only, no network, deterministic).

## License

MIT — see `LICENSE`.
