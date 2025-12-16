#!/usr/bin/env python3
"""
lectura_sensor.py

Lee un sensor DHT11 o DHT22 conectado al pin GPIO4 (board.D4) y muestra
la temperatura (°C) y la humedad (%) en consola cada 2 segundos.

Requisitos / instalación (ejecutar en la Raspberry Pi):
  sudo apt update
  sudo apt install -y python3-pip python3-dev build-essential libgpiod-dev
  sudo pip3 install adafruit-blinka adafruit-circuitpython-dht

Conexiones típicas (ver documentación del sensor):
  - Data -> GPIO4 (pin físico 7)
  - VCC  -> 3.3V o 5V según el módulo
  - GND  -> GND

Notas:
  - Ejecuta el script con sudo si no tienes permisos para GPIO.
  - El script reintenta lecturas fallidas y maneja Ctrl+C limpiamente.
"""

import sys
import time
import board
import adafruit_dht


# Inicializar el objeto del sensor DHT11 en el pin GPIO4 (board.D4)
# Si deseas usar otro pin, cámbialo aquí (por ejemplo, board.D17).
dhtDevice = adafruit_dht.DHT11(board.D4)


def main() -> int:
    """Bucle principal de lectura del sensor.

    - Intenta leer temperatura y humedad.
    - Si falla por problemas temporales (RuntimeError), muestra un mensaje
      en español y reintenta tras 2 segundos.
    - Si hay un error inesperado se cierra el dispositivo y se propaga
      la excepción para facilitar el diagnóstico.
    - Ctrl+C detiene el bucle y cierra el dispositivo sin mostrar traza.
    """

    try:
        while True:
            try:
                # Obtener lecturas del sensor
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity
                print(f"Temperatura: {temperature_c:.1f}°C - Humedad: {humidity:.1f}%")
            except RuntimeError as error:
                # Errores esperables por lecturas fallidas; reintentamos
                print(f"No se pudo leer el sensor. Reintentando en 2 s. (Detalle: {error})")
                time.sleep(2.0)
                continue
            except Exception as error:
                # Error inesperado: cerrar el sensor y propagar la excepción
                print("Error inesperado leyendo el sensor. Cerrando el dispositivo.")
                dhtDevice.exit()
                raise

            # Esperar antes de la siguiente lectura
            time.sleep(2.0)

    except KeyboardInterrupt:
        # Manejo limpio de Ctrl+C: no mostrar traza de excepción
        print("\nInterrumpido por el usuario. Cerrando el sensor y saliendo...")
        try:
            dhtDevice.exit()
        except Exception:
            # Ignorar errores al cerrar para evitar mensajes innecesarios
            pass
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

