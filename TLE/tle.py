from skyfield.api import load

# load the TLE filess
def load_tle():
    url = 'https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=starlink&FORMAT=tle'
    global sats
    sats = load.tle_file(url)
    break_point = 0
    return sats


sats = []
load_tle()
