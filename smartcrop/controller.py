"""Módulo de control de relés/GPIO.

Provee la clase `RelayController` para manejar un relé conectado a un pin
BCM (por ejemplo GPIO17). Maneja `active_low` si el relé se activa con nivel
bajo.
"""

from __future__ import annotations

from typing import Optional

import RPi.GPIO as GPIO  # type: ignore


class RelayController:
    """Controla un relé en un pin BCM específico.

    Parámetros:
    - pin: número BCM (ej. 17)
    - active_low: True si el relé se activa con nivel LOW
    """

    def __init__(self, pin: int = 17, active_low: bool = False) -> None:
        self.pin = int(pin)
        self.active_low = bool(active_low)
        self._setup_gpio()
        # Asegurar estado apagado al iniciar
        self.off()

    def _setup_gpio(self) -> None:
        GPIO.setmode(GPIO.BCM)
        # Seguir la convención de `pruebas_reles.py`:
        # - si active_low == False: ACTIVE = HIGH, INACTIVE = LOW
        # - si active_low == True:  ACTIVE = LOW,  INACTIVE = HIGH
        inactive = GPIO.LOW if not self.active_low else GPIO.HIGH
        GPIO.setup(self.pin, GPIO.OUT, initial=inactive)

    def on(self) -> None:
        level = GPIO.LOW if self.active_low else GPIO.HIGH
        GPIO.output(self.pin, level)

    def off(self) -> None:
        level = GPIO.HIGH if self.active_low else GPIO.LOW
        GPIO.output(self.pin, level)

    def cleanup(self) -> None:
        GPIO.cleanup(self.pin)

    def __enter__(self) -> "RelayController":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.off()
        finally:
            self.cleanup()
