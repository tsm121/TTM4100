# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):

        self.host = host
        self.server_port = server_port

        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

        # TODO: Finish init process with necessary code
    def run(self):

        # Initiate the connection to the server
        print "client: connecting"
        self.connection.connect((self.host, self.server_port))
        self.thread = MessageReceiver(self, self.connection)
        self.thread.start()
        print "client: connected"
        print "1. login <username>, 2. logout, 3. msg <message>, 4. history, 5. users,  6. help\n"

        while True:
            payload = self.create_response()
            self.send_payload(payload)
            if input is "logout":
                self.disconnect()
                break

        
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        payload = json.loads(message)
        response = payload["response"]
        content = payload["content"]
        sender = payload["sender"]
        timestamp = payload["timestamp"]

        if response == "info":
            print "[info]: " + content

        elif response == "error":
            print "[error]: " + content

        elif response == "msg":
            print timestamp[11:16] + "-" + sender + ": " + content

        elif response == "history":
            for msg in content:
                self.receive_message(msg)

        elif response == "help":
            print str(content)

        elif response == "users":

            print "There are " + str(len(content)) + " users logged in: " + str(content)

        else:
            print "Unknown response from server: " + message


    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.sendall(data)

    # More methods may be needed!

    def create_response(self):

        user_input = raw_input(">>> ").split(" ")

        if (len(user_input) == 1):

            json_dic = {
                "response": user_input[0], #type
            }

        else:
            json_dic = {
                "response": user_input[0], #type
                "content": user_input[1], #user msg
            }


        return json.dumps(json_dic)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
