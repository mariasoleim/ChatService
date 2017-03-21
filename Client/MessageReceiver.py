# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        # Flag to run thread as a deamon
        Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.connection = connection
        self.start()

    def run(self):
        while True:
            received_string = self.connection.recv(4096)
            self.client.receive_message(received_string)
