# Mangal Dosha (Kuja Dosha) reference

Mangal Dosha is a traditional factor checked **in addition to** the
Ashtakoota/Guna Milan score — it's not one of the 8 kootas, it's a separate
check based on where Mars sits in the birth chart.

## What it needs

Unlike the Ashtakoota koota calculations (which only need Rasi/Nakshatra),
Mangal Dosha needs the **Ascendant (Lagna)**, which requires birth
**place coordinates** (latitude/longitude), not just a UTC offset — the
Ascendant is sensitive to exact location and exact time in a way the Moon's
position is not. Run `scripts/compute_mangal_dosha.py` with the birth
date, time, UTC offset, latitude, and longitude to get the Lagna, Moon
sign, and Mars sign, and the houses Mars falls in relative to each.

**Accuracy note (important):** this script uses a simplified two-body
model for Mars's orbit and a standard Ascendant formula, not full
perturbation theory. Treat results as a reasonable first pass, with wider
uncertainty than the Rasi/Nakshatra calculation — especially if birth time
isn't known to the exact minute (the Ascendant moves about 1° every 4
minutes). If the script prints the near-boundary warning, say so plainly
and recommend verification with real astrology software or a professional.

## The core rule

Mangal Dosha is traditionally present if Mars occupies one of these houses,
counted from the **Lagna (Ascendant)**: **1, 2, 4, 7, 8, or 12**. Many
traditions also check the same house set counted from the **Moon sign**
(Chandra Lagna), and some additionally check from Venus — this skill checks
from Lagna and from Moon, and says so explicitly rather than implying a
single definitive check.

Report whichever reference point(s) show the dosha. Dosha from Lagna is
generally treated as the primary check; dosha from Moon is often treated as
an additional/secondary indicator.

## Commonly cited mitigating factors (not exhaustive)

Classical texts list many conditions that reduce or cancel Mangal Dosha.
This skill can only check the ones computable from what it already has —
say explicitly that other classical exceptions exist but aren't checked here:

- **Mars in its own sign** (Mesha/Aries or Vrischika/Scorpio) **or exalted
  sign** (Makara/Capricorn) while in a dosha house: traditionally
  considered to significantly weaken or cancel the dosha.
- **Mutual Mangal Dosha**: if *both* partners show Mangal Dosha (from the
  same reference point, e.g. both from Lagna), many traditions treat this
  as self-cancelling — the idea being that both are equally affected, so
  neither is at a disadvantage relative to the other.
- Not checked here (mention as unverified classical factors if relevant):
  Jupiter's aspect/conjunction with Mars, dosha from Venus's position,
  and various house-specific sub-exceptions some regional traditions apply.

## Presenting the result

For each person, state: Lagna sign, Mars sign, house from Lagna, house from
Moon, whether each is a dosha house, and whether Mars is in its own/exalted
sign. Then give an overall read combining both people — call out mutual
dosha cancellation explicitly if it applies, since it changes the practical
conclusion even though it doesn't change either person's raw chart.

Close with the same spirit as the rest of this skill: this is a traditional
calculation with real uncertainty in this implementation, not a verdict —
for something this emotionally and socially weighted, a professional
astrologer working from precise birth records is worth more than this
approximation, especially when the result is close to a boundary.
