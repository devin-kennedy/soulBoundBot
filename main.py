import discord
from discord.ext import commands, tasks
from pretty_help import DefaultMenu, PrettyHelp
import os
import requests

TOKEN = os.environ["DISCORD_AUTH"]
menu = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌")
bot = commands.Bot(command_prefix="sb.", intents=discord.Intents.all())
bot.help_command = PrettyHelp(menu=menu)


# When the bot is turned on, print out bot has connected
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord")
    check_server.start()


# Every 2 minutes, check the web server for new badge earns
@tasks.loop(minutes=2)
async def check_server():
    # Define the channel to send updates in
    channel = bot.get_channel(884899768617300008)
    # Get the data
    r = requests.get("https://soulbound.llaamaguy.repl.co/data")
    # Parse and send the data to the defined channel
    data = r.json()['response']

    print(data)

    for player in data:
        await channel.send(str(player['username']) + " just got the " + str(player['badge']) + " badge")


bot.run(TOKEN)
