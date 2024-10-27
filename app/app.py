import os
import serial
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see all messages; use INFO for general operation
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Serial port settings
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

# MQTT broker settings from environment variables
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'default/topic')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'username')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'password')

# TimeZone
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')


# Initialize MQTT client and configure authentication
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

def connect_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()  # Start the loop to process network traffic
        logger.info(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        logger.error(f"Failed to connect to MQTT Broker: {e}")
        time.sleep(5)  # Retry connection after 5 seconds

def send_to_mqtt(data):
    try:
        mqtt_client.publish(MQTT_TOPIC, data)
        logger.info(f"Sent to MQTT: {data}")
    except Exception as e:
        logger.error(f"Failed to send data to MQTT: {e}")

# Main loop to read from serial port and send to MQTT
def main():
    try:
        # Initialize serial communication
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logger.info(f"Listening to serial port: {SERIAL_PORT}")

        while True:
            if ser.in_waiting > 0:
                serial_data = ser.readline().decode('utf-8').strip()
                try:
                    # Try to parse the received data as JSON
                    json_data = json.loads(serial_data)
                    logger.debug(f"Received JSON data: {json_data}")
                    timestamp = datetime.now(ZoneInfo(TIME_ZONE)).isoformat()
                    dict = {
                        "data": json_data,
                        "timestamp": timestamp
                    }
                    send_to_mqtt(json.dumps(dict))
                    
                except json.JSONDecodeError:
                    # Ignore non-JSON data
                    logger.warning("Received data is not valid JSON, ignoring...")
                    pass

    except serial.SerialException as e:
        logger.error(f"Serial error: {e}")
        time.sleep(5)   # Retry connecting to the serial port after 5 seconds
        main()          # Retry by calling main again to reconnect

    except KeyboardInterrupt:
        logger.info("Exiting...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        ser.close()

if __name__ == "__main__":
    # Connect to the MQTT broker
    connect_mqtt()

    # Run the main loop
    main()

