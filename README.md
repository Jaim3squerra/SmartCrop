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

Instalación (editable) y despliegue en Raspberry Pi
--------------------------------------------------

1. Subir a GitHub (desde tu máquina de desarrollo):

	git add .
	git commit -m "Add packaging and installation files"
	git push origin main

2. En la Raspberry Pi clonar e instalar en modo editable:

	git clone https://github.com/Jaim3squerra/SmartCrop.git
	cd SmartCrop
	# Instalar dependencias del sistema si falta (ejemplo):
	sudo apt update && sudo apt install -y python3-pip python3-dev build-essential libgpiod-dev
	# Instalar las dependencias Python y registrar el paquete en editable
	python3 -m pip install -e .

3. Ejecutar el monitor (con permisos si se necesitan):

	sudo smartcrop-monitor --sensor-pin D4 --sensor-type DHT11 --relay-pin 17 --threshold 30.0

Notas:
- `pip install -e .` instala el paquete en modo editable: los cambios en el código fuente se reflejan sin reinstalar. Esto es ideal durante desarrollo y útil para desplegar rápidamente en la Raspberry Pi.
- Para un entorno de producción más estricto: considerar crear un release en GitHub, usar versiones semver y desplegar con `pip install` de la release o usar contenedores/paquetes `.deb` o un servicio systemd que invoque el binario instalado.

Ejemplo de servicio systemd (opcional)
------------------------------------

Se incluye un ejemplo de unidad systemd en `contrib/smartcrop.service`. Para instalarlo en la Raspberry Pi:

	sudo cp contrib/smartcrop.service /etc/systemd/system/smartcrop.service
	sudo systemctl daemon-reload
	sudo systemctl enable --now smartcrop.service

Revisar logs con `journalctl -u smartcrop.service -f`.
