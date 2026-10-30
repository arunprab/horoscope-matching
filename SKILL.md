---
name: horoscope-matching
description: "Generate a Vedic/Indian-astrology life-horoscope summary for one person, run traditional marriage-compatibility (kundli/horoscope) matching between two people, check Mangal/Kuja Dosha, or map out Vimshottari Dasha (Mahadasha) planetary periods — including a joint overlay of favorable/challenging periods for a couple. Trigger this skill whenever the user mentions horoscope, kundli, birth chart, Rasi, Nakshatra, Moon sign in an Indian-astrology sense, panchang, janam patri, guna milan, ashtakoota, nadi dosha, mangal dosha, kuja dosha, dasha, mahadasha, or asks whether two people's horoscopes/birth details 'match' for marriage, engagement, or compatibility, or asks about good/bad/favorable time periods in an astrological sense — even if they only give a date and time of birth without using any of this vocabulary (e.g. 'can you check if me and my partner's birth details are compatible for marriage' or 'when is a good time period for us'). Use it for a single-person reading, two-person matching, or a couple's joint period overlay."
---

# Horoscope matching (Vedic astrology)

This skill produces four kinds of output, grounded in traditional Vedic
(jyotish) astrology:

1. **Life horoscope summary** — for one person, a brief read of personality,
   career/finance, health tendencies, and relationship style based on their
   Rasi (Moon sign) and Nakshatra (lunar mansion).
2. **Marriage matching** — for two people, the traditional Ashtakoota / Guna
   Milan 36-point compatibility score, with a breakdown and verdict.
3. **Mangal Dosha (Kuja Dosha) check** — for one or two people, whether Mars
   falls in a traditionally sensitive house, and known mitigating factors.
4. **Vimshottari Dasha (Mahadasha) periods** — for one person, the exact
   sequence of planetary life-periods; for a couple, a joint overlay of
   whose periods line up and how they traditionally relate to each other.

The first two rest on the same core inputs: each person's **Rasi** and
**Nakshatra**. Get those first, then branch into whichever output the user
asked for (or several, if they want more than one — e.g. a summary for each
person *and* a match score, or a match score *and* a Dasha overlay).

## Step 1: Collect inputs

For each person involved, ask for whichever of these they can give — don't
demand all of them if they already know their Rasi/Nakshatra:

- **Rasi and Nakshatra**, if they already know them (e.g. from a family
  priest, a panchang, or prior astrology software). If given, **use these
  directly and skip calculation** — a value from an actual birth chart is
  more trustworthy than this skill's approximate calculation.
- Otherwise, **date of birth**, **exact time of birth** (as precise as
  possible — minutes matter), and the **UTC offset** for where they were born
  (e.g. "+5:30" for India). Birth place name is welcome for narrative context
  but isn't needed for the calculation itself (Moon position barely depends
  on location, only on the moment in UTC).

If someone gives a birth place but not a UTC offset, ask for the UTC offset
directly rather than guessing a timezone from the place name — get it right
rather than silently assuming.

## Step 2: Get Rasi and Nakshatra

- **If Rasi/Nakshatra were given directly**: use them as-is.
- **If not**: run the bundled calculator:

```bash
python3 scripts/compute_rasi_nakshatra.py YYYY-MM-DD HH:MM [+-]UTCOFFSET
```

Example: `python3 scripts/compute_rasi_nakshatra.py 1990-08-15 14:30 +5:30`

This is a self-contained, dependency-free approximation (no internet, no
ephemeris library) using a truncated lunar-position series and an
approximate Lahiri (Chitrapaksha) ayanamsa — see the script's docstring for
the method. It's accurate to roughly a few arcminutes up to perhaps half a
degree, which is normally enough to place the Moon correctly within its
Nakshatra (13°20′ wide) and Rasi (30° wide).

**If the script prints the near-boundary warning**, tell the user plainly:
their result landed close to a sign/star boundary, so small uncertainty in
birth time (or in this approximation) could put the true value in the
neighboring Rasi or Nakshatra instead. Recommend double-checking against a
precise panchang or a professional astrologer before relying on the result,
especially if they're not fully confident about the exact birth minute.

## Step 3: Produce the output

### For a life horoscope summary

