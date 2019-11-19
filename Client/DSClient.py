__author__ = "Christopher Windmill, Brad Solomon"

__version__ = "1.0.1"
__status__ = "Development"

import time
import socket
import selectors
import DSClientLib
import traceback

LBhost = "127.0.0.1"
LBport = 9999

class DSThreadedClient ():
    def __init__(self, host, port):
        if __debug__:
            print("DSThreadedClient.__init__", host, port)

        # Network components
        self._host = host
        self._port = port
        self._listening_socket = None
        self._selector = selectors.DefaultSelector()

        self._module = None

    def start_connection(self, host, port):
        addr = (host, port)
        print("starting connection to", addr)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)

        self._module = DSClientLib.Module(sock, addr)
        self._module.start()

    def run(self):
        self.start_connection(self._host, self._port)

        if self._module.responseProcessor.state == "status":
            self._module.create_message("stype".encode())
        # ^^ if state status is not to be used switch to this
        time.sleep(0.2)

        while True:
            if self._module.responseProcessor.state == "closed":
                print("Connection closed breaking loop.")
                break

            userInput = input("Send a message:")

            if len(userInput) == 0:  # This is used to prevent sending an empty message
                userInput = userInput + " "

            if self._module.responseProcessor.state == "status":
                message = userInput.encode()
            else:
                message = self._module.securityClient.encryptData(userInput)

            self._module.create_message(message)

            time.sleep(0.1)


if __name__ == "__main__":
    client = DSThreadedClient(LBhost, LBport)
    client.run()
