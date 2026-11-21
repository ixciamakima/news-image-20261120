# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ixciamakima/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ixciamakima/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up a whole day of world news: a 1024 x 1024
front page for **Friday 20 November 2026**, drawn programmatically
with Python and PIL. It carries a bold masthead and the date in
large red type, one giant lead story, a vector chart of the day's
market rout, an equirectangular world map with numbered markers, a
grid of the remaining stories, a region legend and a markets strip
with closing figures — 25 verified stories in total.

## Round 2 — what changed vs v1

v1 was submitted on 20 November at 19:10 WIB and scored 94.95%,
rank #7,413 — far outside the paid zone (cutoff 98.87%, rank 1
99.21%). It was built while the day was still unfolding, with 38
stories set in 13px type. v2 rebuilds the page from scratch
around three fixes:

- **The day, completed.** v2 is built on 21 November, after the
  full 20 November news cycle: the Wall Street close (Nasdaq
  -5.28%, S&P 500 into correction), the COP31 talks running past
  their deadline, the Las Vegas qualifying result and the
  BepiColombo orbit-insertion commands.
- **Fewer stories, each deeper and legible.** 25 stories instead
  of 38: one giant lead plus 24 in the grid. The smallest text is
  now 15px (grid details) instead of 13px, headlines are 16px
  bold, and every headline and detail fits on one line with no
  truncation — checked programmatically and by eye, including at
  300px wide.
- **A lead story with a chart.** The lead is the market rout that
  closed the day — Nasdaq wiping out its 2026 gains, Nvidia down
  14%, Anthropic giving back 8.5% a day after its record IPO —
  with a vector-drawn plunging Nasdaq chart beside it, instead of
  a second text block.

## How it is built

- `render.py` — the PIL renderer. It draws the page from scratch
  with DejaVu fonts and saves `entry.png` (1024 x 1024). The
  world map uses hand-drawn simplified continent outlines in an
  equirectangular projection; markers are nudged so no two
  overlap. Output is deterministic: two runs give the same file.
- `entry.png` — the finished front page shipped with the entry.
- `main.py` — the delivery program. It uses only the Python
  standard library and copies `entry.png` to the output location:
  the `MAKEFUN_OUTPUT_DIR` directory when that variable is set,
  otherwise `/output/entry.png`. It never writes into the repo.

## The stories, with sources

Lead story — **Wall Street rout wipes out Nasdaq's 2026 gains**:
the S&P 500 fell 3.7% to 6,910.39, its seventh straight loss,
entering correction; the Dow dropped 949 points to 48,147.33;
the VIX fear gauge spiked 30% to 40. Source: AP; Investopedia;
Motley Fool, 20 Nov 2026.

1. **Kyiv bridges hit by ballistic missiles** — Russian missiles
   hit three Dnipro bridges (Podilsko-Voskresenskyi, Darnytskyi,
   Pivdennyi); Mayor Klitschko said 3 killed and 15 injured.
   Source: Reuters, 20 Nov 2026; also AP and BBC.
2. **COP31 final day: talks run past deadline** — the scheduled
   Friday close in Antalya passed without agreement; the final
   draft dropped all fossil-fuel language and the $120 billion
   adaptation finance goal. Source: UN News; Reuters; The
   Guardian, 20 Nov 2026.
3. **World Court: Myanmar committed genocide** — the ICJ ruled 9-6
   that Myanmar committed genocide against the Rohingya in
   northern Rakhine in 2017; about 10,000 were violently killed.
   Source: BBC; Reuters; CNN.
4. **Trump, Xi and Putin issue peace declaration** — the first
   three-way summit, in Shenzhen, ended with a joint peace
   declaration and no arms-control deal. Source: Reuters; BBC; AP.
5. **Cyclone Akvan makes landfall at Gopalpur** — the third cyclone
   in under a month crossed the north Andhra Pradesh / south
   Odisha coast at 70-80 km/h, gusting 90; no major damage
   reported at first. Source: Reuters, citing the India
   Meteorological Dept.
6. **Nvidia crashes 14% on SEC probe report** — worst day in
   almost two years; down 22.9% on the week and 47.5% from its
   October peak, with $2.7 trillion of value gone since then.
   Source: CNN; Investors' Business Daily; The Times, 20 Nov 2026.
7. **Anthropic slides 8.5% after record IPO** — shares closed at
   $88.91, near the $83 offer price, a day after debuting at
   $97.17. Source: CNN; Finnhub market data, 20 Nov 2026.
8. **Norris takes pole in wet Las Vegas qualifying** — Lando
   Norris beat Max Verstappen by 0.323 seconds (1:47.934);
   Piastri fifth, Hamilton last. Source: Reuters; AP, 20 Nov 2026.
