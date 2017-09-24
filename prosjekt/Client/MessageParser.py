import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'history' : self.parse_history
	    # More key:values pairs are needed
        }

    def parse(self, payload):
        self.payload = json.loads(payload)


        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print "DID NOT FIND RESPONSE"

    def parse_error(self, payload):
        print "ERROR MSG: "
        print payload
        #print json.dumps(payload)

    def parse_info(self, payload):
        self.print_response(payload)

    def parse_history(self, payload):
        print "Message history: "
        for message in payload['content']:
            payload = json.loads(message)
            self.print_response(payload)

    
    # Include more methods for handling the different responses...
