# Ashtakoota (Guna Milan) matching reference

The traditional Vedic "36-point" marriage-compatibility system (Ashtakoota /
Guna Milan) compares the Rasi (Moon sign) and Nakshatra (lunar mansion) of
two people across 8 kootas (factors), each with its own weight, totaling 36.

This file implements the standard simplified scoring rules used by most
computerized Kundli-matching tools. Professional astrologers may also weigh
additional factors (Mangal dosha, planetary dashas, the full chart) that are
out of scope here — say so in the output, per SKILL.md's disclaimer.

You need, for each person: **Rasi** and **Nakshatra** (from direct input or
from `compute_rasi_nakshatra.py`).

## The 8 kootas

| # | Koota | Max pts | Based on |
|---|---|---|---|
| 1 | Varna | 1 | Rasi |
| 2 | Vashya | 2 | Rasi |
| 3 | Tara | 3 | Nakshatra |
| 4 | Yoni | 4 | Nakshatra |
| 5 | Graha Maitri | 5 | Rasi lord |
| 6 | Gana | 6 | Nakshatra |
| 7 | Bhakoot | 7 | Rasi |
| 8 | Nadi | 8 | Nakshatra |
| | **Total** | **36** | |

### 1. Varna (1 point) — spiritual/social temperament hierarchy

Each Rasi belongs to a Varna:
- **Brahmin** (highest): Karka, Vrischika, Meena
- **Kshatriya**: Mesha, Simha, Dhanu
- **Vaishya**: Vrishabha, Kanya, Makara
- **Shudra**: Mithuna, Tula, Kumbha

Scoring: 1 point if the groom's Varna is equal to or higher than the bride's
(Brahmin > Kshatriya > Vaishya > Shudra); 0 points if the bride's Varna is
higher than the groom's. If you don't know which person is "groom"/"bride"
(e.g. same-sex couple or unspecified), score it both ways and report 1 point
if either ordering satisfies the rule, noting the traditional framing assumes
a bride/groom direction.

### 2. Vashya (2 points) — mutual control/dominance in the relationship

Simplified Rasi groups (classical texts split Dhanu and Makara by half-sign;
this simplified whole-sign version is what most calculators use):
- **Chatushpada** (quadruped): Mesha, Vrishabha, Dhanu
- **Manava** (human): Mithuna, Kanya, Tula, Kumbha
- **Jalachara** (aquatic): Karka, Meena, Makara
- **Vanachara** (wild): Simha
- **Keeta** (insect): Vrischika

Scoring:
- Same group: 2
- Manava + Jalachara, or Manava + Chatushpada: 1
- Vanachara + Chatushpada: 1 (lion partially dominates quadruped)
- Any pairing involving Keeta with a different group: 0.5
- All other different-group pairings: 0

### 3. Tara (3 points) — the two nakshatras' numerical relationship

Count nakshatra positions (1–27, Ashwini=1 ... Revati=27). For each direction:
1. Count from person A's nakshatra to person B's nakshatra inclusive (wrapping past 27 back to 1).
2. Take that count modulo 9 (if the remainder is 0, treat it as 9) → gives a Tara type 1–9:
   `1 Janma, 2 Sampat, 3 Vipat, 4 Kshema, 5 Pratyak, 6 Sadhaka, 7 Vadha (Naidhana), 8 Mitra, 9 Ati-Mitra (Parama Mitra)`
3. Types 1, 3, 5, 7 (Janma, Vipat, Pratyak, Vadha) are inauspicious → 0 points for that direction.
   All other types → 1.5 points for that direction.

Do this for both directions (A→B and B→A) and sum the two (max 3).

### 4. Yoni (4 points) — symbolic "animal nature" compatibility

Each nakshatra maps to one of 14 Yoni (animal) symbols:

| Yoni | Nakshatras |
|---|---|
| Horse | Ashwini, Shatabhisha |
| Elephant | Bharani, Revati |
| Sheep/Goat | Krittika, Pushya |
| Serpent | Rohini, Mrigashira |
| Dog | Ardra, Mula |
| Cat | Punarvasu, Ashlesha |
| Rat | Magha, Purva Phalguni |
| Cow | Uttara Phalguni, Uttara Bhadrapada |
| Buffalo | Hasta, Swati |
| Tiger | Chitra, Vishakha |
| Deer | Anuradha, Jyeshtha |
| Monkey | Purva Ashadha, Shravana |
| Mongoose/Weasel | Uttara Ashadha |
| Lion | Dhanishta, Purva Bhadrapada |

