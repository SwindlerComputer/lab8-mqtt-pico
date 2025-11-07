# publisher_pico.py
# Nelson Ude C20479276 | Mateusz Matijuk C21473436 | Luca Ursache C21392706

import network
import time
import machine
from umqtt.simple import MQTTClient

# --- Wi-Fi Setup ---
ssid = "Emeka Ude"
password = "Internet2002"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)
print("Connected to Wi-Fi!")
print("Network config:", wlan.ifconfig())

# --- MQTT Broker Setup ---
broker = "172.20.10.8"  
client_id = "pico_publisher"
topic = b"temp/pico"

try:
    mqtt = MQTTClient(client_id, broker)
    mqtt.connect()
    print("Connected to MQTT broker at", broker)
except Exception as e:
    print("Failed to connect to MQTT broker:", e)
    while True:
        time.sleep(1)

# --- Onboard Temperature Sensor ---
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / 65535

def read_temp():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return round(temperature, 2)

# --- Main Loop ---
while True:
    try:
        temp = read_temp()
        print("Publishing temperature:", temp)
        mqtt.publish(topic, str(temp))
        time.sleep(2)
    except OSError as e:
        print("Error publishing:", e)
        # Attempt reconnection if MQTT drops
        try:
            mqtt.connect()
            print("Reconnected to broker.")
        except Exception as err:
            print("Reconnection failed:", err)
            time.sleep(5)

