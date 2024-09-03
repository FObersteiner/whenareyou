from whenareyou.whenareyou import whenareyou, whenareyou_IATA


def get_version():
    try:
        # Py 3.8+
        from importlib import metadata

        return metadata.version("whenareyou")
    except ImportError:
        # Py <= 3.7
        import pkg_resources

        return pkg_resources.get_distribution("whenareyou").version


__version__ = get_version()

del get_version  # this should not be exported

__all__ = ("whenareyou", "whenareyou_IATA")
