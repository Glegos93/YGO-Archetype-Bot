import os
import discord
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


async def on_message(message):
    if message.author == client.user:
        return

client.run(TOKEN)
