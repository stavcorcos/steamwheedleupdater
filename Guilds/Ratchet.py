import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import os
from dotenv import load_dotenv
import subprocess
import json
import time
load_dotenv()
password = os.environ['PASSWORD']
credentials = json.loads(os.environ['CREDENTIALS'])

def Ratchet():
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    guild = requests.get("https://api.warcraftrumble.gg/guild/437956461").json()
    lastupdated = date.today().strftime("%d %B %Y")
    row = 7

    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.environ['LIVE']) #Local #Dev #Live
    sheet = sheet.worksheet("Ratchet")

    mogul = sheet.cell(2,12).value
    officerone = sheet.cell(3,12).value
    officertwo = sheet.cell(4,12).value

    members = guild["data"]["members"]
    def sortFn(dict):
        return dict['skulls']
    members.sort(key=sortFn, reverse=True)
    for index, key in enumerate(members):
        if key["name"] == mogul:
            members.insert(0, members.pop(index))
            members[0]["name"] += "👑"
        if (key["name"] == officerone) or (key["name"] == officertwo and officerone == ""):
            members.insert(1, members.pop(index))
            members[1]["name"] += "💍"
        if key["name"] == officertwo:
            members.insert(2, members.pop(index))
            members[2]["name"] += "💍"

    for key in members:
        id = key["id"]
        name = key["name"]
        player = requests.get(f"https://api.warcraftrumble.gg/player/{id}").json()
        time.sleep(20)
        link = f"=HYPERLINK(\"https://warcraftrumble.gg/player/{id}\", \"{name}\")"
        skulls = player['data']["skulls"]
        collection = player['data']["level"]
        honor = player['data']["leaderAHonor"] + player['data']["leaderBHonor"] + player['data']["leaderCHonor"]
        cell_list = sheet.range(f"B{str(row)}:I{str(row)}")
        for i, val in enumerate([link, "", skulls, collection, str(honor), "", "", lastupdated]):
            if val != "":
                cell_list[i].value = val
        sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
        row += 1