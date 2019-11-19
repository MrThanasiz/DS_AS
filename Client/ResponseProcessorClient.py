import os
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

        elif self.state == "songTransfer":
            try:
                if message.decode() == "STOVER":
                    os.startfile("song.wav")
                    self.state = "default"
            except UnicodeDecodeError:
                pass
            f = open("song.wav", "ab")
            f.write(message)
            f.close()

        else:
            contents = module.securityClient.decryptData(message)
            try:
                if contents.decode() == "STINIT":
                    if os.path.exists("song.wav"):
                        os.remove("song.wav")
                    self.state = "songTransfer"
                else:
                    print(contents.decode())
            except UnicodeDecodeError:
                print(message)