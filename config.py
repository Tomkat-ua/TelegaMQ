from dotenv import load_dotenv
import os

load_dotenv()

MQTT_BROKER=os.getenv("MQTT_BROKER")
MQTT_PORT=os.getenv("MQTT_PORT")
MQTT_USERNAME=os.getenv("MQTT_USERNAME")
MQTT_PASSWORD=os.getenv("MQTT_PASSWORD")
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
