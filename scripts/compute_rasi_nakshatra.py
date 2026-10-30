#!/usr/bin/env python3
"""
Computes sidereal Moon position (Rasi / Nakshatra / Pada) for a birth
date, time, and UTC offset, using the Lahiri (Chitrapaksha) ayanamsa.

No external dependencies. Uses a truncated (~13-term) lunar longitude
series (the standard "abridged" low-precision lunar theory reproduced
in many astronomy references, derived from the ELP2000/82 mean
elements). Expected accuracy: a few arcminutes to roughly half a
degree, which is generally good enough to place the Moon correctly
within a Nakshatra (13d20m wide) and Rasi (30d wide) -- EXCEPT when
the true position falls within about an hour (in Moon-travel terms,
~0.5 degree) of a boundary. This script flags that case explicitly.

Usage:
    python3 compute_rasi_nakshatra.py YYYY-MM-DD HH:MM [+-]UTCOFFSET

Example:
    python3 compute_rasi_nakshatra.py 1990-08-15 14:30 +5:30
"""

import math
import sys


RASI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)",
    "Karka (Cancer)", "Simha (Leo)", "Kanya (Virgo)",
    "Tula (Libra)", "Vrischika (Scorpio)", "Dhanu (Sagittarius)",
    "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)",
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NEAR_BOUNDARY_DEG = 0.5  # flag if within this many degrees of a Rasi/Nakshatra edge


def julian_day(year, month, day, ut_hours):
    """Standard Meeus Julian Day algorithm (Gregorian calendar, UT input)."""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = (
        math.floor(365.25 * (year + 4716))
        + math.floor(30.6001 * (month + 1))
        + day + b - 1524.5 + ut_hours / 24.0
    )
    return jd


def norm360(x):
    x = x % 360.0
    if x < 0:
        x += 360.0
    return x


def moon_tropical_longitude(jd):
    """Truncated lunar longitude series (degrees, tropical)."""
    t = (jd - 2451545.0) / 36525.0

    lp = 218.3164477 + 481267.88123421 * t - 0.0015786 * t**2
    d = 297.8501921 + 445267.1114034 * t - 0.0018819 * t**2
    m = 357.5291092 + 35999.0502909 * t - 0.0001536 * t**2
    mp = 134.9633964 + 477198.8675055 * t + 0.0087414 * t**2
    f = 93.2720950 + 483202.0175233 * t - 0.0036539 * t**2

    lp, d, m, mp, f = (norm360(v) for v in (lp, d, m, mp, f))

    lp_r, d_r, m_r, mp_r, f_r = (math.radians(v) for v in (lp, d, m, mp, f))

    correction = (
        6.289 * math.sin(mp_r)
        - 1.274 * math.sin(mp_r - 2 * d_r)
        + 0.658 * math.sin(2 * d_r)
        - 0.186 * math.sin(m_r)
        - 0.059 * math.sin(2 * mp_r - 2 * d_r)
        - 0.057 * math.sin(mp_r - 2 * d_r + m_r)
        + 0.053 * math.sin(mp_r + 2 * d_r)
        + 0.046 * math.sin(2 * d_r - m_r)
        + 0.041 * math.sin(mp_r - m_r)
        - 0.035 * math.sin(d_r)
        - 0.031 * math.sin(mp_r + m_r)
        - 0.015 * math.sin(2 * f_r - 2 * d_r)
        + 0.011 * math.sin(mp_r - 4 * d_r)
    )

    return norm360(lp + correction)


def lahiri_ayanamsa(decimal_year):
    """
    Approximate Lahiri (Chitrapaksha) ayanamsa in degrees.
    Calibrated to ~23.85 deg at year 2000.0, advancing at the
    general precession rate (~50.3 arcsec/year). Matches commonly
    published Lahiri values (e.g. ~24d11m around 2024) to within a
    few arcminutes.
    """
    return 23.85 + (decimal_year - 2000.0) * 0.013972


def decimal_year(year, month, day):
    # Rough day-of-year based decimal year, fine for an ayanamsa rate this slow.
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    days_cum = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    doy = days_cum[month - 1] + day
    if month > 2 and days_in_year == 366:
        doy += 1
    return year + (doy - 1) / days_in_year


def compute(year, month, day, hour, minute, utc_offset_hours):
    ut_hours = (hour + minute / 60.0) - utc_offset_hours
    jd = julian_day(year, month, day, ut_hours)

    tropical_lon = moon_tropical_longitude(jd)
    ayanamsa = lahiri_ayanamsa(decimal_year(year, month, day))
    sidereal_lon = norm360(tropical_lon - ayanamsa)

    rasi_span = 30.0
    nak_span = 360.0 / 27.0
    pada_span = nak_span / 4.0

    rasi_idx = int(sidereal_lon // rasi_span)
    nak_idx = int(sidereal_lon // nak_span)
    pos_in_nak = sidereal_lon - nak_idx * nak_span
    pada = int(pos_in_nak // pada_span) + 1

    dist_to_rasi_edge = min(sidereal_lon % rasi_span, rasi_span - (sidereal_lon % rasi_span))
    dist_to_nak_edge = min(sidereal_lon % nak_span, nak_span - (sidereal_lon % nak_span))
    near_boundary = dist_to_rasi_edge < NEAR_BOUNDARY_DEG or dist_to_nak_edge < NEAR_BOUNDARY_DEG

    return {
        "julian_day": jd,
        "tropical_longitude_deg": tropical_lon,
        "ayanamsa_deg": ayanamsa,
        "sidereal_longitude_deg": sidereal_lon,
        "rasi": RASI_NAMES[rasi_idx],
        "nakshatra": NAKSHATRA_NAMES[nak_idx],
        "pada": pada,
        "near_boundary": near_boundary,
    }


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    date_str, time_str, offset_str = sys.argv[1:4]
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

    result = compute(year, month, day, hour, minute, utc_offset)

    print(f"Julian Day (UT):        {result['julian_day']:.6f}")
    print(f"Tropical Moon longitude: {result['tropical_longitude_deg']:.4f} deg")
    print(f"Ayanamsa (Lahiri):       {result['ayanamsa_deg']:.4f} deg")
    print(f"Sidereal Moon longitude: {result['sidereal_longitude_deg']:.4f} deg")
    print(f"Rasi:                    {result['rasi']}")
    print(f"Nakshatra:               {result['nakshatra']}")
    print(f"Pada:                    {result['pada']}")
    if result["near_boundary"]:
        print(
            "WARNING: computed position is within ~0.5 deg of a Rasi/Nakshatra "
            "boundary. Given the approximate nature of this calculation, treat "
            "the result as uncertain and recommend verifying against a precise "
            "panchang or professional astrologer, especially if exact birth "
            "time is uncertain."
        )


if __name__ == "__main__":
    main()
