# -*- coding: utf-8 -*-
import socket
import json
import time
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:

    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_parser = MessageParser()
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.message_receiver = MessageReceiver(self, self.connection)

        while True:
            user_input = input()
            try:
                req, cont = user_input.split(" ", 1)
            except ValueError:
                req = user_input
                cont = 'None'
            payload = {
                'request': req,
                'content': cont
            }
            self.send_payload(payload)

    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        self.message_parser.parse(message)

    def send_payload(self, data):
        payload = json.dumps(data)
        self.connection.send(payload.encode())

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
