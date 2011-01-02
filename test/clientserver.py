import socket, threading, random

from tlslite.api import *

TIMEOUT = 1 # secs
SERVER_PORT = random.randint(10000, 15000)

class TestEndpoint(object):
    def __init__(self, addr='127.0.0.1', port=SERVER_PORT):
        self.addr = addr
        self.port = port

        
class TestServer(TestEndpoint):
    def __init__(self, *args):
        TestEndpoint.__init__(self, *args)
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.addr, self.port))
        self.lsock.listen(TIMEOUT)

    def connect(self):
        return TLSConnection(self.lsock.accept()[0])

    def close(self):
        self.lsock.close()


class TestClient(TestEndpoint):
    def __init__(self, *args):
        TestEndpoint.__init__(self, *args)

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((self.addr, self.port))
        return TLSConnection(sock)

class ServerThread(threading.Thread):
    def __init__(self, server, f):
        threading.Thread.__init__(self)
        self.server = server
        self.run = f

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.join()
