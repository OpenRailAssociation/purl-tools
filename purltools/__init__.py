"""Initialise importable functions"""

from importlib.metadata import version

from .purl2cd import purl2clearlydefined
from .url_purl import convert_purl2url, convert_url2purl

__version__ = version("purl-tools")
