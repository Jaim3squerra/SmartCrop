"""Módulo de acceso al sensor DHT11/DHT22.

Proporciona una clase `DHTSensor` que abstrae la librería `adafruit_dht` y ofrece
un método `read()` que devuelve (temperature_c, humidity) o lanza RuntimeError si falla.
"""

from __future__ import annotations

import time
from typing import Optional, Tuple

import board
import adafruit_dht


class DHTSensor:
    """Lector de sensor DHT11 / DHT22.

    Parámetros:
    - pin: objeto de `board` (ej. board.D4). Por defecto `board.D4`.
    - sensor_type: 'DHT11' o 'DHT22'
    - retry_delay: segundos a esperar antes de reintento en lecturas fallidas
    """

    def __init__(self, pin=board.D4, sensor_type: str = "DHT11", retry_delay: float = 2.0):
        self.pin = pin
        self.retry_delay = float(retry_delay)
        sensor_type = sensor_type.upper()
        if sensor_type == "DHT11":
            self._device = adafruit_dht.DHT11(pin)
        elif sensor_type == "DHT22":
            self._device = adafruit_dht.DHT22(pin)
        else:
            raise ValueError("sensor_type must be 'DHT11' or 'DHT22'")

    def read(self) -> Tuple[Optional[float], Optional[float]]:
        """Lee temperatura (°C) y humedad (%) del sensor.

        Devuelve (temperature_c, humidity). Si la lectura falla por un error
        recuperable, lanza RuntimeError para que el llamador pueda decidir
        reintentar.
        """
        try:
            temperature_c = self._device.temperature
            humidity = self._device.humidity
            return temperature_c, humidity
        except RuntimeError as exc:
            # Errores esperables por lecturas: reintentar con backoff en caller
            raise RuntimeError(f"Lectura DHT fallida: {exc}") from exc
        except Exception as exc:
            # Errores inesperados: asegurar que se cierra el dispositivo
            try:
                self._device.exit()
            except Exception:
                pass
            raise

    def exit(self) -> None:
        """Cierra el objeto del sensor (libera recursos)."""
        try:
            self._device.exit()
        except Exception:
            pass
