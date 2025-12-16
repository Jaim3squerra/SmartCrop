
#!/usr/bin/env python3
"""
pruebas_reles.py

Script simple para probar 3 salidas GPIO en una Raspberry Pi 4.
Activa un relé a la vez durante 5 segundos (por defecto) y pasa al siguiente
en un bucle infinito. Maneja Ctrl+C y limpia los GPIO al salir.

Uso:
  sudo python3 pruebas_reles.py
Opciones:
  --pins  Lista de pines BCM separados por comas (ej: 17,27,22)
  --delay Segundos que se mantiene cada relé activo (default: 5)
  --active-low Indica que los relés se activan con nivel bajo (opcional)
  --once  Ejecuta una sola pasada y sale (opcional)
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import List

import RPi.GPIO as GPIO  # type: ignore


def parse_args(argv: List[str]) -> argparse.Namespace:
	p = argparse.ArgumentParser(description="Probar 3 relés en secuencia")
	p.add_argument("--pins", default="17,27,22",
				   help="Pines BCM separados por coma (default: 17,27,22)")
	p.add_argument("--delay", type=float, default=5.0,
				   help="Segundos por relé (default: 5)")
	p.add_argument("--active-low", action="store_true",
				   help="Si se usa, los relés se activan con nivel LOW")
	p.add_argument("--once", action="store_true",
				   help="Ejecuta una pasada y sale")
	return p.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
	args = parse_args(sys.argv[1:] if argv is None else argv)

	pins = [int(x.strip()) for x in args.pins.split(",") if x.strip()]
	delay = float(args.delay)
	active_low = bool(args.active_low)

	# Mapear valores de activación
	ACTIVE = GPIO.LOW if active_low else GPIO.HIGH
	INACTIVE = GPIO.HIGH if active_low else GPIO.LOW

	# Inicializar GPIO
	GPIO.setmode(GPIO.BCM)
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT, initial=INACTIVE)

	print(f"Secuencia iniciada en pines {pins} con delay={delay}s (active_low={active_low})")

	try:
		while True:
			for pin in pins:
				print(f"Activando pin {pin}")
				GPIO.output(pin, ACTIVE)
				time.sleep(delay)
				GPIO.output(pin, INACTIVE)
				print(f"Desactivado pin {pin}")
			if args.once:
				print("Ejecución única completada. Saliendo.")
				return 0
	except KeyboardInterrupt:
		print("Interrumpido por usuario (Ctrl+C)")
	finally:
		GPIO.cleanup()
		print("GPIO limpiados, chau")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())

