__version__ = "0.0.1"

from typing import Union

JSON = Union[None, bool, dict[str, "JSON"], float, int, list["JSON"], str]
