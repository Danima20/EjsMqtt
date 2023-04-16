# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:29:49 2023

@author: danie
"""
from paho.mqtt.client import Client
import sys


def on_connect(mqttc, userdata, flags, rc):
    print("CONNECT:", userdata, flags, rc)

def on_message(mqttc, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain)
    global sub_humed
    global lim_temp

    # Mirar si es de temperatura
    if msg.topic == 'temperature/t1':
        temperature = float(msg.payload)
        if temperature > lim_temp and not  sub_humed:
            mqttc.subscribe('humidity/#')
            sub_humed = True
            print('Subscrito en el topic humedad')
        elif temperature <= lim_temp and  sub_humed:
            mqttc.unsubscribe('humidity/#')
            sub_humed = False
            print('Desubscrito del topic humedad')

    # Mirar si es del canal de humedad
    elif  sub_humed and msg.topic.startswith('humidity/'):
        humidity = float(msg.payload)
        if humidity > lim_humed:
            mqttc.unsubscribe('humidity/#')
            sub_humed = False
            print('Desubscrito del topic humedad')

def on_publish(mqttc, userdata, mid):
    print("PUBLISH:", userdata, mid)

def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("SUBSCRIBED:", userdata, mid, granted_qos)

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)


def main(hostname):
    global sub_humed
    global lim_temp
    global lim_humed
    sub_humed = False
    lim_temp = 30  # Limite temperatura K0 
    lim_humed = 60 #Limite humedad k1

    mqttc = Client(userdata="data (of any type) for user")
    mqttc.enable_logger()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    mqttc.connect(hostname)

    mqttc.subscribe('temperature/#')

    mqttc.loop_forever()


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)
