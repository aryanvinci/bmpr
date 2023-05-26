import os
import asyncio
import requests
import random
import time
import datetime
import sys
import threading
from webserver import keep_alive
import pytz
try:
    __import__("discum")
    import discum
    from discum.utils.slash import SlashCommander
    from discum.utils.button import Buttoner
except ImportError:
    os.system(
        "python -m pip install --upgrade git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum"
    )
    import discum
    from discum.utils.slash import SlashCommander
    from discum.utils.button import Buttoner


token = os.environ["token"]
disbot = discum.Client(token=token, log=False)

guildID = os.environ["guild_id"]
channelID = os.environ["channel_id"]
botID = "302050872383242240"


def gtway():
  disbot.gateway.run()

def gtwaythread():
    x = threading.Thread(target=gtway,daemon=True)
    x.start()
"""    print("Waiting for gateway thread to finish.")
    x.join()"""

def loopthread():
    x = threading.Thread(target=loop,daemon=True)
    x.start()
"""    print("Waiting for loop thread to finish.")
    x.join()"""

count = 0
data = None
hookurl = os.environ["webhook"]

def sendhook(url,content):
  if "http" in url:
    embed = {
    "description": str(content),
    "title": "Disboard Bump Selfbot"
    }
    data = {
    #"content": "message content",
    "username": """vincis selfbot""",
    "embeds": [
        embed
        ],
}
    headers = {
    "Content-Type": "application/json"
}
    result = requests.post(url, json=data, headers=headers)
    if 200 <= result.status_code < 300:
      print(f"Webhook sent {result.status_code}")
    else:
      print(f"Not sent with {result.status_code}, response:\n{result.json()}")
  else:
    print("Webhook url not set")

def loop():
  while True:
    global count
    global data
    if data != None:
      disbot.triggerSlashCommand(botID, channelID=channelID, guildID=guildID, data=data, sessionID=disbot.gateway.session_id)
      channel = disbot.getChannel(f'{channelID}')
      count+=1
      channeljson = channel.json()
      print(f"\n[ {count} ] Bump Sent in {channeljson.get('name')}!\n")
      randnumbr = random.randint(8234,11011)
      datenow = datetime.datetime.now(tz=pytz.timezone('Europe/Bucharest'))
      datethen = datetime.timedelta(seconds=randnumbr)
      timethen = datenow + datethen
      xyz = f"Waiting {randnumbr} seconds as cooldown. [ next /bump at: {timethen} ]"
      print(xyz)
      sendhook(url=hookurl,content=xyz)
      time.sleep(randnumbr)
    else:
      print("Waiting for slash commands...")
      time.sleep(1)



def slashCommand(resp, guildID, channelID, botID):
  global data
  if resp.event.ready_supplemental:
    disbot.gateway.request.searchSlashCommands(guildID, limit=10, query="bump")
  if resp.event.guild_application_commands_updated:
    disbot.gateway.removeCommand(slashCommand)
    slashCmds = resp.parsed.auto()['application_commands']
    s = SlashCommander(slashCmds, application_id=botID)
    data = s.get(['bump'])


disbot.gateway.command(
    {
        "function": slashCommand,
        "params": {"guildID": guildID, "channelID": channelID, "botID": botID},
    }
)




if __name__ == "__main__":
    keep_alive()
    print("Started webserver thread.")
    gtwaythread()
    print("Started gateway thread.")
    loopthread()
    print("Started loop thread.")
