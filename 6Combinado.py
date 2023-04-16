"""

@author: Daniel Martinez
"""

from paho.mqtt.client import Client
from time import sleep
import sys

# Cliente 1: Escucha en el topic "numbers" y activa la alarma si recibe un entero múltiplo de 5
def on_message_numbers(mqttc, userdata, msg):
    if float(msg.payload).is_integer() and int(msg.payload) % 5 == 0:
        print(f"Alarma activada para {msg.payload} segundos")
        mqttc.publish("timer", f"{msg.payload};temp1;Alarma activada")

# Cliente 2: Espera el tiempo de la alarma y publica un mensaje en el topic "temp1"
def on_message_timer(mqttc, userdata, msg):
    data = msg.payload.decode().split(';')
    if len(data) == 3:
        sleep(int(data[0]))
        mqttc.publish(data[1], data[2])

# Cliente 3: Se suscribe al topic "temp1" y, si el valor máximo es mayor que 40, se suscribe a "humidity"
def on_message_temp1(mqttc, userdata, msg):
    values = [float(x) for x in msg.payload.decode().split(',')]
    max_value = max(values)
    print(f"Valor máximo de temp1: {max_value}")
    if max_value > 40:
        print("Suscribiéndose a humidity")
        mqttc.subscribe("humidity")
    else:
        print("Dejando de suscribirse a humidity")
        mqttc.unsubscribe("humidity")

def main(hostname):
    # Cliente 1: Escucha en "numbers"
    client_numbers = Client()
    client_numbers.on_message = on_message_numbers
    client_numbers.connect(hostname)
    client_numbers.subscribe("numbers")
    client_numbers.loop_start()

    # Cliente 2: Escucha en "timer"
    client_timer = Client()
    client_timer.on_message = on_message_timer
    client_timer.connect(hostname)
    client_timer.subscribe("timer")
    client_timer.loop_start()

    # Cliente 3: Escucha en "temp1" y, si es necesario, en "humidity"
    client_temp1 = Client()
    client_temp1.on_message = on_message_temp1
    client_temp1.connect(hostname)
    client_temp1.subscribe("temp1")
    client_temp1.loop_forever()

if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)