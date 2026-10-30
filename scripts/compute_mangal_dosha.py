#!/usr/bin/env python3
"""
Checks for Mangal Dosha (Kuja Dosha): whether Mars falls in one of the
traditionally inauspicious houses counted from the Ascendant (Lagna) and/or
from the Moon sign.

This needs more than compute_rasi_nakshatra.py: it needs the Ascendant,
which depends on birth *place* (latitude/longitude), not just a UTC offset,
because the Ascendant is highly sensitive to the exact local sidereal time.
It also needs Mars's position, computed here with a simplified two-body
(Keplerian) orbital model -- NOT a full perturbation theory. Expect larger
uncertainty here than in compute_rasi_nakshatra.py:
  - The Ascendant moves ~1 degree every 4 minutes of time, so any birth-time
    uncertainty matters much more here than for the Moon.
  - Mars's simplified orbit can be off by roughly half a degree to a couple
    of degrees depending on epoch, which can occasionally flip which sign
    (and therefore house) Mars appears to be in.
This script flags "near boundary" cases, but treat Mangal Dosha results from
this tool as a rough first pass, not a substitute for a professional chart.

Usage:
    python3 compute_mangal_dosha.py YYYY-MM-DD HH:MM [+-]UTCOFFSET LAT LON

LAT: positive = North, negative = South.
LON: positive = East, negative = West.

Example (Chennai, India):
    python3 compute_mangal_dosha.py 1979-10-22 13:15 +5:30 13.0827 80.2707
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compute_rasi_nakshatra as moon  # reuse JD / Moon / ayanamsa logic

RASI_NAMES = moon.RASI_NAMES
NEAR_BOUNDARY_DEG = 0.75  # wider than the Moon script's, since inputs here are noisier

MARS_OWN_SIGNS = {0, 7}       # Mesha, Vrischika
MARS_EXALTED_SIGN = 9         # Makara
DOSHA_HOUSES = {1, 2, 4, 7, 8, 12}


def mean_obliquity_deg(t):
    return 23.4392911 - 0.0130042 * t


def gmst_degrees(jd):
    t = (jd - 2451545.0) / 36525.0
    gmst = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * t**2
        - t**3 / 38710000.0
    )
    return moon.norm360(gmst)


def ascendant_tropical_longitude(jd, geo_lon_east_deg, geo_lat_deg):
    t = (jd - 2451545.0) / 36525.0
    eps = math.radians(mean_obliquity_deg(t))
    lst_deg = moon.norm360(gmst_degrees(jd) + geo_lon_east_deg)
    theta = math.radians(lst_deg)
    phi = math.radians(geo_lat_deg)

    y = math.cos(theta)
    x = -(math.sin(eps) * math.tan(phi) + math.cos(eps) * math.sin(theta))
    return moon.norm360(math.degrees(math.atan2(y, x)))


def solve_kepler(m_deg, e, iterations=8):
    m = math.radians(m_deg)
    ec = m
    for _ in range(iterations):
        ec = ec - (ec - e * math.sin(ec) - m) / (1 - e * math.cos(ec))
    return ec  # radians


def sun_geocentric(d):
    """Returns (longitude_deg, distance_au) -- used as Earth's position reference."""
    w = 282.9404 + 4.70935e-5 * d
    e = 0.016709 - 1.151e-9 * d
    m = moon.norm360(356.0470 + 0.9856002585 * d)
    ec = solve_kepler(m, e)
    xv = math.cos(ec) - e
    yv = math.sqrt(1 - e**2) * math.sin(ec)
    r = math.hypot(xv, yv)
    v = math.degrees(math.atan2(yv, xv))
    lon = moon.norm360(v + w)
    return lon, r


