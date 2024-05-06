import os
import discord
from dotenv import load_dotenv
import deck_scraper
import deck_review

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

    if message.content.startswith('!participants'):
        if "Admin" not in [role.name for role in message.author.roles]:
            await message.channel.send("You do not have permission to use this command.")
            return
        role = discord.utils.get(message.guild.roles, name="Participant")
        members = []
        for member in message.guild.members:
            if role in member.roles:
                members.append(member.mention)

        message_text = "Current participants: " + ", ".join(members)

        await message.channel.send(message_text)
    if message.content.startswith('!review'):
        command, url, *archetype = message.content.split()
        archetype = ' '.join(archetype)
        user_deck = deck_scraper.scrape_decks(url)
        archetype_deck = deck_review.get_card_ids(archetype)
        archetype_deck1 = deck_review.scrape_yugipedia(archetype)
        archetype_deck2 = deck_review.scrape_yugioh_archetype(archetype)
        print(archetype_deck1)
        percentage = deck_review.count_cards(user_deck, archetype_deck)
        await message.channel.send(f"Your deck matches {percentage}% of the {archetype} archetype.")


client.run(TOKEN)
