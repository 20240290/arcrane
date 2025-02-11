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

    """
    A class that will be used to communicate 2 devices using lightweight messaging protocol mqtt.
    Args:
        None

    Returns:
        None 
    """

    def __init__(self, broker: str, topic: str, isBackground: bool, on_message=None):
        """
        Class initializer.

        Args:
            broker (String) : address of the client.
            topic (String) : message identifier.
            isBackground (bool) : distinguish the start of the protocol to be in background or in a loop.
            on_message (method): callback method to handle incoming messages.

        Returns:
            None 
        """
        # MQTT broker and topic setup
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client()

        # Use custom on_message callback if provided
        if on_message:
            self.client.on_message = on_message
        else:
            self.client.on_message = self.on_message

        # Initialize MQTT client
        self._setup_mqtt_client(background=isBackground)

    def _setup_mqtt_client(self, background: bool):
        """
        Initialize and connect to the MQTT broker.

        Args:
            isBackground (bool) : distinguish the start of the protocol to be in background or in a loop.

        Returns:
            None 
        """
        try:
            # Connect to MQTT broker
            self.client.connect(self.broker, port=1883, keepalive=60)
            print("Connected to MQTT broker:", self.broker)

            self.subscribe_to_topic()

            # Start the MQTT client loop in the background
            if background:
                self.client.loop_start
            else:    
                self.client.loop_forever()
        except Exception as e:
            print(f"Error while connecting to MQTT broker: {e}")

    def subscribe_to_topic(self):
        """
        Subscribe to the configured topic.

        Args:
           None

        Returns:
            None 
        """
        try:
            self.client.subscribe(self.topic)
            print(f"Subscribed to topic: {self.topic}")
        except Exception as e:
            print(f"Error while subscribing: {e}")

    def publish_message(self, message):
        """
        Publish a message to the configured topic.

        Args:
           None

        Returns:
            None 
        """
        try:
            self.client.publish(self.topic, message)
            print(f"Published message: {message}")
        except Exception as e:
            print(f"Error while publishing message: {e}")

    def disconnect(self):
        """
        Disconnect from the MQTT broker.

        Args:
           None

        Returns:
            None 
        """
        try:
            self.client.loop_stop()  # Stop the MQTT client loop
            self.client.disconnect()
            print("Disconnected from MQTT broker.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

    def on_message(self, client, userdata, message):
        """
        Callback method to handle incoming messages.

        Args:
           client (class) : mqtt client instance.
           userdata: (dict) : additional information.
           message: (dict) : message meta data.

        Returns:
            None 
        """
        print(f"Received message: {message.payload.decode()} on topic: {message.topic}")
