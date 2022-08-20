# python 3.6

import random
import time

from datetime import datetime
from faker import Faker

from paho.mqtt import client as mqtt_client

fake = Faker()
broker = 'localhost'
port = 1883
topic = "iot_center"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(2)
        #msg = f"messages: {msg_count}"
        Temperature = random.randint(3, 40)
        Lat, Lon = fake.latlng()
        CO2 = random.randint(123, 2000)
        Pressure = random.randint(123, 2000)
        TVOC = random.randint(123, 2000)
        Humidity = random.randint(1, 100)
        speed_a = random.randint(1, 100)
        speed_b = random.randint(1, 100)
        Distance = random.randint(1, 200)
        x_axis = random.randint(1, 180)
        y_axis = random.randint(1, 180)
        z_axis = random.randint(1, 180)
        current_time = int(time.time())
        msg = f"environment,CO2Sensor=virtual_CO2Sensor,GPSSensor=virtual_GPSSensor,HumiditySensor=virtual_HumiditySensor,PressureSensor=virtual_PressureSensor,TVOCSensor=virtual_TVOCSensor,TemperatureSensor=virtual_TemperatureSensor,speed_a={speed_a},speed_b={speed_b},distance={Distance},x_axis={x_axis},y_axis={y_axis},z_axis={z_axis},clientId=robot_mac CO2={CO2}i,Humidity={Humidity},Lat={Lat},Lon={Lon},Pressure={Pressure},TVOC={TVOC}i,Temperature={Temperature} {current_time}"
        #msg = f"environment,clientId=robot_mac CO2Sensor=virtual_CO2Sensor,GPSSensor=virtual_GPSSensor,HumiditySensor=virtual_HumiditySensor,PressureSensor=virtual_PressureSensor,TVOCSensor=virtual_TVOCSensor,TemperatureSensor=virtual_TemperatureSensor,speed_a={speed_a},speed_b={speed_b},distance={Distance},x_axis={x_axis},y_axis={y_axis},z_axis={z_axis},CO2={CO2}i,Humidity={Humidity},Lat={Lat},Lon={Lon},Pressure={Pressure},TVOC={TVOC}i,Temperature={Temperature}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        print("")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()