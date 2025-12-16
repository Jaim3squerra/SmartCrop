#!/usr/bin/env python3
"""Monitor de temperatura que activa un relé cuando supera un umbral.

Ejemplo:
  sudo python3 scripts/monitor.py --sensor-pin D4 --sensor-type DHT11 --relay-pin 17 --threshold 30.0

Requisitos: correr en Raspberry Pi con `adafruit-circuitpython-dht` y `RPi.GPIO`.
"""

from __future__ import annotations

import argparse
import logging
import signal
import sys
import time
from typing import Optional

import board

from smartcrop.sensor import DHTSensor
from smartcrop.controller import RelayController


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Monitor de temperatura y relé")
    p.add_argument("--sensor-pin", default="D4",
                   help="Pin del sensor (board name), ejemplo: D4 or D17")
    p.add_argument("--sensor-type", default="DHT11", choices=["DHT11", "DHT22"],
                   help="Tipo de sensor")
    p.add_argument("--relay-pin", type=int, default=17, help="Pin BCM del relé (default: 17)")
    p.add_argument("--threshold", type=float, default=30.0, help="Umbral en °C para activar relé")
    p.add_argument("--interval", type=float, default=2.0, help="Segundos entre lecturas (default: 2)")
    p.add_argument("--active-low", action="store_true", help="Indica que el relé se activa con nivel LOW")
    return p.parse_args(argv)


def _resolve_board_pin(name: str):
    # Convierte un nombre como 'D4' en board.D4
    try:
        return getattr(board, name)
    except AttributeError:
        raise ValueError(f"Pin de placa desconocido: {name}")


def main(argv=None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    sensor_pin = _resolve_board_pin(args.sensor_pin)

    sensor = DHTSensor(pin=sensor_pin, sensor_type=args.sensor_type)
    relay = RelayController(pin=args.relay_pin, active_low=args.active_low)

    # Estado del relé (True = on, False = off)
    relay_on = False

    # Manejo de salida limpia con señales
    stop = False

    def _signal_handler(signum, frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    logging.info("Monitor iniciado: threshold=%.1f°C, relay_pin=%d", args.threshold, args.relay_pin)

    try:
        while not stop:
            try:
                temperature, humidity = sensor.read()
            except RuntimeError as exc:
                logging.warning("Lectura fallida del sensor: %s", exc)
                time.sleep(args.interval)
                continue

            if temperature is None:
                logging.warning("Temperatura nula en lectura; saltando ciclo")
                time.sleep(args.interval)
                continue

            logging.info("Temperatura: %.1f°C Humedad: %s%%", temperature, humidity if humidity is not None else "?")

            if temperature > args.threshold and not relay_on:
                logging.info("Temperatura > %.1f°C -> activando relé", args.threshold)
                relay.on()
                relay_on = True
            elif temperature <= args.threshold and relay_on:
                logging.info("Temperatura <= %.1f°C -> desactivando relé", args.threshold)
                relay.off()
                relay_on = False

            time.sleep(args.interval)

    except Exception as exc:
        logging.exception("Error inesperado en el monitor: %s", exc)
        # Intentar apagar el relé si está activado
        try:
            if relay_on:
                relay.off()
        except Exception:
            pass
        raise
    finally:
        try:
            if relay_on:
                relay.off()
        finally:
            relay.cleanup()
            sensor.exit()
            logging.info("Monitor detenido y recursos liberados")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
