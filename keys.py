import ubinascii
import machine

# Wi-Fi credentials
WIFI_SSID = 'tp-link_2.4'
WIFI_PASS = 'xxxxxxxxx'

# Adafruit IO configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "dz222cv"
AIO_KEY = "aio_xxxxxxxxxxxxxxxx"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# Feed keys
AIO_TEMPERATURE_FEED = "dz222cv/feeds/temperature"  
AIO_HUMIDITY_FEED = "dz222cv/feeds/humidity"
AIO_BUTTON_FEED = "dz222cv/feeds/button"