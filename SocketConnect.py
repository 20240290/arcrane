import paho.mqtt.client as mqtt
import time

# MQTT Broker configuration
BROKER = "resurgo2.local" #"10.0.105.146"  # Replace with your broker address
PORT = 1883
TOPIC = "raspberry/signal"  # Replace with your topic

def main():
    client = mqtt.Client()
    client.enable_logger()
    
    try:
        client.connect(BROKER, PORT, 60)
        print("Connected to MQTT Broker!")

        while True:
            message = "Hello MQTT!"
            client.publish(TOPIC, message)
            print(f"Sent: {message}")
            time.sleep(2)  # Publish every 2 seconds

    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")
        client.disconnect()

if __name__ == "__main__":
    main()
