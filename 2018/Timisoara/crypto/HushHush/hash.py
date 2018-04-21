#!/usr/bin/env python

import SocketServer
import time
import threading
import random
from Crypto.Util import number
import md5

PORT = 6665    # we obviously need a port to run on...
HOST = '0.0.0.0'
FLAG = "*********"

n = number.getPrime(512)

# can't break it
def my_hash(x):
    global n
    x += "piper"
    x = int(x.encode('hex'), 16)
    for i in range(32):
        x = pow(x, x, n)
        x +=1
    m = md5.new()
    m.update(hex(x))
    return m.hexdigest()


class Service(SocketServer.BaseRequestHandler):

    def handle( self ):
        global FLAG

        self.send("Hello stranger!")
        self.send("Nobody can break my hash but you are free to try.")
        input1 = self.receive("First input: ")
        input2 = self.receive("Second input: ")

        hash1 = my_hash(input1)
        hash2 = my_hash(input2)

        if hash1 == hash2  and input1 != input2:
            print "flag"
            self.send("Thix will never be printed anyway, " + FLAG)
        else:
            self.send("Told ya!")

    def send( self, string, newline = True ):
        if newline: string = string + "\n"
        self.request.sendall(string)  # this `request` object is internal to the BaseRequestHandler that we inherit.

    def receive( self, prompt = " > " ):
        self.send( prompt, newline = False )
        return self.request.recv( 4096 ).strip()


# this class literally doesn't need to do anything, but we need it to exist
# to make the threaded service and serve it up.
class ThreadedService( SocketServer.ThreadingMixIn, SocketServer.TCPServer, SocketServer.DatagramRequestHandler ):
    pass

def main():
    global PORT, HOST

    service = Service # not an object, but at least use the class...

    # now we can create the server object, using the host and port that we define
    # and hosting our service (the class we will keep working on very soon!)
    server = ThreadedService( ( HOST, PORT ), service )
    server.allow_reuse_address = True

    server_thread = threading.Thread( target = server.serve_forever )

    server_thread.daemon = True
    server_thread.start()

    print "Server started on port", PORT

    # Now let the thread just do its thing. We'll wait and do nothing...
    while ( True ): time.sleep(60)


if ( __name__ == "__main__" ):
    main()
