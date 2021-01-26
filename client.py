# This is the first line of this file.  Notice that it starts with a '#' character.  That character
# is called a "hash" or "pound" character, and indicates that this line (and the one above, and...
# this one below) is a "comment".  That means it's just plain, conversational text that you are
# enjoying right now.  This is not text that the computer can understand - this is not "code".
# a few lines down, you'll see "import socket" -- THAT line is actually computer code.  Any line
# that does not begin with a hash is a "real" line of code.  Well... almost.  That's "close enough"
# for now!  On we go....

# Import the libraries we'll need:
import socket  
import select
import sys

# Constants:
# Constants are often written at the top of a file so that another programmer can change them later.
# For instance, we set ADDRESS to ('pineapple', 8001) here because the hostname of our tutor's Pi
# is 'pineapple' and the port we decided (arbitrarily) to use is 8001.  Another person might prefer
# a different hostname, for a different server computer.  They could simply change this.
ADDRESS = ('pineapple', 8001)

# Code:
# The remainder of this file is executable "code". This first line will...
# Create the socket and connect it to the server:
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this appears to be a magical, mysterious line of code; you can learn more at https://docs.python.org/3/library/socket.html
connection.connect(ADDRESS) 

# We will "try" to send and recieve all the messages we can, but if there's an error, our program
# will kick down to the "except:" bracket, at the bottom...
try:
	
	# We will simply run this same bit of code, top to bottom, over and over and over, until the
	# connection is closed on us or you press "Control-C" to quit.
	while True: 

		# Look for any input, either from the 'connection' or from the user's own keyboard (sys.stdin):
		readers, writers, errors = select.select((connection, sys.stdin), (), ())

		for reader in readers:
			if reader == connection:
				# A message from another user is ready for us to receive!  Receive it, and print it:
				message = reader.recv(2048) # Why 2048?  That's another study.  You could certainly change this number, with thoughtfulness.
				if message:
					print(message) # this makes the message print out onto your screen
				else:
					# There was nothing in the message, which usually means that the connection closed
					raise # this "raises an exception", causing the program to jump down to the "except" clause and finish, as there's nothing more to do
			else:
				# If the reader was not the connection to the server, then the "input" we have to read 
				# is a message that the user running this 'client.py' program actually typed in, and so
				# we need to read that, and then send it to the server over our 'connection':
				message = sys.stdin.readline() # the message became available when the user pressed "Enter", and so it's one "line" of text
				connection.send(message) 

except:
	# Either something went wrong, or, more likely, our program was intentionally interrupted,
	# meaning that the user running this (client.py) program, himself (or herself), pressed Control-C
	# in order to stop the program, or the server closed the connection, so we no longer have a way
	# to send or receive messages anyway.  For now, all we'll do is try to close our connection to
	# the server (if it isn't already closed), and let our program end.
	connection.close()
