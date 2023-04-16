# -*- coding: utf-8 -*-
"""
@author: Daniel Martinez
"""
from paho.mqtt.client import Client
import sys
import time


global temperature_values
temperature_values = {}

def on_connect(mqttc, userdata, flags, rc):
    print("CONNECT:", userdata, flags, rc)

def on_message(mqttc, userdata, msg):
    global temperature_values
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain)
    if msg.topic.startswith("temperature/"):
        sensor_id = msg.topic.split("/")[1]
        temperature = float(msg.payload)
        if sensor_id not in temperature_values:
            temperature_values[sensor_id] = []
        temperature_values[sensor_id].append(temperature)

def on_publish(mqttc, userdata, mid):
    print("PUBLISH:", userdata, mid)

def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("SUBSCRIBED:", userdata, mid, granted_qos)

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def calculo_temp():
    global temperature_values
    all_temperatures = []
    for sensor_id, temperatures in temperature_values.items():
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        avg_temp = sum(temperatures) / len(temperatures)
        print(f"Sensor {sensor_id}: Max={max_temp:.2f}, Min={min_temp:.2f}, Avg={avg_temp:.2f}")
        all_temperatures.extend(temperatures)
    max_all = max(all_temperatures)
    min_all = min(all_temperatures)
    avg_all = sum(all_temperatures) / len(all_temperatures)
    print(f"All Sensors: Max={max_all:.2f}, Min={min_all:.2f}, Avg={avg_all:.2f}")

def main(hostname):
    mqttc = Client(userdata="data (of any type) for user")
    mqttc.enable_logger()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    mqttc.connect(hostname)

    mqttc.subscribe('temperature/#')

    while True:
        mqttc.loop()
        #Hagamos que la funcion se ejecute cada 8 segundos
        time.sleep(8)
        calculo_temp()

if __name__ == '__main__':
    hostname = 'localhost'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)