Scoring:
- Same Yoni: 4
- Friendly pair (same broad temperament — e.g. two grazing/herd animals): 3
- Neutral (no special relationship): 2
- Mild rivalry: 1
- Natural predator/prey pairs (traditionally the strongest clash) — notably
  **Rat↔Cat, Cow↔Tiger, Buffalo↔Horse, Deer↔Dog, Monkey↔Sheep/Goat, Elephant↔Lion,
  Mongoose↔Serpent**: 0

When the specific pair isn't one of the well-known friend/enemy pairs listed
above, use 2 (neutral) as the default rather than guessing — flag in your
output that the Yoni score used a neutral default for that pair.

### 5. Graha Maitri (5 points) — friendship between the two Rasi lords

Rasi lords: Mesha/Vrischika→Mars, Vrishabha/Tula→Venus, Mithuna/Kanya→Mercury,
Karka→Moon, Simha→Sun, Dhanu/Meena→Jupiter, Makara/Kumbha→Saturn.

Classical natural-friendship table (Naisargika Maitri):

| Planet | Friends | Neutral | Enemies |
|---|---|---|---|
| Sun | Moon, Mars, Jupiter | Mercury | Venus, Saturn |
| Moon | Sun, Mercury | Mars, Jupiter, Venus, Saturn | — |
| Mars | Sun, Moon, Jupiter | Venus, Saturn | Mercury |
| Mercury | Sun, Venus | Mars, Jupiter, Saturn | Moon |
| Jupiter | Sun, Moon, Mars | Saturn | Mercury, Venus |
| Venus | Mercury, Saturn | Mars, Jupiter | Sun, Moon |
| Saturn | Mercury, Venus | Jupiter | Sun, Moon, Mars |

Look up each lord's view of the other (the table is not always symmetric),
then combine:
- Same lord for both (identical planet): 5
- Both see each other as friends: 5
- One friend + other neutral: 4
- Both neutral: 3
- One neutral + other enemy: 1
- One friend + other enemy: 1
- Both enemies: 0

### 6. Gana (6 points) — temperament group (Deva/Manushya/Rakshasa)

Gana per nakshatra is in `nakshatra_rasi_traits.md`. Scoring (simplified
symmetric version used by most modern calculators):
- Same Gana: 6
- Deva + Manushya: 6
- Deva + Rakshasa: 0
- Manushya + Rakshasa: 0

### 7. Bhakoot (7 points) — Rasi distance

Count the Rasi position distance (1–12) from person A's Rasi to person B's
Rasi, and vice versa. If either direction's count is **2/12, 5/9, or 6/8**
(the three classically inauspicious distance pairs — "Dwadasha", "Navapancham",
"Shadashtak"), it's a **Bhakoot Dosha**: 0 points. Otherwise: 7 points.

**Exception**: classical texts cancel Bhakoot Dosha if both Rasi lords are the
same planet. Apply this exception and note it explicitly if it changes the score.

### 8. Nadi (8 points) — the biggest single koota; Vata/Pitta/Kapha-style classification

Nadi per nakshatra (fixed groups of 9):
- **Adi**: Ashwini, Ardra, Punarvasu, Uttara Phalguni, Hasta, Jyeshtha, Mula, Shatabhisha, Purva Bhadrapada
- **Madhya**: Bharani, Mrigashira, Pushya, Purva Phalguni, Chitra, Anuradha, Purva Ashadha, Dhanishta, Uttara Bhadrapada
- **Antya**: Krittika, Rohini, Ashlesha, Magha, Swati, Vishakha, Uttara Ashadha, Shravana, Revati

Scoring:
- Different Nadi: 8 (full)
- Same Nadi: 0 — this is **Nadi Dosha**, traditionally one of the most
  significant red flags in matching, even when the total score is otherwise good.

**Exception**: some classical sources cancel Nadi Dosha if both people also
share the exact same Rasi *and* same Nakshatra (i.e. effectively the same
birth star). Mention this exception only if it applies; otherwise, flag Nadi
Dosha clearly.

## Producing the verdict

1. Sum all 8 koota scores → total out of 36.
2. Apply standard thresholds (widely used, not a strict scientific cutoff):
   - **18 and above**: traditionally considered an acceptable match.
   - **24 and above**: considered a good/favorable match.
   - **Below 18**: traditionally discouraged, though not an absolute bar —
     real practice weighs which specific kootas failed and why.
3. Regardless of total score, **explicitly call out Nadi Dosha and Bhakoot
   Dosha by name** if present — these are traditionally treated as more
   serious than a simple point deduction, and many families/astrologers will
   want them flagged even in an otherwise high-scoring match.
4. Always close with the disclaimer: this is a traditional/cultural
   calculation (not scientific), real kundli matching also considers Mangal
   dosha and other chart factors not covered here, and major life decisions
   should weigh the couple's own compatibility and (if desired) a
   professional astrologer's full reading — not this score alone.
