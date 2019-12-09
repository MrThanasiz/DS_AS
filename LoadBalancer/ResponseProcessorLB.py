import StorageLB
import time
import os

serverInstancePath = "..\ServerInstance\\"
serverPath = "servers.txt"
clientsPerServer = 5 #should be set to atleast 2

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

# While in the status state the load balancer points the client connected to the next available server
# and keeps track of the number of clients connected to it, when its more than 4 it creates a new server
# and points incoming traffic to there.

    def stateStatus(self, dataDec, module):
        if dataDec.upper() == "STYPE":

            print("NEXT SERVER: ", self.server)
            if StorageLB.getServerConnected(serverPath) == 0:
                StorageLB.createCMD(StorageLB.getServerIP(serverPath), StorageLB.getServerPort(serverPath), serverInstancePath)
                StorageLB.runCMD(serverInstancePath)
            # if last server is almost full, create a new one, so that it'll be read by the time the next client connects
            if StorageLB.getServerConnected(serverPath) == clientsPerServer -1:
                StorageLB.createCMD(StorageLB.getServerIP(serverPath), StorageLB.getServerPort(serverPath) + 1, serverInstancePath)
                StorageLB.runCMD(serverInstancePath)
            if StorageLB.getServerConnected(serverPath) == clientsPerServer:
                StorageLB.setServerPort(StorageLB.getServerPort(serverPath) + 1, serverPath)
                StorageLB.setServerConnected(0, serverPath)
                time.sleep(1)
            StorageLB.setServerConnected(StorageLB.getServerConnected(serverPath) + 1, serverPath)
            sendData("LB " + StorageLB.getServerIP(serverPath) + " " + str(StorageLB.getServerPort(serverPath)), module)
        else:
            sendData("Commands: STYPE", module)