Read `references/nakshatra_rasi_traits.md` and follow its "Writing the
summary" section: blend the Rasi's and Nakshatra's traits into a brief,
readable narrative covering personality & temperament, career & finance,
health tendencies, and relationships & marriage style. Keep it to a few
sentences per dimension — the user asked for *brief*, not an exhaustive
reading. Present tendencies as traditional associations ("in this tradition,
X Nakshatra is associated with...") rather than as fortune-telling certainty.

### For marriage matching between two people

Read `references/ashtakoota_matching.md` and work through all 8 kootas
(Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi) for the two
people's Rasi/Nakshatra pairs. Show your work as a per-koota table (score
and a short reason), then the total out of 36, then the verdict using the
thresholds in that file. Explicitly call out Nadi Dosha or Bhakoot Dosha by
name if either applies, regardless of the total score — these traditionally
matter beyond their point value, and burying them in the total would
mislead the user about what the match score is actually saying.

If the user wants both a life summary *and* a match score, do the life
summaries first (one per person) and the match score after — the match score
is easier to interpret once the reader has a feel for each person's chart.

### Optional: favorable/challenging life periods (Vimshottari Dasha)

If the user asks about good/bad time periods, "dasha," or when something is
favorable in life, read `references/dasha_periods.md` and run
`scripts/compute_vimshottari_dasha.py` with the person's DOB, time, and UTC
offset. This is exact arithmetic (no astronomical approximation beyond the
Moon position already computed in Step 2) — but what each period *means*
for that specific person is general traditional color, not a personalized
verdict, since a true individualized read needs the full chart. Say that
distinction explicitly rather than implying more precision than you have.

### Optional: joint Dasha overlay for a couple

If the user asks about Dasha "compatibility," or whether their periods line
up, read the "Two-person Dasha overlay" section of `references/dasha_periods.md`.
There is no fixed classical score for this — say so up front — then merge
both people's Mahadasha sequences into a shared timeline, look up the
natural planetary friendship (Graha Maitri, from `ashtakoota_matching.md`)
between whichever lords are running in each segment, and combine that with
each lord's general flavor. Focus the write-up on the current segment and
the next one or two; a full-lifetime grid is fine to show for transparency
but isn't what the user is actually asking for.

### Optional: Mangal Dosha (Kuja Dosha) check

If the user asks about Mangal Dosha (or "Mars dosha", "Kuja dosha") in
addition to or instead of the Ashtakoota score, read
`references/mangal_dosha.md` and run `scripts/compute_mangal_dosha.py`.
This needs birth **place coordinates** (latitude/longitude), not just the
UTC offset used elsewhere — ask for the birth city if you don't already
have coordinates, and only use well-known coordinates you're confident
about rather than guessing. This check carries more uncertainty than the
Rasi/Nakshatra calculation (see the script's docstring) — say so, and flag
near-boundary results clearly.

## Always include this closing note

End every output (summary or match) with a short, plain disclaimer: this is
a traditional/cultural astrology calculation, not a scientific or
deterministic prediction; the Rasi/Nakshatra calculation here is an
approximation when not given directly; and for significant decisions
(especially marriage matching), consulting a professional astrologer with
the full birth chart — and, more importantly, the couple's own judgment — is
worth more than any single score.

## Reference files

- `references/nakshatra_rasi_traits.md` — personality/career/health/
  relationship associations for all 12 Rasis and 27 Nakshatras, and how to
  weave them into a life-summary narrative.
- `references/ashtakoota_matching.md` — full Guna Milan scoring rules for
  all 8 kootas, including the simplifications made and why.
- `references/mangal_dosha.md` — Mangal Dosha rules, what it needs beyond
  the Ashtakoota inputs, and commonly cited mitigating factors.
- `references/dasha_periods.md` — general traditional significations for
  each Vimshottari Mahadasha lord, how to present a life-period overview,
  and how to build a two-person Dasha overlay ("Dasha compatibility").
- `scripts/compute_rasi_nakshatra.py` — DOB + time + UTC offset → Rasi,
  Nakshatra, Pada (run directly with `python3`, no dependencies).
- `scripts/compute_mangal_dosha.py` — DOB + time + UTC offset + lat/lon →
  Lagna, Mars sign, and Mangal Dosha houses from Lagna and Moon.
- `scripts/compute_vimshottari_dasha.py` — DOB + time + UTC offset →
  full Mahadasha sequence with start/end dates.
