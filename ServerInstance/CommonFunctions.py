import time
import SecurityServer

def numberOfWords(string):
    stringSplit = string.split(" ")
    return len(stringSplit)


def firstWord(string):
    stringSplit = string.split(" ")
    return stringSplit[0]


def secondWord(string):
    stringSplit = string.split(" ")
    if len(stringSplit) >= 2:
        return stringSplit[1]
    else:
        return "-"


def commandOnly(string):
    commandOnly = firstWord(string).upper()
    return commandOnly


def argumentOnly(string):
    word2 = secondWord(string)
    if word2 == "-":
        return "-"
    stringSplit = string.split(" ", 1)
    return stringSplit[1]


def userpassValidate(argument):
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-=_+,.?"
    if all(char in charset for char in argument) and len(argument) >=6:
        return True
    else:
        return False


def sendDataKeyExchange(data, module):
    data = data.encode()
    module._send_data(data)


def sendData(data, module, SecurityServer):
    data = data.encode()
    data = SecurityServer.encryptData(data)
    module._send_data(data)


def decryptData(data, SecurityServer):
    return SecurityServer.decryptData(data)

def sendSong(songLoc, module, SecurityServer):
    sendData("STINIT", module, SecurityServer) # Song Transfer Init
    time.sleep(0.2)
    f = open(songLoc, 'rb')
    l = f.read(1024)
    while (l):
        module._send_data(l)
        l = f.read(1024)
    f.close()
    time.sleep(0.3)
    module._send_data("STOVER".encode())
