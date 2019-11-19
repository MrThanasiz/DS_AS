import time
import SMTPClient

class responceProcessor:
    def __init__(self):
        self.state = "status"
        self.nextServer = []

    def messageRouter(self, message, module):
        if self.state == "status" and message.decode().startswith("LB "):
            message = message.decode()
            message = message.split(" ")
            self.nextServer.append(message[1])
            self.nextServer.append(int(message[2]))
            print("Next Server: " + str(self.nextServer))
            module.close()
            self.state = "closed"
            SMTPClient.NWSThreadedClient(self.nextServer[0], self.nextServer[1]).run()
        elif self.state == "keyExchange":
            module.securityClient.messageRouter(message, module)

        elif self.state == "status" and message.decode().startswith("EP"):
            self.state = "keyExchange"
            module.create_message("init".encode())

        else:
            contents = module.securityClient.decryptData(message)
            try:
                print(contents.decode())
            except UnicodeDecodeError:
                print(message)


