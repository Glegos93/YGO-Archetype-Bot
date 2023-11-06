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


@client.event
async def on_message(message):
    # test only
    if message.content.startswith('!test'):
        await message.channel.send("it worked")
    if message.content.startswith("!join"):
        role = discord.utils.get(message.guild.roles, name="Participant")
        if role in message.author.roles:
            await message.channel.send("You are already participating")
            return
        await message.author.add_roles(role)
        await message.channel.send("Welcome to the season!")
    if message.content.startswith('!reset'):
        if "Admin" not in [role.name for role in message.author.roles]:
            await message.channel.send("You do not have permission to use this command.")
            return
        role = discord.utils.get(message.guild.roles, name="Participant")
        for member in message.guild.members:
            if role in member.roles:
                await member.remove_roles(role)
        await message.channel.send("Season over!")


client.run(TOKEN)
