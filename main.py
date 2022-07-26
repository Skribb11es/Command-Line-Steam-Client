from data.config import *
import vdf
import requests
import json
import os

defaultDirFile = open("C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf", "r").read()
vdfFile = vdf.loads(defaultDirFile)
libFolders = vdfFile["libraryfolders"]
constructedCacheJson = json.loads("[]")
print("Discovering steam apps...")
for folderNum in libFolders:
    print("Initilizing folder (" + str(int(folderNum) + 1) + "/" + str(len(libFolders)) + ")")
    for name in os.listdir(libFolders[folderNum]["path"] + "\\steamapps\\common"):
        exeCount = 0
        exePath = json.loads("[]")
        for exe in os.listdir(libFolders[folderNum]["path"] + "\\steamapps\\common\\" + name):
            if str(exe)[-3:] == "exe":
                exeCount += 1
                exePath.append({
                    "exeName": exe,
                    "path": libFolders[folderNum]["path"] + "\\steamapps\\common\\" + name + "\\" + exe
                })

        if exeCount > 0:
            constructedCacheJson.append({
                "name": name,
                "exeCount": exeCount,
                "pathToExe": exePath
            })

print("Initilization finished!")

run = True
while run:

    x = input()
    if x == "help" or x == "cmds" or x == "commands":
        print("help/cmds/commands - Returns a list of commands and basic explanations \nlaunch [GAME NAME] - Launches the specified game \nClose - closes the command line \nlist - Returns a list of all installed games to the console")
        continue

    if x[0:6] == "launch":
        found = False
        for game in constructedCacheJson:
            if game["name"] == x[7:]:
                found = True
                if game["exeCount"] > 1:
                    print("This app has more than one executible. Which one would you like to run?")
                    count = 1
                    for exe in game["pathToExe"]:
                        print("(" + str(count) + "/" + str(game["exeCount"]) + ") " + exe["exeName"])
                        count += 1
                    select = True
                    while select:
                        y = input()
                        if int(y) < 1 or int(y) > len(game["pathToExe"]):
                            print("Invalid selection")
                        os.startfile(game["pathToExe"][int(y)-1]["path"])
                        select = False
                        print("Done")
                        break
                else:
                    os.startfile(game["pathToExe"][0]["path"])
                    print("Done")
        if found == False:
            print("No app found with name \"" + x[7:] + "\"" )
        continue

    if x == "list":
        for game in constructedCacheJson:
            print(game["name"])
        continue

    if x == "close":
        run = False
        continue
    print("\"" + x + "\" is not a recognised command.")
