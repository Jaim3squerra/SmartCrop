import time
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Inicializar SPI
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)

# Crear objeto MCP3008
mcp = MCP3008(spi, cs)

# Canal donde está conectado el MQ135 (CH1)
mq = AnalogIn(mcp, MCP3008.P1)

print("=== Lectura MQ135 (MCP3008) ===")
print("Presiona Ctrl+C para salir.\n")

while True:
    raw = mq.value          # 0–65535
    voltage = mq.voltage    # voltaje real

    print(f"Raw: {raw} | Voltaje: {voltage:.3f} V")

    # Si quieres, puedes agregar una estimación simple:
    # calidad = "Buena" si voltage < 1.0 else "Mala"
    # print(f"Calidad del aire: {calidad}")

    time.sleep(1)
