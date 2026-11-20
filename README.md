# The World in One Day — Friday 20 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty%20news--image--20261120-red)](https://make.fun/bounty/news-image-20261120)
[![entry](https://img.shields.io/badge/entry-The%20World%20in%20One%20Day-blue)](https://make.fun/bounty/news-image-20261120)
[![date](https://img.shields.io/badge/date-Friday%2020%20November%202026-green)](https://make.fun/bounty/news-image-20261120)

One image that sums up a whole day of world news: a 1024 x 1024
front page for **Friday 20 November 2026**, drawn programmatically
with Python and PIL. It carries a bold masthead and date, one giant
lead story, an equirectangular world map with numbered markers, a
dense grid of the remaining stories, a region legend and a markets
strip — 38 verified stories in total.

Every story below was checked against reporting by Reuters, BBC,
AP, UN News or Formula 1 published on or about 20 November 2026,
up to about 19:00 Jakarta time. Coverage of the day was still
incomplete at build time; figures are as reported then.

## How it is built

- `render.py` — the PIL renderer. It draws the page from scratch
  with DejaVu fonts and saves `entry.png` (1024 x 1024).
- `entry.png` — the finished front page shipped with the entry.
- `main.py` — the delivery program. It uses only the Python
  standard library and copies `entry.png` to the output location:
  the `MAKEFUN_OUTPUT_DIR` directory when that variable is set,
  otherwise `/output/entry.png`. It never writes into the repo.

## The stories, with sources

1. **Kyiv bridges hit by ballistic missiles** — Russian missiles
   hit three Dnipro bridges (Podilsko-Voskresenskyi, Darnytskyi,
   Pivdennyi); Mayor Klitschko said 3 killed and 15 injured.
   Source: Reuters, 20 Nov 2026; also AP and BBC.
2. **Trump, Xi and Putin issue peace declaration** — the first
   three-way summit, in Shenzhen, ended with a joint peace
   declaration and no arms-control deal. Source: Reuters; BBC; AP.
3. **COP31 final day: deadlock in Antalya** — 21 issues unresolved
   on finance, adaptation, mitigation and just transition as the
   scheduled Friday close arrived. Source: UN News; Reuters.
4. **Cyclone Akvan makes landfall at Gopalpur** — the third cyclone
   in under a month crossed the north Andhra Pradesh / south Odisha
   coast at 70-80 km/h, gusting 90; no major damage reported at
   first. Source: Reuters, citing the India Meteorological Dept.
5. **World Court: Myanmar committed genocide** — the ICJ ruled 9-6
   that Myanmar committed genocide against the Rohingya in northern
   Rakhine in 2017; about 10,000 were violently killed.
   Source: BBC; Reuters; CNN; Le Monde.
6. **Myanmar calls genocide ruling unfair** — a government
   spokesperson said the ruling was not unanimous and Myanmar had
   been unjustly accused. Source: Reuters, 20 Nov 2026.
7. **Anthropic IPO: biggest debut in history** — priced at $83 a
   share, raising about $81 billion at a valuation near $1.5
   trillion; shares closed at $97.17, up 17 percent.
   Source: Reuters.
8. **Anthropic slips in post-debut reality check** — shares eased
   to $91.24 on Friday as investors questioned AI valuations.
   Source: Reuters, 20 Nov 2026.
9. **Asian shares face worst week since 2020** — MSCI Asia-Pacific
   fell 2.5 percent on Friday; Nikkei fell 4.1 percent and Kospi
   4.7 percent. Source: Reuters.
10. **US stocks slump about 2 percent again** — the S and P 500
    fell for a fifth straight session to fresh seven-month lows.
    Source: Reuters.
11. **Oil edges up on Riyadh and Hormuz fears** — Brent rose 0.3
    percent to $92.22 a barrel early Friday on supply concerns.
    Source: Reuters.
12. **Gold slides toward a heavy weekly loss** — gold dipped 0.6
    percent to $3,601 an ounce, heading for a 7.3 percent weekly
    loss. Source: Reuters.
13. **Dollar rally reaches strongest since 2025** — the dollar
    index held at 103.86, its strongest since April 2025.
    Source: Reuters.
14. **Houthi strike damages Riyadh PIF Tower** — Riyadh's tallest
    skyscraper, home to the Saudi Public Investment Fund, was
    struck on 19 Nov; no injuries reported. Source: Reuters.
15. **Houthis say they targeted Riyadh airport** — the group said
    it aimed cruise missiles at King Khalid Airport and the
    financial centre. Source: Reuters.
16. **Senate rejects Iran war powers move 51-48** — Senate
    Republicans blocked a resolution to end the Iran war or
    require congressional approval. Source: Reuters.
17. **Trump: aide raised detained Americans** — Trump said an aide
    raised the cases of Youlin Chen and Min Zin, designated
    wrongfully detained, with Chinese officials. Source: Reuters.
18. **Prabowo and Xi discuss South China Sea** — Indonesia's
    president and China's president discussed economic partnership
    and South China Sea cooperation. Source: Reuters.
19. **Taiwan flags 2,700 China-linked accounts** — Taipei told
    Meta nearly 2,700 accounts seek to influence the 28 November
    local elections. Source: Reuters.
20. **Russia rejects NATO-style guarantees** — Deputy Foreign
    Minister Ryabkov pushed back on NATO-style security guarantees
    for Ukraine. Source: Reuters.
21. **Europe ready to talk to Russia, leaders say** — Ukraine's
    allies meeting in Berlin said Europe is ready for talks with
    Russia on ending the war. Source: BBC; AP.
22. **European troops drill in Poland** — thousands of troops from
    11 countries exercised at Nowa Deba for a possible postwar
    Ukraine mission. Source: AP.
23. **UK-EU summit: youth mobility deal nears** — Prime Minister
    Burnham went to Brussels for deals on youth mobility, food
    trade and linked carbon emissions schemes. Source: BBC; AP.
24. **UK faces coldest autumn night, minus 10C** — Friday night
    was forecast to be the coldest of the autumn so far.
    Source: BBC.
25. **Iraq forces to deploy in militia stronghold** — security
    forces will deploy in Jurf al-Sakhar under a compromise deal
    with Kataib Hezbollah. Source: Reuters.
26. **Dozens missing as boat capsizes off Senegal** — a migrant
    boat bound for Europe capsized off Yenne; the UN refugee
    agency said nearly 8,200 migrants reached the Canary Islands
    in the first 12 days of November. Source: Reuters.
27. **Nigeria moves to end jail for suicide bid** — President
    Tinubu backed reform to end jail terms for attempted suicide,
    after years of calls from psychiatrists. Source: BBC.
28. **Nearly 600 women killed in South Africa** — nearly 600 women
    were killed in South Africa within three months.
    Source: BBC.
29. **Kenya discharges its last Ebola patient** — the last patient
    was discharged 37 days after the first case. Source: One Turn
    daily digest of wire reporting, 20 Nov 2026.
30. **Bukele launches bid for a third term** — El Salvador's
    president launched his candidacy for a third term while
    campaigning on gang crackdowns at home and in Haiti.
    Source: AP.
31. **Sydney man charged over car bomb plot** — Australian police
    arrested a man in greater Sydney accused of researching how to
    build a car bomb and downloading Islamic State material.
    Source: AP.
32. **Daycare principal jailed in Indonesia** — an Indonesian
    daycare principal received five years in jail over a child
    abuse case. Source: BBC.
33. **China issues Mount Fuji climb warning** — a $75,000 reward
    offered by the family of missing climber Chen Jie sparked
    fears of reckless climbing attempts. Source: BBC.
34. **BepiColombo nears Mercury after 8 years** — the ESA-JAXA
    probe is due to enter Mercury orbit on 21 November 2026 after
    an eight-year journey; science begins April 2027.
    Source: BBC; ESA.
35. **GTA VI smashes launch-day sales records** — Sensor Tower
    estimates 24.6 million copies and $2.36 billion by the end of
    launch day, 19 November; Take-Two has not released official
    figures. Source: BBC; Reuters.
36. **Russell fastest in wet Las Vegas practice** — George Russell
    topped FP2 in 1:47.272, 0.071 seconds ahead of Gasly, with
    Leclerc third. Source: Formula 1; BBC Sport.
37. **Israeli army ends Gaza ground operation** — the Israeli
    military said it completed a ground operation in Gaza beyond
    the Yellow Line. Source: BBC.
38. **Venezuela signs military deal with US** — Venezuela signed a
    military deal with the United States less than a year after
    Maduro's removal. Source: BBC.

## Markets strip (as reported Friday morning)

Brent $92.22 (+0.3 percent) · WTI $83.40 · Gold $3,601 an ounce
(-0.6 percent) · S and P 500 about -2 percent · Nikkei -4.1
percent · Kospi -4.7 percent · Dollar index 103.86.
Source: Reuters market reporting, 20 November 2026.

## Notes on accuracy

- Where outlets differed, the page follows Reuters: for the Kyiv
  strikes Reuters reported 3 killed and 15 injured via the mayor,
  while a BBC headline summary said five killed.
- The GTA VI sales figure is a Sensor Tower estimate, labelled as
  such, not an official Take-Two number.
- This is a same-day edition built before the day ended, so late
  developments of 20 November are not all reflected here.

## Licence

MIT — see the LICENSE file in this repository.
