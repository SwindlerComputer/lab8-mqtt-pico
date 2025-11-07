# subscriber_pico.py
# Nelson Ude C20479276 | Mateusz Matijuk C21473436 | Luca Ursache C21392706
import network, time, machine
from umqtt.simple import MQTTClient

# --- Wi-Fi ---
ssid = "Emeka Ude"
password = "Internet2002"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)
print("Connected:", wifi.ifconfig())

# --- MQTT ---
broker = "172.20.10.8"     # same Pi IP as publisher
client_id = "pico_subscriber"
topic = b"temp/pico"

# --- LED setup ---
led = machine.Pin(16, machine.Pin.OUT)

def on_message(topic, msg):
    print("Received:", msg)
    try:
        temp = float(msg)
        if temp >= 25:
            led.value(1)
            print("Temperature high – LED ON")
        else:
            led.value(0)
            print("Temperature normal – LED OFF")
    except Exception as e:
        print("Error parsing message:", e)

mqtt = MQTTClient(client_id, broker)
mqtt.set_callback(on_message)
mqtt.connect()
mqtt.subscribe(topic)
print("Subscribed to topic:", topic)

try:
    while True:
        mqtt.check_msg()
        time.sleep(0.5)
except KeyboardInterrupt:
    mqtt.disconnect()
    print("Disconnected")

