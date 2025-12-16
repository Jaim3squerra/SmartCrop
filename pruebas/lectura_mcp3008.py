import time
import json
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

CAL_FILE = "calibracion.json"

# -----------------------------
#  Cargar o crear calibración
# -----------------------------
def cargar_calibracion():
    try:
        with open(CAL_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"pH4": None, "pH7": None, "pH10": None}

def guardar_calibracion(data):
    with open(CAL_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Calibración guardada.")

# -----------------------------
#  Calcular pH desde voltaje
# -----------------------------
def calcular_ph(voltage, cal):
    if None in cal.values():
        return None  # No calibrado

    # Ajuste lineal usando pH 4 y pH 7
    m = (7 - 4) / (cal["pH7"] - cal["pH4"])
    b = 7 - m * cal["pH7"]

    return m * voltage + b

# -----------------------------
#  Inicializar MCP3008
# -----------------------------
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP3008(spi, cs)
canal = AnalogIn(mcp, MCP3008.P0)

# -----------------------------
#  Modo calibración
# -----------------------------
def modo_calibracion():
    cal = cargar_calibracion()

    print("\n=== MODO CALIBRACIÓN ===")
    print("Coloca el electrodo en solución pH 4 y presiona Enter.")
    input()
    cal["pH4"] = canal.voltage
    print(f"Registrado pH4 = {cal['pH4']:.3f} V")

    print("\nColoca el electrodo en solución pH 7 y presiona Enter.")
    input()
    cal["pH7"] = canal.voltage
    print(f"Registrado pH7 = {cal['pH7']:.3f} V")

    print("\nColoca el electrodo en solución pH 10 y presiona Enter.")
    input()
    cal["pH10"] = canal.voltage
    print(f"Registrado pH10 = {cal['pH10']:.3f} V")

    guardar_calibracion(cal)
    print("\nCalibración completa.")

# -----------------------------
#  Modo lectura continua
# -----------------------------
def modo_lectura():
    cal = cargar_calibracion()

    print("\n=== LECTURA CONTINUA ===")
    print("Presiona Ctrl+C para salir.\n")

    while True:
        voltage = canal.voltage
        ph = calcular_ph(voltage, cal)

        if ph is None:
            print(f"Voltaje: {voltage:.3f} V | pH: (sin calibrar)")
        else:
            print(f"Voltaje: {voltage:.3f} V | pH estimado: {ph:.2f}")

        time.sleep(1)

# -----------------------------
#  Menú principal
# -----------------------------
def main():
    print("=== Medidor de pH con MCP3008 ===")
    print("1) Calibrar")
    print("2) Leer en tiempo real")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        modo_calibracion()
    else:
        modo_lectura()

if __name__ == "__main__":
    main()