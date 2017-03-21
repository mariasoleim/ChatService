# -*- coding: utf-8 -*-
import socketserver
import json
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_users = {}
messages = []

def login(client_handler, username):
    ips = []
    for handler in connected_users.keys():
        ips.append(handler.ip)
    if not username.isalnum():
        client_handler.send_error('Username can only contain letters and numbers.')
    elif username in connected_users.values():
        client_handler.send_error('Username is already taken.')
    elif client_handler.ip in ips:
        client_handler.send_error('You are already connected.')
    else:
        connected_users[client_handler] = username
        client_handler.send_info('Login successful.')

def logout(client_handler, self):
    # Not finished
    pass

def msg(client_handler, content):
    message = {
        'timestamp': '{:%x - %X}'.format(datetime.datetime.now()),
        'sender': 'username',
        'response': 'message',
        'content': content
    }
    payload = json.dumps(message).encode()
    for handler in connected_users.keys():
        handler.connection.send(payload)

def names(client_handler, foo):
    names = 'Connected users:'
    for name in connected_users.values():
        names += '\n'
        names += name
    client_handler.send_info(names)

def help(client_handler):
    pass

requests = {
    'login': login,
    'logout': logout,
    'msg': msg,
    'names': names,
    'help': help
}

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).decode()
            payload = json.loads(received_string)
            req = payload['request']
            cont = payload['content']
            if req in requests.keys():
                requests[req.lower()](self, cont)
            else:
                self.send_error('Do not reqognize the request.')

    def send_error(self, content):
        self.send('server', 'error', content)

    def send_info(self, content):
        self.send('server', 'info', content)

    def send(self, sender, response, content):
        message = {
            'timestamp': '{:%x - %X}'.format(datetime.datetime.now()),
            'sender': sender,
            'response': response,
            'content': content
        }
        payload = json.dumps(message).encode()
        self.connection.send(payload)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
