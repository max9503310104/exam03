import serial
import time
import matplotlib.pyplot as plt
import paho.mqtt.client as paho

serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

mqttc = paho.Client()
host = "192.168.244.128"
topic = "velocity"

def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)


print("start sending RPC")
i = 50
while i > 0:
    i = i - 1
    s.write("/acc/run\r".encode())
    char = s.read(5)
    print(char)
    mqttc.publish(topic, char, qos=0)
    time.sleep(1)
    
    



s.close()