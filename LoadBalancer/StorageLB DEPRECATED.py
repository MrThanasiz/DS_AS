

def loadServerList(path):
    try:
        file = open(path, "r")
    except FileNotFoundError:
        return []
    else:
        serverList = file.readlines()
        file.close()
        for x in range(0, len(serverList)):
            serverList[x] = serverList[x].split(" ")
            serverList[x][1] = int(serverList[x][1])
            serverList[x][2] = int(serverList[x][2].rstrip())
        return serverList

def saveServerList(serverList,path):
    file = open(path,"w+")
    for server in serverList:
        file.write(server[0] + " " + str(server[1]) + " " + str(server[2]) + "\n")
    file.close()

def getServer(path):
    serverList = loadServerList(path)

    if len(serverList) == 0:
        serverList.append(["127.0.0.1",10002,1])
    elif len(serverList) > 0:
        if serverList[-1][2] < 5:
            serverList[-1][2] = serverList[-1][2] + 1
        else:
            serverList.append(["127.0.0.1",serverList[-1][1] + 1,1])

    saveServerList(serverList, path)
    return [serverList[-1][0], serverList[-1][1], serverList[-1][2]]

def printServerList(path):
    serverList = loadServerList(path)
    print(serverList)

def createCMD(addr, port, serverInstancePath):
    file = open(serverInstancePath,"w+")

    file.close()