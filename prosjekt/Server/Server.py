# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time


"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = ["thomas", "andreas"]
logged_in_users = {
    #username:self
}
user_history=[]

class ClientHandler(SocketServer.BaseRequestHandler):

    username = None
    connection_active = True
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
        print self.ip + " connected to server on port " + str(self.port)
        while self.connection_active:
            received_string = self.connection.recv(4096)


            if len(received_string) > 0:

                json_msg = json.loads(received_string)

                type = json_msg["response"]
                if len(json_msg) > 1:
                    usermsg = json_msg["content"]
                else:
                    usermsg = None

                client_port, client_ip = self.client_address[1], self.client_address[0]
                self.handlePayload(type, usermsg, client_port)


    def handlePayload(self, type, usermsg, client_port):

        response = None


        if type == "login":
            #usermsg = brukernavn

            if usermsg not in users:
                self.send_response("Unknown user: " + usermsg, "error", "server")

            elif usermsg in users:
                if logged_in_users.has_key(usermsg):
                    self.send_response("User " + usermsg + " already logged in","info","server")

                else:
                    logged_in_users[usermsg] = self
                    self.username = usermsg
                    self.send_response("User " + usermsg + " logged in", "info", "server")
                    print "User " + usermsg + " logged in with port " + str(client_port)

            #return self.createServerResponse(type, usermsg, response)

        elif type == "logout":

            if self.username in logged_in_users.keys():

                del logged_in_users[self.username]
                print "User " + self.username + " logged out"
                self.send_response("User " + self.username + " logged out", "info","server")

            else:
                self.send_response("User " + usermsg + " is not logged in", "info", "server")

        elif type == "help":

            self.send_response("1. login <username>, 2. logout, 3. msg <message>, 4. history, 5. users,  6. help", "help", "server")


        elif type == "msg":
            if self.username in logged_in_users.keys():
                self.send_response(usermsg, "msg", self.username)

            else:
                self.send_response("Can't send msg: '" + usermsg + "'. You are not logged in.", "error", "server")

        elif type == "history":
            self.send_response(user_history, "history","server")

        elif type == "users":
            self.send_response(logged_in_users.keys(), "users", "server")


        # TODO: Add handling of received payload from client

    def send_response(self, content, response, sender):

        json_msg = {}
        json_msg["response"] = response
        json_msg["timestamp"] = time.asctime( time.localtime(time.time()))
        json_msg["sender"] = sender
        json_msg["content"] = content
        json_obj = json.dumps(json_msg)

        if response == "msg":
            for user in logged_in_users:
                logged_in_users[user].connection.sendall(json_obj)
            user_history.append(json_obj)

        elif response == "logout":
            self.connection.close()
            self.connection_active = False

        else:
            self.connection.send(json_obj)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
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
    HOST, PORT = "localhost", 9998
    print "Server running..."

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
