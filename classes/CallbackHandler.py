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
 limitations under
 """

class CallbackHandler:
    def __init__(self):
        # Dictionary to store subscribers and their callback methods
        self.subscribers = {}

    def register_subscriber(self, subscriber_id, callback):
        """
        Register a subscriber with an ID and their callback function.
        :param subscriber_id: Unique ID for the subscriber.
        :param callback: Function to be called when an event occurs.
        """
        self.subscribers[subscriber_id] = callback

    def unregister_subscriber(self, subscriber_id):
        """
        Unregister a subscriber by their ID.
        :param subscriber_id: Unique ID of the subscriber.
        """
        if subscriber_id in self.subscribers:
            del self.subscribers[subscriber_id]

    def notify_subscriber(self, subscriber_id, message):
        """
        Notify a specific subscriber.
        :param subscriber_id: The ID of the subscriber to notify.
        :param message: The message to send to the subscriber.
        """
        if subscriber_id in self.subscribers:
            self.subscribers[subscriber_id](message)
        else:
            print(f"Subscriber with ID '{subscriber_id}' not found.")

    def notify_all(self, message):
        """
        Notify all subscribers.
        :param message: The message to send to all subscribers.
        """
        for subscriber_id, callback in self.subscribers.items():
            callback(message)