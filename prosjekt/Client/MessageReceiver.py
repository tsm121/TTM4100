# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):

    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        super(MessageReceiver, self).__init__()
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True
        self.connection = connection
        self.client = client

        # TODO: Finish initialization of MessageReceiver

    def run(self):

        while True:
            #break
            data = self.connection.recv(1024)
            self.client.receive_message(data)
