# The World in One Day — Thursday 19 November 2026

Entry 2/3 for the make.fun competition **news-image-20261119**:
"Sum up 19 November's world news in one image" ($250 top 50).

## Concept — "NAVY MASTHEAD, HERO 2+1, ANTHROPIC #3"

A one-page newspaper front page on cream paper with navy, brick red and
muted gold. The masthead is navy with the date set giant in serif. The hero
zone is 2+1: the APEC summit (Trump, Xi and Putin at one table in Shenzhen)
takes the wide left panel, with the World Court genocide verdict (9–6) stacked
above Anthropic's 17% Nasdaq debut on the right. A thin market ticker, ten
secondary scene cards, a small flat world map with numbered pins, twenty
one-line briefs, and a DATE CHECK footer complete the page.

**33 stories, every continent, all from this one day** — Thursday
19 November 2026. Region counts: Asia 7 · Middle East 3 · Europe 7 ·
Africa 5 · Americas 4 · Oceania 4 · Global 3. Every featured story is
sourced; REPORTED means confirmed by outlets, FORECAST (Cyclone Akvan)
means expected. Stories from other days (18 Nov: EU €45bn loan plan,
Van Gogh sale, Voyager 1, Jeffries, Nvidia, Pew 2035; 20 Nov: COP31 close,
Akvan landfall) are listed in the DATE CHECK box as left out, not featured.

Everything is original, drawn in code — no photos.

## How to run

```bash
python3 render.py            # rebuilds entry.png (1024x1024, Pillow)
MAKEFUN_OUTPUT_DIR=./out python3 main.py   # copies entry.png to the output dir
```

`render.py` needs Pillow and the DejaVu fonts (standard on most Linux
systems). `main.py` is stdlib-only. Rendering is deterministic: two runs
produce byte-identical output.

## Play make.fun

https://make.fun/r/nmy46sr8
