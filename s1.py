import asyncio
import sys
import os
 
import aiohttp
import discord
 
"""beamng-mp only"""
# CONFIG Standalone mode:
# BOT_TOKEN = ""  # https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
# IP = "" 
# PORT = ""

# CONFIG Docker mode:
BOT_TOKEN = os.environ['token']
IP = os.environ['ip']
PORT = os.environ['port']

class LivePlayercountBot(discord.Client):
    """Discord bot to display the beamng-mp server's playercount in the bot status"""
 
    async def on_ready(self):
        print(f"Logged on as {self.user}\n" f"Started monitoring server {IP}:{PORT}")
        status = ""
        async with aiohttp.ClientSession() as session:
            while True:
                newstatus = await get_playercount(session)
                if newstatus != status:  # avoid spam to the discord API
                    await self.change_presence(activity=discord.Game(newstatus))
                    status = newstatus
                await asyncio.sleep(60) # time before next request
 
 
async def get_playercount(session):
    try:
        url = "https://beamng-mp.com/servers-info"
        async with session.get(url) as r:
            page = await r.json()
            for i in range(len(page)):
                if page[i][f"{i}"]["ip"] == IP and page[i][f"{i}"]["port"] == PORT:
                    playerlist = page[i][f"{i}"]["players"]
                    maxplayers = page[i][f"{i}"]["maxplayers"]
                    map = page[i][f"{i}"]["map"].replace("/levels/", "").replace("/info.json", "").replace("_"," ")
                    break
            return f"{playerlist}/{maxplayers} players - {map.capitalize()}"  # discord status message
    except Exception as e:
        print(f"Error getting data from beamng-mp.com: {e}")  # Failed to get info
 
 
if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Script requires Python 3.7+"
    assert IP and PORT and BOT_TOKEN, "Config is empty, pls fix"
    print("Initiating bot")
    LivePlayercountBot().run(BOT_TOKEN)