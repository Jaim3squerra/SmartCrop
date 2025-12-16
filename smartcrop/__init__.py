"""SmartCrop package

Módulos principales:
- sensor: lectura y abstracción del DHT11/DHT22
- controller: control de relés mediante RPi.GPIO
"""
from importlib.metadata import version, PackageNotFoundError

from .sensor import DHTSensor
from .controller import RelayController

__all__ = ["DHTSensor", "RelayController", "__version__"]

try:
	__version__ = version("smartcrop")
except PackageNotFoundError:  # package not installed
	__version__ = "0.0.0"
