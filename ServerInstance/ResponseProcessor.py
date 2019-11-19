import CommonFunctions
import SecurityServer
import Storage
import time

class responseProcessor:
    def __init__(self):
        self.state = "status"
        self.transferKey = 0
        self.securityServer = SecurityServer.securityServer()
        self.accountUserRegistry = Storage.accountsLoad("User")
        self.songRegistry = Storage.songListLoad()
        print("FILES LOADED")
        self.currentUser = []

    def commandRouter(self, dataEnc, module):

        if self.state == "status":
            dataDec = dataEnc.decode()
            self.stateStatus(dataDec, module)

        elif self.state == "keyExchange":
            dataDec = dataEnc.decode()
            self.stateKeyExchange(dataDec, module)

        elif self.state == "login":
            dataDec = self.securityServer.decryptData(dataEnc).decode()
            self.stateLogin(dataDec, module)

        elif self.state == "default":
            dataDec = self.securityServer.decryptData(dataEnc).decode()
            self.stateDefault(dataDec, module)
        else:
            CommonFunctions.sendData("Command couldn't be routed " + self.state + " state unknown", module, self.securityServer)

    def stateStatus(self, dataDec, module):
        dataDec = dataDec.upper()
        if dataDec == "INIT":
            self.state = "keyExchange"
            self.stateKeyExchange(dataDec, module)
        elif dataDec == "STYPE":
            CommonFunctions.sendDataKeyExchange("EP", module)
        elif dataDec == "LOAD":
            CommonFunctions.sendDataKeyExchange("WiP", module) #TODO this how?
        else:
            CommonFunctions.sendDataKeyExchange("Commands: INIT, STYPE, LOAD", module)

    def stateKeyExchange(self, dataDec, module):
        self.transferKey, completed = (self.securityServer.initiateKeyExchangeServer(dataDec, module))
        if completed:
            self.state = "default" #TODO CHANGE BACK TO LOGIN AFTER TESTING!!!
            print(str(self.transferKey))

    def stateLogin(self, dataDec, module):
        command = CommonFunctions.commandOnly(dataDec).upper()
        argument = CommonFunctions.argumentOnly(dataDec)
        if (command == "REGISTER" or command == "LOGIN") and CommonFunctions.numberOfWords(argument) == 2:
            userName = CommonFunctions.firstWord(argument)
            userPass = CommonFunctions.secondWord(argument)
            if CommonFunctions.userpassValidate(userName) and CommonFunctions.userpassValidate(userPass):
                if command == "REGISTER":
                    self.commandREGISTER(argument, module)
                else:
                    self.commandLOGIN(argument, module)
            else:
                CommonFunctions.sendData(" Username and Password must be atleast 6 characters long and CAN contain numbers,"
                                         " letters including the following symbols !@#$%^&*()-=_+,.?", module, self.securityServer)
        else:
            CommonFunctions.sendData(" Available commands: \n"
                         "login <username> <password> \n"
                         "register <username> <password>", module, self.securityServer)


    def stateDefault(self, dataDec, module):

        command = CommonFunctions.commandOnly(dataDec)
        argument = CommonFunctions.argumentOnly(dataDec)
        print("State:" + self.state + " Data:" + dataDec + " Command:" + command + " argument:" + argument)

        if command ==   "LOGOUT":
            self.commandLOGOUT(module)
        elif command == "SONGLIST":
            self.commandSONGLIST(module)
        elif command == "DOWNSONG":
            self.commandDOWNSONG(argument, module)
        elif command == "HELP":
            self.commandHELP(argument, module)
        else:
            CommonFunctions.sendData("Unknown command, try HELP", module, self.securityServer)


    def commandREGISTER(self, argument, module):

        userName = CommonFunctions.firstWord(argument)
        if Storage.accountExists(self.accountUserRegistry, userName):
            CommonFunctions.sendData("Account already exists.", module, self.securityServer)
        else:
            userPass = CommonFunctions.secondWord(argument)
            hashedPassword, salt = SecurityServer.hashPW(userPass)
            tuser = Storage.accountUser(userName, hashedPassword, salt, ["",""])
            Storage.accountAdd(self.accountUserRegistry, tuser)
            Storage.accountsSave(self.accountUserRegistry, "User")
            CommonFunctions.sendData("Account Registered Successfuly, Log in.", module, self.securityServer)


    def commandLOGIN(self, argument, module):
        userName = CommonFunctions.firstWord(argument)
        userPass = CommonFunctions.secondWord(argument)
        if Storage.accountValidateLogin(self.accountUserRegistry, userName, userPass):
            self.currentUser = Storage.accountGet(self.accountUserRegistry, userName)
            self.state = "default"
            CommonFunctions.sendData("Logged in successfully", module, self.securityServer)
        else:
            CommonFunctions.sendData("Username password pair doesn't exist, try again.", module, self.securityServer)


    def commandLOGOUT(self, module):
        self.state = "login"
        self.currentUser = []
        CommonFunctions.sendData("Logged out successfully.", module, self.securityServer)

    def commandSONGLIST(self, module):
        for song in self.songRegistry:
            CommonFunctions.sendData(song[1], module, self.securityServer)
            time.sleep(0.05) #????

    def commandDOWNSONG(self, argument, module):
        try:
            songid = int(argument)
        except ValueError:
            CommonFunctions.sendData("Song ID can only be an Integer.", module, self.securityServer)
        else:
            songloc = Storage.getSongLoc(self.songRegistry, songid)
            if contents == "IDERROR":
                CommonFunctions.sendData("Song ID does not exist.", module, self.securityServer)
            else:
                CommonFunctions.sendSong(songloc, module, SecurityServer)

    def commandHELP(self, argument, module):
        argument = argument.upper()
        if argument == "-":
            data = "For more information on a specific command, type HELP command \n" \
                    "LOGOUT          The Logout command logs out the current user. \n" \
                    "SONGLIST        The Songlist command lists all the available songs. \n" \
                    "DOWNSONG        The Downsong command downloads the song with the provided ID. \n" \
                    "HELP            The Help command shows more information about commands."
        elif argument == "LOGOUT":
            data = "The Logout command logs out the current user. \n" \
                   "USAGE: LOGOUT"
        elif argument == "SONGLIST":
            data = "The Songlist command lists all the available songs. \n" \
                   "USAGE: SONGLIST"
        elif argument == "DOWNSONG":
            data = "The Downsong command downloads the song with the provided ID. \n" \
                   "USAGE: DOWNSONG 4"
        elif argument == "HELP":
            data = "The Help command shows more information about commands. \n" \
                   "USAGE: HELP (SONGLIST)"
        else:
            data = "Unknown command, try HELP"

        CommonFunctions.sendData(data, module, self.securityServer)



