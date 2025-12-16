# SmartCrop

Proyecto para monitorizar temperatura con DHT11/DHT22 y activar un relé (GPIO) cuando se superen ciertos umbrales.

Estructura propuesta:

- `smartcrop/` - paquete principal con módulos `sensor` y `controller`.
- `scripts/monitor.py` - script CLI para ejecutar el monitor
- `tests/` - pruebas unitarias con mocks
- `requirements.txt` - dependencias para la Raspberry Pi

Uso (ejemplo):

```bash
sudo python3 scripts/monitor.py --sensor-pin D4 --sensor-type DHT11 --relay-pin 17 --threshold 30.0
```

Notas:
- `scripts/monitor.py` usa `board` para identificar el pin del sensor (ej. `D4`) y BCM para el relé (ej. `17`).
- Asegúrate de instalar `adafruit-circuitpython-dht` y que `RPi.GPIO` esté disponible en tu sistema.

Contribuciones: abrir issues o PRs con mejoras.
