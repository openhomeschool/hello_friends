# The "hello_friends" project
## openhome.school Computer Class

This project extends the idea of saying "hello" (see the "hello" project) to involve a basic
computer network.  You will say hello to your friends in class over the class LAN (local area
network).

## Network hello

**A network is a collection of computers that are connected, usually by a TCP or UDP connection,
either wirelessly or with network cable like Cat5 cable.**  Our network in class is wireless.
Each Raspberry Pi has what's called a "wireless controller".

**A wireless (network interface) controller is a special piece of hardware on a computer (or
attached to a computer) that translates network communication into radio waves which can be received
by another computer's wireless controller, to allow wireless communication between the computers.**

These are sometimes called "wi-fi" devices or adapters.  The acronym "NIC" refers to a "Network
Interface Controller", which were originally wired pieces of hardware, but the most commonly used
personal computer (or personal device, like a phone) network interfaces today are wireless.

This project's code is not very complicated.  It's only about 50 lines of code, and we'll really
only look closely at one file, containing 15 lines of code, most of which are very short, easy
lines to understand, such as:

```python
connection.send(message)
```

There are two main files that make up this "hello" stunt:

## client.py

This is the file we'll focus on most.  It is full of comments to help understand each bit of code.
It's job is to "connect" to a "server", then to listen for any input from the server, or any input
that the user typed into the keyboard.  When you type a message on your keyboard and press "Enter",
the message is sent on this connection, to the server, which then passes that message along to all
other connected computers, called "clients".  Your own computer, where you type, is a "client", and
thus we put this code into a file called "client.py".  The ".py" part of the filename just reminds
you (and your computer) that it's file containing python code.  You'll remember that python is the
name of the computer language that we're using.  Other users in class will type into their computers,
and their messages will travel to the server, which will then broadcast the messages out to all
other clients, including your own computer, so that you can see their messages.

## server.py

This is the slightly longer file.  It has a little more to do.  It doesn't have to look for any
keyboard input, but it does have to manage connections with lots of clients.  Every message that
comes in from a client has to be re-broadcast to the other clients that are connected to this
server.  Because it "serves" the many clients which connect to it, it is called a "server".
Otherwise, there is no magic here.  It doesn't have to live on a fancy computer in a top-secret
"server room" in a special building of unknown location, like in the movies.  You can run the
server on your own computer!

## All alone?

Yes, you can run the server on your own computer.  Then, in another terminal, you can run a client
on your own computer. In yet another terminal, you can run a third client on your own computer.
Then, you can use the two clients to send messages to one another -- type into one client and you'll
see the message pop up in the other (and on the server, which also prints out all messages that
go through it).  Type into the other client, and you'll see the message pop up on the first.  You
could actually start 10 or 100 such clients and talk back and forth, if you're feeling that lonely.

## Let's do it...

Open a terminal.  Change to the "hello_friends" directory:

```sh
cd ohs/hello_friends
```

Your instructor will start the server (server.py).  All students should run the client:

```sh
python client.py
```

Now type something simple an press "Enter".  Everybody in class sees what you typed!

## Code inspection

Let's look at the code a bit:

```python
import socket  
import select
import sys
```

These are libraries - packages of code that will do things for us, simplifying our lives.  'socket'
is a library for managing network connections.  'select' and 'sys' are libraries we'll use to fetch
your typed messages (that you want to send).

Now, the code itself has a lot of "comments"; this conversation should continue there, rather than
here.  Commenting code is a good practice, and writing code that is clear enough to not need much
in the way of comments is an even better practice.

Go spend time with the code!

## More

For more investigation...

* [learn a little more python](https://docs.python.org/3/tutorial/controlflow.html)
* [basic networking](https://edu.gcfglobal.org/en/internetbasics/what-is-the-internet/1/) - the video is half-way down.  There are so many lame videos in this space, so it's worth watching when you find one that's halfway decent!
