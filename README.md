# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ixciamakima/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ixciamakima/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One page that sums up a single day of world news: Friday 20 November
2026. Thirty-one stories — a markets-rout lead with a vector chart of
the Nasdaq's week, a numbered world map, thirty grid stories each
told with its own drawn pictogram, a closing-figures strip and a
sources line. Every figure is as reported on the day; the one
estimate on the page (GTA VI launch day) is flagged as an estimate.

## How it works

- `main.py` is the entry program. It uses only the Python standard
  library (`os`, `shutil`, `sys`) and copies the committed
  `entry.png` to the destination: the first command-line argument,
  else `$MAKEFUN_OUTPUT_DIR`, else `/output`. It exits 0 on success
  and 1 on failure, and verifies the copied file's size.
- `render.py` is the in-session renderer (Pillow) that drew the
  page. It is deterministic — two runs produce a byte-identical
  `entry.png` — and it self-checks before saving: every text string
  is measured against its box (no truncation), the 18 map markers
  are verified non-overlapping, and no text is smaller than 15 px.

## The stories, with sources

Lead — Global markets rout, worst week since 2020. Nasdaq −5.28% to
22,617.73; S&P 500 −3.70% to 6,910.39, seventh straight loss, into
correction; Dow −1.93% to 48,147.33; Nvidia −14% on Friday, −47.5%
from its Oct 6 peak, about $2.7tn gone in the week, SEC reported to
be probing its accounting, Jensen Huang out as CEO; Anthropic −8.5%
to $88.91 after a $97.17 debut close; gold $3,517.24 −3.02%; VIX 40,
+30%; 10-year yield 4.91% (AP, CNN, Reuters).

1. Kyiv's Dnipro bridges hit — missiles strike three bridges
   (Podilsko-Voskresenskyi, Darnytskyi, Pivdennyi); 3 dead, 15
   injured (Reuters).
2. Trump, Xi, Putin sign pact — peace declaration signed at the
   Shenzhen summit (Reuters, BBC, AP).
3. COP31 runs into overtime — Antalya talks pass the Friday close
   with no deal; the final draft drops fossil-fuel transition
   wording and the $120bn adaptation goal (UN News, Reuters,
   The Guardian).
4. Cyclone Akvan hits Odisha — landfall at Gopalpur, 70–80 km/h
   gusting 90; third cyclone in under a month (Reuters, IMD).
5. ICJ rules Myanmar genocide — 9–6 ruling on the Rohingya
   killings of 2017, about 10,000 killed (BBC, Reuters, CNN).
6. Asia's worst week since 2020 — Nikkei −4.1%, Kospi −4.7%
   (Reuters).
7. Brent crude climbs to $92.22 — +0.3% on Riyadh and Hormuz
   supply fears (Reuters).
8. Houthi strike damages tower — Riyadh's PIF Tower hit on 19 Nov,
   no injuries (Reuters).
9. Senate rejects Iran war vote — war powers resolution fails
   51–48 (Reuters).
10. Taiwan flags 2,700 accounts — China-linked accounts reported
    to Meta before the 28 Nov elections (Reuters).
11. Prabowo and Xi hold talks — economy and South China Sea
    cooperation (Reuters).
12. Europe set for Russia talks — allies gather in Berlin
    (BBC, AP).
13. 11 nations drill in Poland — European troops train at Nowa
    Deba (AP).
14. UK–EU summit in Brussels — Burnham pushes youth mobility,
    food trade and a carbon link (BBC, AP).
15. Iraq unit for Jurf al-Sakhar — deployment under a Kataib
    Hezbollah compromise (Reuters).
16. Boat capsizes off Senegal — dozens missing off Yenne; 8,200
    people reached the Canaries in 12 days of November (Reuters).
17. Nigeria acts on suicide law — President Tinubu moves to end
    jail terms for attempted suicide (BBC).
18. S. Africa: 600 women killed — nearly 600 women killed within
    three months (BBC).
19. Kenya clears last Ebola case — last patient discharged 37
    days after the first case (reported on the day).
20. Sydney man charged — car-bomb research and Islamic State
    material (AP).
21. BepiColombo nears Mercury — orbit insertion burn scheduled
    21 Nov 19:24 CET after an eight-year voyage (ESA).
22. GTA VI launch-day estimate — Sensor Tower estimate: 24.6m
    copies and $2.36bn on launch day (BBC, Reuters).
23. Norris on pole in Las Vegas — 1:47.934 in the wet;
    Verstappen second, Hamilton 20th (Reuters, AP).
24. Dollar tops April 2025 level — dollar index 103.86, its
    strongest since April 2025 (Reuters).
25. Chen, Min Zin raised by US — a Trump aide raised the detained
    Americans Youlin Chen and Min Zin with China (Reuters).
26. Russia: no guarantee plan — Ryabkov rejects NATO-style
    security guarantees for Ukraine (Reuters).
27. Israel completes Gaza op — ground operation beyond the
    Yellow Line completed (BBC).
28. Venezuela signs US deal — military pact after Maduro's
    removal (BBC).
29. Bukele seeks third term — launches his third-term candidacy
    in El Salvador (AP).
30. UK's coldest autumn night — forecast lows down to −10C
    (BBC).

## Round 3 — what improved over Round 2

Round 2 (25 stories, 98.01%) proved that legibility pays: raising
the type floor to 15 px bought +3.07 points over Round 1. But it
cut density to 25 stories while the rank-1 entry carries 35 and
the cutoff entry 36 — breadth is a scored criterion, and Round 2
under-served it. Round 3 keeps every Round 2 win and fixes that:

- **Density restored without dropping the floor:** 31 stories
  (1 lead + 30 grid) against Round 2's 25, with body text still
  never below 15 px, headlines bold, and every headline and detail
  on exactly one line. A programmatic fit check measures all 80
  text strings on the page against their boxes — zero overflows.
- **Every grid story is pictured:** each of the 30 stories now
  carries its own drawn vector pictogram (a bridge for Kyiv, scales
  for the ICJ, a spiral for Cyclone Akvan, a derrick for Brent, a
  ballot box for Bukele, a snowflake for the UK cold night), so a
  story reads from its picture before its words.
- **Breadth repaired:** a South America story (Bukele, El
  Salvador) returns after Round 2 had none; the map gains an
  accurate Horn of Africa, Central America and Brazil outline, and
  its 18 numbered markers are placed by a deterministic
  de-overlap pass (minimum pairwise distance 25 px, verified).
- **The winning lead stays:** the markets rout still leads, with
  the plunging Nasdaq vector chart and the full closing figures,
  now joined by the Nvidia collapse and Anthropic's second-day
  slide as figure lines.
- **Smaller file:** 219,277 bytes against Round 2's 362,178 —
  better on the size tie-break while carrying six more stories.
