"""
@author: Daniel Martinez
"""

import paho.mqtt.client as mqtt
import json
import time
import sys

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("numbers")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print(f"Received message: {payload}")
    
    # Obtener los campos del mensaje
    delay = payload.get("delay", 0)
    topic = payload.get("topic", "")
    message = payload.get("message", "")

    # Esperar el tiempo de retardo
    time.sleep(delay)

    # Publicar el mensaje en el topic correspondiente
    client.publish(topic, message)
    print(f"Published message in topic {topic}: {message}")

def main(hostname):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()
    
    
if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)
    