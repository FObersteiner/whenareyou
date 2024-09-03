import json
import os
from functools import lru_cache
from typing import Optional
from urllib.parse import quote
from urllib.request import urlopen

from timezonefinder import TimezoneFinder

# -----------------------------------------------------------------------------
# use openstreetmap
# -----------------------------------------------------------------------------
_LONG_LAT_URL_Nominatim = "https://nominatim.openstreetmap.org/search?q="

# -----------------------------------------------------------------------------
# IATA codes
# -----------------------------------------------------------------------------
with open(os.path.join(os.path.dirname(__file__), "airports.csv"), encoding="utf-8") as csvfile:
    data = csvfile.read().splitlines()

parsed = []
for line in data:
    parsed.append(line.split(","))

_airports_dict = {item[0]: list(item[1:]) for item in zip(*parsed)}

# -----------------------------------------------------------------------------


# HELPERS ---------------------------------------------------------------------
@lru_cache(maxsize=None)
def _cached_get(url: str) -> Optional[str]:
    """
    a general helper -
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    with urlopen(url) as response:
        body = response.read()
    return body


def _queryOSM(address: str) -> list[Optional[float]]:
    """
    a helper to query nominatim.openstreetmap for given address
    """
    url = f"{_LONG_LAT_URL_Nominatim}{quote(address)}&format=json&polygon=0"
    response = _cached_get(url)

    # invalid response (403) gives an empty string here
    if not response:
        raise ValueError(f"Invalid response for address '{address}'")

    response_json = json.loads(response)

    # response might be ok (200) but contains no data...
    if not response_json:
        raise ValueError(f"Invalid response for address '{address}'")

    return [float(response_json[0].get(key)) for key in ("lat", "lon")]


def _get_tz(lat: float, lng: float, _tf=TimezoneFinder()) -> Optional[str]:
    """
    a helper to call timezonefinder.
    returns IANA time zone name of given lat/long coordinates
    """
    tzname = _tf.timezone_at(lng=lng, lat=lat)
    if tzname:
        return tzname
    return None


# MAIN METHODS ----------------------------------------------------------------
def whenareyou(address: str) -> Optional[str]:
    """
    Find the time zone of a given address

    Parameters
    ----------
    address : str
        address to search.

    Returns
    -------
    tzname : str
        IANA time zone name

    """
    # adding "geolocator" kwarg would allow to select geolocating service,
    # i.e. the "geolocator" keyword would select a function like _queryOSM
    return _get_tz(*_queryOSM(address))  # type: ignore


def whenareyou_IATA(airport: str) -> Optional[str]:
    """
    Find the time zone of a given airport IATA code

    Parameters
    ----------
    airport : str
        airport IATA code.

    Returns
    -------
    tzname : str
        IANA time zone name

    """
    airport = airport.upper().strip()
    iatacodes = _airports_dict["iata_code"]
    ix = iatacodes.index(airport) if airport in iatacodes else None

    if not ix:
        raise ValueError(f"IATA code not found: '{airport}'")

    tzname = _get_tz(
        float(_airports_dict["latitude_deg"][ix]),
        float(_airports_dict["longitude_deg"][ix]),
    )
    return tzname
