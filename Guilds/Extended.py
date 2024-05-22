import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import os
from dotenv import load_dotenv
import subprocess
import json
load_dotenv()
password = os.environ['PASSWORD']
credentials = json.loads(os.environ['CREDENTIALS'])

def Extended():
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os['LOCAL']) #Local #Dev #Live
    sheet = sheet.worksheet("Extended")

    guilds = [199066642, 467715881, 439520221, 200915262, 469001351, 439001941, 200912272, 202782692, 200875392, 437378721, 437956461, 439021421, 466689451, 437262641, 439157421, 199002432, 466295671, 466386371, 51433483, 438015331, 52083073, 466184131, 202672512, 203652452, 468022961, 467766291, 466419191, 203585612]

    lastupdated = date.today().strftime("%d %B %Y")

    row = 5
    for guildID in guilds:
        guild = requests.get(f"https://api.warcraftrumble.gg/guild/{str(guildID)}").json()
        totalSkulls = 0
        memberCount = 0
        totalLevels = 0
        totalHonor = 0
        for member in guild["data"]["members"]:
            memberCount += 1
            id = member["id"]
            player = requests.get(f"https://api.warcraftrumble.gg/player/{id}").json()
            totalSkulls += int(player["data"]["skulls"])
            totalLevels += int(player["data"]["level"])
            totalHonor += int(player["data"]["leaderAHonor"]) + int(player["data"]["leaderBHonor"]) + int(player["data"]["leaderCHonor"])
        averageSkulls = totalSkulls/memberCount
        averageLevels = totalLevels/memberCount
        averageHonor = totalHonor/memberCount
        cell_list = sheet.range(f"C{str(row)}:I{str(row)}")
        for i, val in enumerate([str(memberCount), "", "", str(averageSkulls), str(averageLevels), str(averageHonor), lastupdated]):
            if val != "":
                cell_list[i].value = val
        sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
        row +=1
