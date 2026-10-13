import csv
import json
import os
from functools import cache
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from timezonefinder import TimezoneFinder

# -----------------------------------------------------------------------------
# use openstreetmap
# -----------------------------------------------------------------------------
_LONG_LAT_URL_Nominatim = "https://nominatim.openstreetmap.org/search?q="
_TIMEOUT = 10  # seconds to wait for a response from nominatim


# -----------------------------------------------------------------------------
# IATA codes
# -----------------------------------------------------------------------------
def _load_airports() -> dict[str, tuple[float, float]]:
    """
    parse the bundled airports.csv into a mapping of IATA code -> (lat, lon)
    """
    path = os.path.join(os.path.dirname(__file__), "airports.csv")
    airports: dict[str, tuple[float, float]] = {}
    with open(path, encoding="utf-8", newline="") as csvfile:
        for row in csv.DictReader(csvfile):
            code = row["iata_code"].strip()
            if not code:
                continue
            # keep the first entry for duplicate codes
            airports.setdefault(code, (float(row["latitude_deg"]), float(row["longitude_deg"])))
    return airports


_airports = _load_airports()

# -----------------------------------------------------------------------------


# HELPERS ---------------------------------------------------------------------
@cache
def _cached_get(url: str) -> bytes:
    """
    a general helper -
    Makes a get to that URL and caches the raw response body.
    """
    request = Request(url, headers={"User-Agent": "whenareyou python package"})
    with urlopen(request, timeout=_TIMEOUT) as response:
        body = response.read()
    return body


@cache
def _timezone_finder() -> TimezoneFinder:
    """
    a helper to get a shared TimezoneFinder instance
    (constructing it is expensive, so it is only built once)
    """
    return TimezoneFinder()


def _queryOSM(address: str) -> tuple[float, float]:
    """
    a helper to query nominatim.openstreetmap for given address
    """
    url = f"{_LONG_LAT_URL_Nominatim}{quote(address, safe='')}&format=json&polygon=0"
    try:
        response_json = json.loads(_cached_get(url))
    except (HTTPError, URLError, TimeoutError, ValueError) as e:
        raise ValueError(f"Invalid response for address '{address}'") from e

    # response might be ok (200) but contains no data...
    if not response_json:
        raise ValueError(f"Invalid response for address '{address}'")

    try:
        return (float(response_json[0]["lat"]), float(response_json[0]["lon"]))
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(f"Invalid response for address '{address}'") from e


def _get_tz(lat: float, lng: float, _tf: TimezoneFinder) -> str | None:
    """
    a helper to call timezonefinder.
    returns IANA time zone name of given lat/long coordinates
    """
    tzname = _tf.timezone_at(lng=lng, lat=lat)
    if tzname:
        return tzname
    return None


# MAIN METHODS ----------------------------------------------------------------
def whenareyou(address: str) -> str | None:
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
    return _get_tz(*_queryOSM(address), _timezone_finder())


def whenareyou_IATA(airport: str) -> str | None:
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
    coords = _airports.get(airport)
    if coords is None:
        raise ValueError(f"IATA code not found: '{airport}'")

    return _get_tz(*coords, _timezone_finder())