9. **BepiColombo set for Mercury orbit insertion** — ESA and JAXA
   sent the commands for the 21 November 19:24 CET burn, ending
   an eight-year voyage. Source: ESA; New Scientist, 20 Nov 2026.
10. **Houthi strike damages Riyadh PIF Tower** — Riyadh's tallest
    skyscraper, home to the Saudi Public Investment Fund, was
    struck on 19 Nov; no injuries reported. Source: Reuters.
11. **Senate rejects Iran war powers move 51-48** — Senate
    Republicans blocked a resolution to end the Iran war or
    require congressional approval. Source: Reuters.
12. **Prabowo and Xi discuss South China Sea** — Indonesia's
    president and China's president discussed economic partnership
    and South China Sea cooperation. Source: Reuters.
13. **Taiwan flags 2,700 China-linked accounts** — Taipei told
    Meta nearly 2,700 accounts seek to influence the 28 November
    local elections. Source: Reuters.
14. **Russia rejects NATO-style guarantees** — Deputy Foreign
    Minister Ryabkov pushed back on NATO-style security guarantees
    for Ukraine. Source: Reuters.
15. **Europe ready to talk to Russia, leaders say** — Ukraine's
    allies meeting in Berlin said Europe is ready for talks with
    Russia on ending the war. Source: BBC; AP.
16. **UK-EU summit: youth mobility deal nears** — Prime Minister
    Burnham went to Brussels for deals on youth mobility, food
    trade and linked carbon emissions schemes. Source: BBC; AP.
17. **Iraq forces to deploy in militia stronghold** — security
    forces will deploy in Jurf al-Sakhar under a compromise deal
    with Kataib Hezbollah. Source: Reuters.
18. **Dozens missing as boat capsizes off Senegal** — a migrant
    boat bound for Europe capsized off Yenne; the UN refugee
    agency said nearly 8,200 migrants reached the Canary Islands
    in the first 12 days of November. Source: Reuters.
19. **Nigeria moves to end jail for suicide bid** — President
    Tinubu backed reform to end jail terms for attempted suicide,
    after years of calls from psychiatrists. Source: BBC.
20. **Nearly 600 women killed in South Africa** — nearly 600 women
    were killed in South Africa within three months.
    Source: BBC.
21. **Kenya discharges its last Ebola patient** — the last patient
    was discharged 37 days after the first case. Source: One Turn
    daily digest of wire reporting, 20 Nov 2026.
22. **Bukele launches bid for a third term** — El Salvador's
    president launched his candidacy for a third term while
    campaigning on gang crackdowns at home and in Haiti.
    Source: AP.
23. **Sydney man charged over car bomb plot** — Australian police
    arrested a man in greater Sydney accused of researching how to
    build a car bomb and downloading Islamic State material.
    Source: AP.
24. **GTA VI smashes launch-day sales records** — Sensor Tower
    estimates 24.6 million copies and $2.36 billion by the end of
    launch day, 19 November; Take-Two has not released official
    figures. Source: BBC; Reuters.

Stories dropped from v1 (38 → 25): the Myanmar response to the
ICJ ruling (folded into story 3), the UK cold snap, the
Indonesia daycare case, the Mount Fuji warning, the Gaza ground
operation and the Venezuela-US military deal — cut for space so
the remaining stories could be set larger, not because they were
unverified.

## Markets strip (closing figures, Friday 20 November)

S&P 500 6,910.39 (-3.70 percent) · Nasdaq 22,617.73 (-5.28
percent) · Dow 48,147.33 (-1.93 percent) · Gold $3,517.24 an
ounce (-3.02 percent) · 10-year Treasury yield 4.91 percent.
Source: AP; Motley Fool; Investopedia, 20 November 2026.
Brent crude $92.22 (+0.3 percent) is the Friday morning figure
from Reuters; the close is not carried on the page.

## Notes on accuracy

- Where outlets differed, the page follows Reuters: for the Kyiv
  strikes Reuters reported 3 killed and 15 injured via the mayor,
  while a BBC headline summary said five killed.
- The GTA VI sales figure is a Sensor Tower estimate, labelled as
  such, not an official Take-Two number.
- The Anthropic close is $88.91 per CNN and Finnhub; one outlet
  reported $88.30. The page follows the $88.91 figure.
- COP31 had not adopted a final cover decision when this page was
  built: talks ran past the scheduled close, so the page reports
  the draft and the overtime, not a concluded deal.
- BepiColombo's orbit insertion was scheduled for 21 November
  19:24 CET; the page reports the commands sent on 20 November
  and the scheduled burn, not a completed insertion.

## Licence

MIT — see the LICENSE file in this repository.
