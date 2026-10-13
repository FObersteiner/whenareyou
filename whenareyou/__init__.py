from importlib import metadata

from whenareyou.whenareyou import whenareyou, whenareyou_IATA


def get_version():
    return metadata.version("whenareyou")


__version__ = get_version()

del get_version  # this should not be exported

__all__ = ("whenareyou", "whenareyou_IATA")
