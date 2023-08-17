# whenareyou

Gets the time zone name of any location in the world. Unless [nominatim](https://nominatim.openstreetmap.org/ui/search.html) doesn't know it ;-)

This fork is a (heavily) modified version of @sils [whenareyou](https://github.com/aerupt/whenareyou). Uses `nominatim.openstreetmap.org` to search the location. It caches the results so that the server isn't stressed by repeated queries of the same address.

## example usage

```Python
from whenareyou import whenareyou

tz = whenareyou('Hamburg')

tz
Out[1]: 'Europe/Berlin'

from datetime import datetime
from zoneinfo import ZoneInfo # Python 3.9+

datetime(2002, 10, 27, 6, 0, 0, tzinfo=ZoneInfo(tz)).isoformat()
Out[2]: '2002-10-27T06:00:00+01:00'
```

Lookup of IATA airport codes (3-letter) is also included:

```Python
from whenareyou import whenareyou_IATA

whenareyou_IATA('PVG') # Shanghai Pudong
Out[3]: 'Asia/Shanghai'
```

### requires

- v0.4 required Python 3.9+ (zoneinfo module)
- v0.5 API change: zoneinfo no longer required, should work well with older versions of Python
- [requests](https://pypi.org/project/requests/), [timezonefinder](https://pypi.org/project/timezonefinder/)
