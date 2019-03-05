# -*- coding: utf-8 -*-
import codecs
import difflib
import json
import os
import re
import urllib
import webbrowser

import requests
from bs4 import BeautifulSoup

from wox import Wox, WoxAPI


class Steamlauncher(Wox):

    gameList = []
    f = codecs.open("./config.json", "r", "utf-8")
    dirConfig = json.load(f)
    f.close()

    if not dirConfig["steamapps_dir"]:
        steamappsDir = None
    else:
        if os.path.isdir(dirConfig["steamapps_dir"]):
            steamappsDir = dirConfig["steamapps_dir"]
            for file_entry in os.scandir(steamappsDir):
                if "appmanifest" in file_entry.name:
                    gameId = file_entry.name.replace("appmanifest_", "").replace(
                        ".acf", ""
                    )
                    if gameId == "228980":
                        continue
                    with open(file_entry.path) as f:
                        for line in f:
                            if line.find("name") > 0:
                                gameTitle = (
                                    line.replace('"', "").replace("name", "").strip()
                                )
                                break
                    if os.path.isfile("./icon/" + gameId + ".jpg"):
                        gameIcon = "./icon/" + gameId + ".jpg"
                    else:
                        try:
                            url = "https://steamdb.info/app/{}/".format(gameId)
                            headers = {
                                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
                            }
                            r = requests.get(url, headers=headers)
                            soup = BeautifulSoup(r.text, "html.parser")
                            data = soup.find("img", attrs={"class": "app-icon avatar"})
                            img = data.attrs["src"]
                            urllib.request.urlretrieve(img, "./icon/" + gameId + ".jpg")
                            gameIcon = "./icon/" + gameId + ".jpg"
                            gameIcon = "./icon/missing.png"
                        except Exception as e:
                            gameIcon = "./icon/missing.png"
                    gameList.append(
                        {"gameId": gameId, "gameTitle": gameTitle, "gameIcon": gameIcon}
                    )
        else:
            steamappsDir = False

    def query(self, query):
        result = []
        gameList = self.gameList
        q = query.lower()
        pattern = ".*?".join(q)
        regex = re.compile(pattern)
        for line in gameList:
            match = regex.search(line["gameTitle"].lower())
            if match:
                result.append(
                    {
                        "Title": line["gameTitle"] + " - ({})".format(line["gameId"]),
                        "SubTitle": "Press Enter key to launch '{}'.".format(
                            line["gameTitle"]
                        ),
                        "IcoPath": line["gameIcon"],
                        "JsonRPCAction": {
                            "method": "launchGame",
                            "parameters": [line["gameId"]],
                            "dontHideAfterAction": False,
                        },
                    }
                )
        return result

    def launchGame(self, gameId):
        webbrowser.open("steam://rungameid/{}".format(gameId))


if __name__ == "__main__":
    Steamlauncher()
