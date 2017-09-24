# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

import time
from socket import *

# Get the server hostname and port as command line arguments
host = "127.0.0.1"
port = 12005
timeout = 1 # in seconds

# Create UDP client socket

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind((host, port))

# Note the second parameter is NOT SOCK_STREAM
# but the corresponding to UDP

# Set socket timeout as 1 second
clientSocket.settimeout(timeout)

# Sequence number of the ping message
ptime = 0

# Ping for 10 times
while ptime < 10:
    ptime += 1
    # Format the message to be sent as in the Lab description
    data = ptime + time.time()
    msg = "testing"


    try:
        start_time = time.time()
        clientSocket.sendto(msg, (host,12000))
        data, server = clientSocket.recvfrom(1024)
        end_time = time.time()
        rtt = round((end_time - start_time),6)

        print ("MSG: "+ data + " " + "Package: " + str(ptime) + " " + "RTT: " + str(rtt))
	# Record the "sent time"

	# Send the UDP packet with the ping message

	# Receive the server response

	# Record the "received time"

	# Display the server response as an output

	# Round trip time is the difference between sent and received time


        # FILL IN END
    except:
        # Server does not response
	# Assume the packet is lost
        print("Request timed out.")
        continue

# Close the client socket
clientSocket.close()

