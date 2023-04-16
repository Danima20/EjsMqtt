"""

@author: Daniel Martinez
"""

from paho.mqtt.client import Client
import sys
# Función para procesar los números recibidos
def process_num(numbers):
    # Separar los enteros y reales
    ints = []
    floats = []
    for num in numbers:
        if isinstance(num, int):
            ints.append(num)
        elif isinstance(num, float):
            floats.append(num)
    
    # Calcular la frecuencia de cada tipo de número
    freq_ints = {}
    freq_floats = {}
    for num in ints:
        freq_ints[num] += 1
    for num in floats:
        freq_floats[num] += 1
    
    # Imprimir resultados
    print("Enteros:", ints)
    print("Reales:", floats)
    print("Frecuencia de enteros:", freq_ints)
    print("Frecuencia de reales:", freq_floats)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        num = int(payload)
    except ValueError:
        try:
            num = float(payload)
        except ValueError:
            print("Error: el payload no es un número válido")
            return
    process_num([num])

def main(hostname):
    client = Client()
    client.on_message = on_message
    client.connect(hostname)
    client.subscribe("numbers")
    client.loop_forever()

if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)
