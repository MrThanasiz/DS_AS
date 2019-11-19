import StorageLB
import time
import os

serverInstancePath = "..\ServerInstance\\"
serverPath = "servers.txt"

def sendData(data, module):
    data = data.encode()
    module._send_data(data)

class responseProcessor:
    def __init__(self):
        self.state = "status"
        self.server = StorageLB.getServer(serverPath)

    def commandRouter(self, dataEnc, module):

        if self.state == "status":

            dataDec = dataEnc.decode()

            self.stateStatus(dataDec, module)

        else:
            sendData("Command couldn't be routed " + self.state + " state unknown", module)

    def stateStatus(self, dataDec, module):
        if dataDec.upper() == "STYPE":
            StorageLB.setServerConnected(StorageLB.getServerConnected(serverPath) + 1, serverPath)
            print("NEXT SERVER: ", self.server)
            if StorageLB.getServerConnected(serverPath) == 6:
                StorageLB.setServerPort(StorageLB.getServerPort(serverPath) + 1, serverPath)
                StorageLB.setServerConnected(1, serverPath)
            if StorageLB.getServerConnected(serverPath) == 1 or StorageLB.getServerConnected(serverPath) == 6:
                StorageLB.createCMD(StorageLB.getServerIP(serverPath), StorageLB.getServerPort(serverPath), serverInstancePath)
                StorageLB.runCMD(serverInstancePath)
                time.sleep(1)
            sendData("LB " + StorageLB.getServerIP(serverPath) + " " + str(StorageLB.getServerPort(serverPath)), module)
        else:
            sendData("Commands: STYPE", module)




