import time
from mqtt import MQTTClient   # MQTT protocol to communicate with Adafruit IO
from machine import Pin      # Pin definitions
import keys                   # Contains Adafruit IO credentials
import wifiConnection         # Wi-Fi connection helper
import dht                    # DHT sensor driver

# ===== CONFIGURATION =====
SEND_INTERVAL = 10000  # Transmission interval: 10 seconds (ms)
AIO_BUTTON_FEED = "dz222cv/feeds/button"

# ===== STATE =====
last_sent_ticks = 0

# ===== PINS =====
tempSensor = dht.DHT11(Pin(27))               # DHT11 on GP27
button = Pin(26, Pin.IN, Pin.PULL_UP)         # Push-button on GP26 (internal pull-up)
last_button_state = button.value()            # Track last button state

# ===== WIFI CONNECT =====
try:
    ip = wifiConnection.connect()
    print("Connected to Wi-Fi, IP:", ip)
except KeyboardInterrupt:
    print("Wi-Fi connection interrupted")
    raise

# ===== MQTT SETUP =====
client = MQTTClient(
    keys.AIO_CLIENT_ID,
    keys.AIO_SERVER,
    keys.AIO_PORT,
    keys.AIO_USER,
    keys.AIO_KEY
)
client.connect()
print("Connected to Adafruit IO")

# ===== MAIN LOOP =====
try:
    while True:
        now = time.ticks_ms()

        # -- Publish sensor data periodically --
        if now - last_sent_ticks >= SEND_INTERVAL:
            try:
                tempSensor.measure()
                temperature = tempSensor.temperature()
                humidity = tempSensor.humidity()
                print(f"Sending Temp={temperature}°C, Hum={humidity}%")
                client.publish(keys.AIO_TEMPERATURE_FEED, str(temperature))
                client.publish(keys.AIO_HUMIDITY_FEED, str(humidity))
                last_sent_ticks = now
            except Exception as e:
                print("Error sending sensor data:", e)

        # -- Detect button state changes --
        current_state = button.value()
        if current_state != last_button_state:
            if current_state == 0:
                print("Button pressed – sending ON")
                client.publish(AIO_BUTTON_FEED, "ON")
            else:
                print("Button released – sending OFF")
                client.publish(AIO_BUTTON_FEED, "OFF")
            last_button_state = current_state

        # Short delay to reduce CPU load
        time.sleep(0.01)

finally:
    client.disconnect()
    # Wi-Fi module remains active; no explicit disconnect method
    print("Disconnected from Adafruit IO.")
