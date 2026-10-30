# Vimshottari Mahadasha — general period significations

`scripts/compute_vimshottari_dasha.py` gives exact Mahadasha date ranges —
that part is deterministic arithmetic once you know the Moon's Nakshatra and
position within it, not an approximation. **What each period actually means
for a specific person is a different matter**: classically that depends on
which house the Dasha lord occupies and rules in *that person's own chart*,
its strength, and aspects on it — none of which this skill computes (it
would need the full chart, not just Lagna/Moon/Mars). So present the table
below as **general traditional associations with each planet's period**,
not a personalized verdict on whether a given stretch of someone's life will
be "good" or "bad." Say this distinction out loud when you give the reading.

| Dasha Lord | Years | General traditional associations |
|---|---|---|
| Sun | 6 | Authority, recognition, government/leadership matters, focus on self and health; can bring both visibility and ego-related friction |
| Moon | 10 | Emotional life, home, family, the public, changeability; a nurturing but sometimes fluctuating period |
| Mars | 7 | Energy, action, courage, property, siblings; can bring achievement through effort, but also conflict or impatience |
| Rahu | 18 | Ambition, unconventional paths, sudden gains or disruptions, foreign/unfamiliar domains; often eventful and hard to predict |
| Jupiter | 16 | Growth, wisdom, higher learning, prosperity, mentorship, children; widely considered one of the more favorable periods |
| Saturn | 19 | Discipline, hard work, delays followed by durable results, responsibility; a long period often read as effortful but structure-building |
| Mercury | 17 | Intellect, communication, business, learning, adaptability; generally a stable, versatile period |
| Ketu | 7 | Detachment, introspection, spiritual inclination, loose ends from the past; can feel unmoored but also liberating |
| Venus | 20 | Relationships, comfort, creativity, wealth, domestic harmony; the longest period and widely considered among the most favorable |

## Two-person Dasha overlay ("Dasha compatibility")

There is no single codified classical koota for "Dasha compatibility" the
way there is for Ashtakoota — be upfront about that if asked for it rather
than presenting a fabricated score as if it were a standard traditional
system. What's reasonable to offer instead is a transparent synthesis of
two things that *are* well-grounded:

1. **Merge both people's Mahadasha sequences into a shared timeline** —
   wherever one person's period boundary falls, split the timeline there,
   so each segment has one fixed lord per person.
2. **For each segment, look up the natural planetary friendship (Graha
   Maitri)** between the two running lords, using the same table in
   `ashtakoota_matching.md`. Rahu and Ketu have no entry in the classical
   Graha Maitri table (they're nodes, not the 7 classical grahas) — the
   common practical workaround, which you should name explicitly when you
   use it, is to treat **Rahu like Saturn** and **Ketu like Mars** for this
   lookup only.
3. Combine that friendship read with each lord's general signification
   (table above) to describe the segment's flavor — e.g. "mutual friends,
   and both periods lean favorable" reads differently from "mutual friends,
   but one period is about discipline/delay and the other about comfort."

Present this focused on **today's segment and the next one or two** — a
full-lifetime table is fine to show for transparency, but the couple almost
always wants "right now and what's coming," not a 50-year grid. Mention
older/pre-relationship segments only in passing if at all, since a planetary
overlay from before two people met isn't meaningful for their relationship.

Close by naming this explicitly as a synthesis you built from two
traditional ingredients, not a fixed classical score — and repeat the usual
caveat that real compatibility depends on far more than this overlay.

## Presenting a "life overview"

1. Run the script, get the full sequence of Mahadashas across the requested span.
2. Identify which period covers **today's date** for each person, and the one or two periods after it — that's usually what people actually want to know ("what's happening now / coming up"), even if they asked for a full life map.
3. For each relevant period, give the general signification from the table above, explicitly framed as "traditionally associated with," and note that Jupiter and Venus periods are the two most consistently described as broadly favorable across classical texts, while Rahu, Ketu, and Saturn periods are more often described as effortful, transformative, or uneven — without casting any of them as simply "bad," since classical texts tie real outcomes to chart specifics this tool doesn't compute.
4. If the user is a couple, note where their current/upcoming periods land relative to each other — e.g. both currently in a long benefic-leaning period is worth mentioning as a general positive signal, same as you'd note a shared Mangal Dosha pattern.
5. Close with the same disclaimer spirit as the rest of this skill, adding specifically: a personalized "good vs. bad" reading of any period really depends on that person's full chart (house lordships, transits, aspects), which this tool doesn't compute — so treat this as general traditional color, not a timed prediction.