def mars_geocentric_longitude(d):
    """Simplified two-body heliocentric Mars position, converted to geocentric."""
    n = math.radians(moon.norm360(49.5574 + 2.11081e-5 * d))
    i = math.radians(1.8497 - 1.78e-8 * d)
    w = math.radians(moon.norm360(286.5016 + 2.92961e-5 * d))
    a = 1.523688
    e = 0.093405 + 2.516e-9 * d
    m = moon.norm360(18.6021 + 0.5240207766 * d)

    ec = solve_kepler(m, e)
    xv = a * (math.cos(ec) - e)
    yv = a * (math.sqrt(1 - e**2) * math.sin(ec))
    r = math.hypot(xv, yv)
    v = math.atan2(yv, xv)

    vw = v + w
    xh = r * (math.cos(n) * math.cos(vw) - math.sin(n) * math.sin(vw) * math.cos(i))
    yh = r * (math.sin(n) * math.cos(vw) + math.cos(n) * math.sin(vw) * math.cos(i))

    sun_lon, sun_r = sun_geocentric(d)
    sun_lon_rad = math.radians(sun_lon)
    xs = sun_r * math.cos(sun_lon_rad)
    ys = sun_r * math.sin(sun_lon_rad)

    xg = xh + xs
    yg = yh + ys
    return moon.norm360(math.degrees(math.atan2(yg, xg)))


def house_from(sign_idx, reference_sign_idx):
    return ((sign_idx - reference_sign_idx) % 12) + 1


def compute(year, month, day, hour, minute, utc_offset_hours, lat, lon):
    ut_hours = (hour + minute / 60.0) - utc_offset_hours
    jd = moon.julian_day(year, month, day, ut_hours)
    d = jd - 2451545.0

    ayanamsa = moon.lahiri_ayanamsa(moon.decimal_year(year, month, day))

    moon_sidereal = moon.norm360(moon.moon_tropical_longitude(jd) - ayanamsa)
    moon_sign = int(moon_sidereal // 30)

    asc_sidereal = moon.norm360(ascendant_tropical_longitude(jd, lon, lat) - ayanamsa)
    asc_sign = int(asc_sidereal // 30)

    mars_sidereal = moon.norm360(mars_geocentric_longitude(d) - ayanamsa)
    mars_sign = int(mars_sidereal // 30)

    house_from_lagna = house_from(mars_sign, asc_sign)
    house_from_moon = house_from(mars_sign, moon_sign)

    dosha_from_lagna = house_from_lagna in DOSHA_HOUSES
    dosha_from_moon = house_from_moon in DOSHA_HOUSES

    mars_strong = mars_sign in MARS_OWN_SIGNS or mars_sign == MARS_EXALTED_SIGN

    def near_edge(lon_deg):
        rem = lon_deg % 30.0
        return min(rem, 30.0 - rem) < NEAR_BOUNDARY_DEG

    return {
        "ayanamsa_deg": ayanamsa,
        "moon_rasi": RASI_NAMES[moon_sign],
        "lagna_rasi": RASI_NAMES[asc_sign],
        "mars_rasi": RASI_NAMES[mars_sign],
        "house_from_lagna": house_from_lagna,
        "house_from_moon": house_from_moon,
        "dosha_from_lagna": dosha_from_lagna,
        "dosha_from_moon": dosha_from_moon,
        "mars_in_own_or_exalted_sign": mars_strong,
        "near_boundary": near_edge(asc_sidereal) or near_edge(mars_sidereal) or near_edge(moon_sidereal),
    }


def main():
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)

    date_str, time_str, offset_str, lat_str, lon_str = sys.argv[1:6]
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

    lat = float(lat_str)
    lon = float(lon_str)

    r = compute(year, month, day, hour, minute, utc_offset, lat, lon)

    print(f"Moon Rasi:              {r['moon_rasi']}")
    print(f"Lagna (Ascendant) Rasi: {r['lagna_rasi']}")
    print(f"Mars Rasi:              {r['mars_rasi']}")
    print(f"Mars house from Lagna:  {r['house_from_lagna']} ({'DOSHA' if r['dosha_from_lagna'] else 'clear'})")
    print(f"Mars house from Moon:   {r['house_from_moon']} ({'DOSHA' if r['dosha_from_moon'] else 'clear'})")
    print(f"Mars in own/exalted sign (possible mitigation): {r['mars_in_own_or_exalted_sign']}")
    if r["near_boundary"]:
        print(
            "WARNING: a key longitude (Lagna, Mars, or Moon) is within "
            "~0.75 deg of a sign boundary. Given the approximations used "
            "here (especially for Mars and the Ascendant), treat this "
            "result as uncertain and verify against proper software or a "
            "professional astrologer."
        )


if __name__ == "__main__":
    main()
