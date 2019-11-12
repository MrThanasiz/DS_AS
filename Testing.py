import os


def songListLoad():
    songslist = []
    songid = 0
    songsPath = "ServerInstance/songs/"
    if os.path.isdir(songsPath):
        for root, directory, files in os.walk(songsPath):
            for file in files:
                if '.wav' in file:
                    songslist.append([os.path.join(root, file),
                    "ID: " + str(songid) + " Song Name: " + file[:-4]])
                    songid = songid + 1
    else:
        print("No songs folder found on the server, returning empty list")
    return songslist


def getSongLoc(songslist, songid): #TODO REWORK
    try:
        return songslist[songid][0]
    except IndexError:
        return "IDERROR"


def playSong(songloc):
    os.startfile(songloc)



songslist = songListLoad()

for f in songslist:
    print(f)

songloc = getSongLoc(songslist,20)

print(songloc)

playSong(songloc)