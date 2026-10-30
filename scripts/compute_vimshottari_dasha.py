#!/usr/bin/env python3
"""
Computes the Vimshottari Dasha sequence (Mahadasha periods) from birth
date, time, and UTC offset. This is deterministic once you have the
Moon's sidereal longitude -- no extra approximation beyond what
compute_rasi_nakshatra.py already does for the Moon.

The Vimshottari system assigns a fixed 120-year cycle of 9 planetary
periods (Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16,
Saturn 19, Mercury 17), always in that order. Which planet's period is
running at birth -- and how much of it is already "used up" -- is fixed
by the birth Nakshatra and the Moon's exact position within it.

Usage:
    python3 compute_vimshottari_dasha.py YYYY-MM-DD HH:MM [+-]UTCOFFSET [YEARS]

YEARS: how many years of the sequence to print (default 100).

Example:
    python3 compute_vimshottari_dasha.py 1979-10-22 13:15 +5:30 100
"""

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compute_rasi_nakshatra as moon

DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
DAYS_PER_YEAR = 365.2425


def sidereal_moon_longitude(year, month, day, hour, minute, utc_offset_hours):
    ut_hours = (hour + minute / 60.0) - utc_offset_hours
    jd = moon.julian_day(year, month, day, ut_hours)
    ayanamsa = moon.lahiri_ayanamsa(moon.decimal_year(year, month, day))
    return moon.norm360(moon.moon_tropical_longitude(jd) - ayanamsa)


def dasha_sequence(birth_date, sidereal_lon, span_years=100.0):
    nak_span = 360.0 / 27.0
    nak_idx = int(sidereal_lon // nak_span)
    pos_in_nak = sidereal_lon - nak_idx * nak_span
    fraction_elapsed = pos_in_nak / nak_span

    start_order_idx = nak_idx % 9
    start_lord = DASHA_ORDER[start_order_idx]
    balance_years = (1 - fraction_elapsed) * DASHA_YEARS[start_lord]

    periods = []
    cursor = birth_date
    end = birth_date + datetime.timedelta(days=balance_years * DAYS_PER_YEAR)
    periods.append((start_lord, cursor, end, DASHA_YEARS[start_lord], balance_years))
    cursor = end

    idx = start_order_idx
    total_days = span_years * DAYS_PER_YEAR
    while (cursor - birth_date).days < total_days:
        idx = (idx + 1) % 9
        lord = DASHA_ORDER[idx]
        full_years = DASHA_YEARS[lord]
        end = cursor + datetime.timedelta(days=full_years * DAYS_PER_YEAR)
        periods.append((lord, cursor, end, full_years, full_years))
        cursor = end

    return periods, nak_idx, fraction_elapsed


def main():
    if len(sys.argv) not in (4, 5):
        print(__doc__)
        sys.exit(1)

    date_str, time_str, offset_str = sys.argv[1:4]
    span_years = float(sys.argv[4]) if len(sys.argv) == 5 else 100.0

    year, month, day = (int(x) for x in date_str.split("-"))
    hour, minute = (int(x) for x in time_str.split(":"))

    sign = 1
    s = offset_str.strip()
    if s.startswith("-"):
        sign = -1
        s = s[1:]
    elif s.startswith("+"):
        s = s[1:]
    if ":" in s:
        oh, om = (int(x) for x in s.split(":"))
    else:
        oh, om = int(s), 0
    utc_offset = sign * (oh + om / 60.0)

    birth_date = datetime.date(year, month, day)
    sidereal_lon = sidereal_moon_longitude(year, month, day, hour, minute, utc_offset)

    periods, nak_idx, fraction_elapsed = dasha_sequence(birth_date, sidereal_lon, span_years)

    print(f"Birth Nakshatra: {moon.NAKSHATRA_NAMES[nak_idx]}")
    print(f"Fraction of birth Nakshatra already elapsed at birth: {fraction_elapsed:.4f}")
    print()
    print(f"{'Mahadasha Lord':<10} {'Start':<12} {'End':<12} {'Duration (yrs)':>15}")
    for lord, start, end, full_years, this_run_years in periods:
        print(f"{lord:<10} {start.isoformat():<12} {end.isoformat():<12} {this_run_years:>15.2f}")


if __name__ == "__main__":
    main()
