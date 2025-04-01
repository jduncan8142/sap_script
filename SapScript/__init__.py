from __future__ import annotations

from Core.sap import SAP  # noqa: F401
from .Gui.vkeys import VKeys  # noqa: F401
from .Utils.systems import Systems  # noqa: F401
import sys

#: The release version
version = "0.0.1"
__version__ = version

MIN_PYTHON_VERSION = 3, 13
MIN_PYTHON_VERSION_STR = ".".join([str(v) for v in MIN_PYTHON_VERSION])

if sys.version_info < MIN_PYTHON_VERSION:
    msg = f"sap_script {version} requires Python {MIN_PYTHON_VERSION_STR} or newer."
    raise Exception(msg)
