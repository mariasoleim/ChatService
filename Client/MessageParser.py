import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload.decode())
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            pass

    def parse_error(self, payload):
        print('\n\n' + payload['timestamp'])
        print('An error has occured:')
        print(payload['content'])
        print('\n')

    def parse_info(self, payload):
        print('\n\n' + payload['timestamp'])
        print('Info from server:')
        print(payload['content'])
        print('\n')


    def parse_message(self, payload):
        print('\n\n' + payload['timestamp'])
        print('Message from ' + payload['sender'] + ':')
        print(payload['content'])
        print('\n')

    def parse_history(self, payload):
        print('\n\nTimestamp: ' + payload['timestamp'] + '\nSender: ' + payload['sender'] + '\nMessage: ' + payload['content'])
