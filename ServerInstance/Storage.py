import datetime
import os
import SecurityServer
import pickle


class accountUser:
    def __init__(self, username, passwordHashed, salt):
        self.username = username
        self.passwordHashed = passwordHashed
        self.salt = salt

    def getIdentifier(self):
        return self.username

    def printAccountData(self):
        print("Address:  " + self.address)
        print("password: " + self.passwordHashed)
        print("Salt:     " + self.salt)


def accountAdd(accountsRegistry, account):
    # Make sure to check that the account doesn't exist already
    # input should be account type
    accountsRegistry.append(account)
    return accountsRegistry


def accountDelete(accountsRegistry, identity):
    for account in accountsRegistry:
        if account.getIdentifier() == identity:
            accountsRegistry.remove(account)
    return accountsRegistry


def accountExists(accountsRegistry, identity):
    # can be used for both Email & User type accounts
    for account in accountsRegistry:
        if account.getIdentifier() == identity:
            return True
    return False

def accountGet(accountsRegistry, identity):
    for account in accountsRegistry:
        if account.getIdentifier() == identity:
            return account


def accountValidateLogin(accountsRegistry, identity, password):
    # can be used for both Email & User type accounts
    for account in accountsRegistry:
        if account.getIdentifier() == identity:
            return SecurityServer.validatePW(account.passwordHashed, account.salt, password)
    print("doesn't exist")
    return False


def accountsSave(accountsRegistry, accountsType):
    filename = "accounts" + accountsType
    f = open(filename, "wb")
    pickle.dump(accountsRegistry, f)
    f.close()


def accountsLoad(accountsType):
    accountsRegistry = []
    filename = "accounts" + accountsType
    try:
        f = open(filename, "rb")
    except FileNotFoundError:
        print("404 - Returing Test Variable")
        if accountsType == "User":
            userName = "testuser"
            userPass = "testpass"
            hashedPassword, salt = SecurityServer.hashPW(userPass)
            tuser = accountUser(userName, hashedPassword, salt)
            accountAdd(accountsRegistry, tuser)
            #accountsSave(accountsRegistry, "User") # Will only be saved if something get's added.
        else:
            print("Unknown type, returning empty list")
        return accountsRegistry
    else:
        accountsRegistry = pickle.load(f)
        f.close()
    return accountsRegistry


def songListLoad():
    songlist = []
    songid = 0
    songsPath = "songs/"
    if os.path.isdir(songsPath):
        for root, directory, files in os.walk(songsPath):
            for file in files:
                if '.wav' in file:
                    songlist.append([os.path.join(root, file),
                    "ID: " + str(songid) + " Song Name: " + file[:-4]])
                    songid = songid + 1
    else:
        print("No songs folder found on the server, returning empty list")
    return songlist


def getSongLoc(songlist, songid):
    try:
        return songlist[songid][0]
    except IndexError:
        return "IDERROR"