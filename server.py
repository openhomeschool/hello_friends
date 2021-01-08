	# Import the libraries we'll need:
import socket # more (very detailed) information at https://docs.python.org/3/library/select.html
import select # more (very detailed) information at https://docs.python.org/3/library/socket.html
import sys # more (very detailed) information at https://docs.python.org/3/library/sys.html
from thread import start_new_thread

# Constants:
# Constants are often written at the top of a file so that another programmer can change them later.
# For instance, we set ADDRESS to ('pineapple', 8001) here because the hostname of our tutor's Pi
# is 'pineapple' and the port we decided (arbitrarily) to use is 8001.  Another person might prefer
# a different hostname, for a different server computer.  They could simply change this.
ADDRESS = ('0.0.0.0', 8001)
# Note that one convention is to CAPITALIZE words that denote "constants" - this value is "constant"
# becuase it is set here, at the top of the file, once, and never changes throughout the program.

# (Advanced: note that 'pineapple' only works because, elsewhere on the computer on which this code
# runs, the "knowledge" that 'pineapple' corresponds to this computer's external IP Address.  In
# our case, that happens to be 10.20.50.11.  By "external", we merely mean that it's "visible" to
# other computers on the 10.20.50 network; in our case, all of the Pis are fruit names, like kiwi.
# If we had used an "internal" name or address, like 'localhost' or '127.0.0.1', no other computers
# on the network would be able to see this server or interact with it. This is a bit hard to
# understand until you have a little more experience with networks.)


# Global variables:
# By contrast (to constants), variables are containers for data that will change over the course
# of a program's lifespan.  In this case, 'clients' is initialized as an empty list.  Many things
# (connections, in our case) can be put into a list.
clients = [] 


# Functions:
# Our "big" problem can be broken up into smaller pieces.  Each piece of our solution gets a
# function.  Each function starts with 'def' (meaning "define" a function as...), takes input
# inside of parentheses (), and ends with a colon ':'.

def create_server():
	# Make calls to libraries to do magical mysterious things to make the kind of server we want:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	server.bind(ADDRESS) 
	server.listen(100) # tells the server to listen for up to 100 simultaneous connections; this could have been specified as a CONSTANT at the top of the file, after ADDRESS
	# (learn more about these magical arguments at https://docs.python.org/3/library/socket.html)
	# Now that our server is all set up, we "return" it to the caller of this function:
	return server


def client_thread(connection, address): 
	# Send a "welcome" message to the client who just connected to us, which started this thread:
	connection.send("Welcome to the class chat room!  Type your message, then hit enter!")

	# Loop until this connection dies ('alive' will be set to False when that happens): 
	alive = True
	while alive:
		try:
			# Receive ('recv') as many as 2,048 characters that were sent.  Why 2048?  That's another study.  You could certainly change this number.
			message = connection.recv(2048) 
			if message: # i.e., if there was actually any text in the message sent...

				# Print the (sender, or client) address and message on the server screen:
				formatted_message = "<" + address[0] + "> " + message
				print (formatted_message) 

				# Broadcast the message (i.e., send it to all clients in our collection - see the broadcast() function definition for more details)
				for client in clients:
					# Try to send to each client in our list of clients...
					if client != connection: # ... EXCEPT the client that is the original sender! (they don't need to see their own message spit back at them!)
						try: 
							client.send(formatted_message)
						except:
							# The send() failed, so we assume that that client can no longer be reached.  We'll "close" the socket connection to that client:
							client.close() 
							# And remove the client from the list:
							try:
								clients.remove(client)
							except:
								# Another thread must have removed the client while we weren't looking! There is nothing left to do
								pass # pass just means: "never mind, move on"

			else:
				# The incoming message had no text at all. This tends to mean that the connection is broken, so we remove it from the list:
				clients.remove(connection)
				# And we set 'alive' to False, which will cause this thread to stop looping, and it will come to an end.
				alive = False

		except:
			# Any other trouble we have, we'll assume is not important enough to treat now, but an improvement would be to at least print something to the screen to indicate that there was trouble
			continue # this is like "pass", above, but it specifically means to start over at the top of the "while" loop.
			# In this case, since there is no code in this function below, "continue" would do the same thing as "pass"


# And here begins the actual main program, as everything above was just code that defined constants,
# global variables, and functions.  If the rest of this file was empty, this "program" would do
# nothing at all.  The code below is not inside of a function, so it will get executed when the
# program is run, but, when the code below needs to use the constants or functions defined above,
# then it can call them by name.  When the function, above, is called by name, it will finally be
# run, or "executed", as it's often called in software development.

server = create_server() # Finally, actually create the server

# This "while True:" is just a never-ending loop.  The code below, within, will run, top to bottom,
# over and over again until you forcibly kill it (e.g., by pressing Control-C while it's running
# in your terminal).
while True: 
	
	# Accept connections that clients are asking us to accept (this is like picking up the phone when it's ringing):
	connection, address = server.accept() 

	# Add the new connection to the list of clients:
	clients.append(connection)

	# Print the IP address of the client that just connected, just to inform anybody watching the server directly:
	print(address[0] + " connected")

	# Start the thread that will process this connection's messages until it is finally closed (by the user, or by the server shut-down):
	start_new_thread(client_thread, (connection, address))

server.close() 


# Possible improvements you could make:
# 1) Make the number of simultaneous connections (100) a constant at the top of the file.  Try
#    making it very small and see what happens if you try to connect too many clients.
# 2) print() some useful information to screen when an exception occurs (in an 'except:' handler).
# 3) print() the address of a client that just disconnected, before removing the client from our list
# Advacnced improvements you could make:
# 1) Add a mechanism in client.py that allows a user to state their name (or 'handle') upon
#    connecting.  Then, use that name instead of the IP addresses of clients, to broadcast the
#    message to other connected clients/users.
# 2) Do a DNS lookup, in order to convert the IP address to a hostname, and either use that in the
#    place of the IP addresses, or, in combination with #1, prompt each message with "<user, host>"
# 3) Add a mutex in client_thread (at a carefully chosen location) to ensure the processing of only
#    one message at a time, and protect against the attempt to use a connection that might have
#    been removed by another thread.
