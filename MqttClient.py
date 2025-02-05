"""
 Copyright 2024 Resurgo

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, broker="resurgo2.local", topic="raspberry/signal"):
        # MQTT broker and topic setup
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client()
        
        # Initialize MQTT client
        self._setup_mqtt_client()

    def _setup_mqtt_client(self):
        """Initialize and connect to the MQTT broker."""
        try:
            # Connect to MQTT broker
            self.client.connect(self.broker, port=1883, keepalive=60)
            print("Connected to MQTT broker:", self.broker)

            # Start the client loop
            self.client.loop_start()
        except Exception as e:
            print("Error while connecting to MQTT broker:", e)

    def subscribe_to_topic(self):
        """Subscribe to the configured topic."""
        try:
            self.client.subscribe(self.topic)
            print(f"Subscribed to topic: {self.topic}")
        except Exception as e:
            print("Error while subscribing:", e)

    def publish_message(self, message):
        """Publish a message to the configured topic."""
        try:
            self.client.publish(self.topic, message)
            print(f"Published message: {message}")
        except Exception as e:
            print("Error while publishing message:", e)

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        try:
            self.client.loop_stop()  # Stop the MQTT client loop
            self.client.disconnect()
            print("Disconnected from MQTT broker.")
        except Exception as e:
            print("Error while disconnecting:", e)
