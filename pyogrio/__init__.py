from pyogrio.core import (
    list_drivers,
    list_layers,
    read_bounds,
    read_info,
    set_gdal_config_options,
    get_gdal_config_option,
    get_gdal_data_path,
    __gdal_version__,
    __gdal_version_string__,
    __gdal_geos_version__,
)
from pyogrio.geopandas import read_dataframe, write_dataframe
from pyogrio._version import get_versions


__version__ = get_versions()["version"]
del get_versions

__all__ = [
    "list_drivers",
    "list_layers",
    "read_bounds",
    "read_info",
    "set_gdal_config_options",
    "get_gdal_config_option",
    "get_gdal_data_path",
    "read_dataframe",
    "write_dataframe",
    "__gdal_version__",
    "__gdal_version_string__",
    "__gdal_geos_version__",
    "__version__",
]
