# horoscope-matching

A [Claude Code](https://claude.com/claude-code) skill for Vedic (jyotish) astrology. It covers four things:

| Output | Input | What you get |
|---|---|---|
| **Life horoscope summary** | One person | A brief read of personality, career/finance, health tendencies and relationship style, based on Rasi (Moon sign) and Nakshatra (lunar mansion) |
| **Marriage matching** | Two people | The traditional Ashtakoota / Guna Milan score out of 36, with a per-koota breakdown and a verdict |
| **Mangal (Kuja) Dosha check** | One or two people | Whether Mars sits in a traditionally sensitive house from the Lagna and the Moon, plus common mitigating factors |
| **Vimshottari Dasha periods** | One or two people | The Mahadasha sequence with start and end dates. For a couple, a joint overlay of whose periods line up |

Claude loads the skill when you mention horoscope, kundli, rasi, nakshatra, guna milan, ashtakoota, nadi dosha, mangal dosha, dasha, and similar terms. It also loads when you ask whether two people's birth details "match" for marriage.

## Installation

Copy or symlink this folder into your Claude Code skills directory:

```bash
# Copy
cp -R horoscope-matching ~/.claude/skills/

# Or symlink, so edits in this repo take effect immediately
ln -s "$(pwd)" ~/.claude/skills/horoscope-matching
```

Then ask Claude something like:

- "Check if my horoscope matches my partner's. I was born 15 Aug 1990 at 2:30 PM in India, and they were born ..."
- "What is the Mangal Dosha status for someone born on 22 Oct 1979 at 1:15 PM in Chennai?"
- "Show my Mahadasha periods."

## What you need to provide

For each person, give either:

- **Rasi and Nakshatra**, if you already know them from a panchang or an astrologer. Claude uses these directly and skips the calculation.
- **Date of birth, exact time of birth and UTC offset** (for example `+5:30` for India). Claude calculates the Moon position.

The Mangal Dosha check also needs the **birth place's latitude and longitude**, because the Ascendant depends on location.

## Repository layout

```
SKILL.md                              Skill definition and workflow that Claude follows
references/
  nakshatra_rasi_traits.md            Traits for the 12 Rasis and 27 Nakshatras, and how to write the summary
  ashtakoota_matching.md              Scoring rules for all 8 kootas, with the simplifications made
  mangal_dosha.md                     Mangal Dosha rules and commonly cited mitigating factors
  dasha_periods.md                    Mahadasha lord significations and the two-person overlay method
scripts/
  compute_rasi_nakshatra.py           Date, time and UTC offset to Rasi, Nakshatra and Pada
  compute_mangal_dosha.py             Adds latitude and longitude to give Lagna, Mars sign and Dosha houses
  compute_vimshottari_dasha.py        Date, time and UTC offset to the Mahadasha sequence
```

## Running the scripts directly

The scripts use only the Python 3 standard library.

```bash
# Rasi, Nakshatra, Pada
python3 scripts/compute_rasi_nakshatra.py 1990-08-15 14:30 +5:30

# Mangal Dosha (date, time, UTC offset, latitude, longitude)
python3 scripts/compute_mangal_dosha.py 1979-10-22 13:15 +5:30 13.0827 80.2707

# Vimshottari Dasha (last argument is the number of years to print, default 100)
python3 scripts/compute_vimshottari_dasha.py 1979-10-22 13:15 +5:30 100
```

Example output for the first command:

```
Sidereal Moon longitude: 51.0496 deg
Rasi:                    Vrishabha (Taurus)
Nakshatra:               Rohini
Pada:                    4
```

## Accuracy and limitations

- **The Moon position is an approximation.** It uses a truncated lunar series and an approximate Lahiri (Chitrapaksha) ayanamsa, with no ephemeris library. It is normally enough to place the Moon in the right Rasi and Nakshatra. When the result falls close to a boundary, the script prints a warning. Check those cases against a precise panchang.
- **Mangal Dosha is less certain.** Mars uses a simplified two-body orbit, and the Ascendant moves about 1° every 4 minutes, so birth-time errors matter more. Treat the result as a rough first pass.
- **Dasha dates are exact arithmetic** once the Moon position is known. What each period means for a person is general traditional color, not an individualized reading.
- **There is no classical score for Dasha compatibility.** The couple overlay is a structured interpretation, and the skill says so.

This is traditional and cultural astrology, not a scientific or deterministic prediction. For significant decisions, especially marriage, consult a professional astrologer with the full birth chart. The couple's own judgment matters more than any score.
