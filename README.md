# horoscope-matching

A [Claude Code](https://claude.com/claude-code) skill for Vedic (jyotish) astrology. It can:

- write a short **life horoscope summary** for one person
- run **marriage matching** (Ashtakoota / Guna Milan, scored out of 36) for two people
- check for **Mangal Dosha** (Kuja Dosha)
- list **Vimshottari Dasha** (Mahadasha) periods, including a joint overlay for a couple

Everything runs offline in plain Python 3. There are no dependencies and no ephemeris files.

## What it does

| Output | Needs | How it's produced |
|---|---|---|
| Life summary | Rasi and Nakshatra | Traits from `references/nakshatra_rasi_traits.md` |
| Marriage matching | Rasi and Nakshatra for both people | 8-koota scoring from `references/ashtakoota_matching.md`, with a per-koota table, total and verdict. Nadi and Bhakoot Dosha are called out by name. |
| Mangal Dosha | Birth date, time, UTC offset, latitude and longitude | `scripts/compute_mangal_dosha.py`, plus the rules and mitigating factors in `references/mangal_dosha.md` |
| Dasha periods | Birth date, time and UTC offset | `scripts/compute_vimshottari_dasha.py`, plus `references/dasha_periods.md` |
| Couple's Dasha overlay | Both people's birth details | Both Mahadasha sequences merged into one timeline, with the planetary friendships (Graha Maitri) for each segment |

If you already know someone's Rasi and Nakshatra, for example from a panchang, the skill uses them directly and skips the calculation.

## Repository layout

```
horoscope-matching/
├── SKILL.md                         # Skill definition and workflow (what Claude reads)
├── references/
│   ├── nakshatra_rasi_traits.md     # Traits for 12 Rasis and 27 Nakshatras
│   ├── ashtakoota_matching.md       # Scoring rules for all 8 kootas
│   ├── mangal_dosha.md              # Mangal Dosha rules and mitigations
│   └── dasha_periods.md             # Mahadasha meanings and couple overlay
└── scripts/
    ├── compute_rasi_nakshatra.py    # Birth details -> Rasi, Nakshatra, Pada
    ├── compute_mangal_dosha.py      # Birth details + place -> Lagna, Mars, Dosha
    └── compute_vimshottari_dasha.py # Birth details -> Mahadasha sequence
```

## Installation

Copy or symlink the folder into your Claude Code skills directory:

```bash
git clone https://github.com/arunprab/horoscope-matching.git
ln -s "$(pwd)/horoscope-matching" ~/.claude/skills/horoscope-matching
```

Use the symlink if you want edits in the repo to take effect in the live skill. To use a plain copy instead, run `cp -R horoscope-matching ~/.claude/skills/`.

Claude loads the skill automatically when you mention things like horoscope, kundli, Rasi, Nakshatra, guna milan, mangal dosha or dasha. You can also give it a date and time of birth and ask whether two people are compatible for marriage.

## Example prompts

- "Can you check if my partner's and my birth details are compatible for marriage?"
- "Give me a brief horoscope summary. I was born 15 Aug 1990 at 2:30 pm in India."
- "Does this chart have Mangal Dosha?"
- "What are my Mahadasha periods, and when is a good time period for us as a couple?"

## Using the scripts directly

All times are local birth time. The UTC offset is written like `+5:30`.

```bash
# Moon sign (Rasi), star (Nakshatra) and Pada
python3 scripts/compute_rasi_nakshatra.py 1990-08-15 14:30 +5:30

# Mangal Dosha (adds latitude and longitude: North and East are positive)
python3 scripts/compute_mangal_dosha.py 1979-10-22 13:15 +5:30 13.0827 80.2707

# Vimshottari Dasha sequence (last argument is the number of years to print, default 100)
python3 scripts/compute_vimshottari_dasha.py 1979-10-22 13:15 +5:30 100
```

## Accuracy and limits

- **Rasi and Nakshatra:** an approximation. It uses a truncated lunar series and an approximate Lahiri (Chitrapaksha) ayanamsa. It is accurate to a few arcminutes up to about half a degree, which normally places the Moon in the right sign and star. The script warns when a result is close to a boundary, and in that case you should check it against a precise panchang.
- **Mangal Dosha:** less certain than the Moon calculation. The Ascendant moves about 1° every 4 minutes, and Mars uses a simplified two-body orbit. Treat it as a first pass.
- **Dasha periods:** the arithmetic is exact once the Moon position is known. What each period means for a person is general traditional description, not a personalised prediction.
- **Couple's Dasha overlay:** there is no fixed classical score for it, and the skill says so.

This is a traditional and cultural astrology tool, not a scientific or deterministic prediction. For major decisions, especially marriage, consult a professional astrologer with the full birth chart. The couple's own judgment matters more than any score.
