import os

defaultServer = ["127.0.0.1", 10002, 0]

def getServer(path):
    try:
        file = open(path, "r")
    except FileNotFoundError:
        print("File not found returning default server")
        file = open(path, "w+")
        file.write(defaultServer[0] + " " + str(defaultServer[1]) + " " + str(defaultServer[2]))
        file.close()
        return defaultServer
    else:
        serverLines = file.readlines()
        file.close()
        if len(serverLines) == 0:
            file = open(path, "w+")
            file.write(defaultServer[0] + " " + str(defaultServer[1]) + " " + str(defaultServer[2]))
            file.close()
            file = open(path, "r")
            serverLines = file.readlines()
            file.close()
        if len(serverLines) == 1:
            server = serverLines[0].split(" ")
            server[1] = int(server[1])
            server[2] = int(server[2].rstrip())
        if len(serverLines) > 1:
            print("error in servers.txt returning default server...")
            return defaultServer
        return server

def getServerIP(path):
    server = getServer(path)
    return server[0]

def getServerPort(path):
    server = getServer(path)
    return server[1]

def getServerConnected(path):
    server = getServer(path)
    return server[2]

def setServerIP(ip, path):
    server = getServer(path)
    file = open(path, "w+")
    file.write(ip + " " + str(server[1]) + " " + str(server[2]))
    file.close()
    server[0] = ip

def setServerPort(port, path):
    server = getServer(path)
    file = open(path, "w+")
    file.write(server[0] + " " + str(port) + " " + str(server[2]))
    file.close()
    server[1] = port

def setServerConnected(count, path):
    server = getServer(path)
    file = open(path, "w+")
    file.write(server[0] + " " + str(server[1]) + " " + str(count))
    file.close()
    server[2] = count

def setServer(ip, port, count, path):
    setServerIP(ip, path)
    setServerPort(port, path)
    setServerConnected(count, path)


def createCMD(addr, port, serverInstancePath):
    file = open(serverInstancePath + "startServer.cmd","w+")
    file.write("python SMTPServer.py" + " " + addr + " " + str(port) +"\npause")
    file.close()

def runCMD(serverInstancePath):
    os.system("cd "+ serverInstancePath + " & start startServer.cmd")

def resetServer(path):
    server = getServer(path)
    setServer(defaultServer[0], defaultServer[1], defaultServer[2], path)