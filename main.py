import os
import discord
from dotenv import load_dotenv
import deck_scraper
import deck_review
import random
import asyncio

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

draft_state = {}
draft_order = []
max_decks = 0


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global draft_state, draft_order, max_decks
    # test only
    if message.content.startswith('!test'):
        if "Admin" not in [role.name for role in message.author.roles]:
            await message.channel.send("You do not have permission to use this command.")
            return
        await message.delete()
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
        await message.delete()
        command, url, *archetype = message.content.split()
        archetype = ' '.join(archetype)
        user_deck = deck_scraper.scrape_decks(url)
        archetype_deck1 = deck_review.scrape_yugipedia(archetype)
        archetype_deck2 = deck_review.scrape_yugioh_archetype(archetype)
        combined_archetype_search = archetype_deck1 + archetype_deck2
        percentage = deck_review.count_cards(user_deck, combined_archetype_search)
        print(f'{message.author.name}\'s archetype is {archetype}')
        print(user_deck)
        await message.channel.send(
            f"Your deck matches {percentage}% of the archetype. {message.author.mention}")
        private_channel_id = 1237166172328296500
        private_channel = client.get_channel(private_channel_id)
        await private_channel.send(f"Deleted message from {message.author.name}: {message_content}")

    if message.content.startswith('!draft'):
        if "Admin" not in [role.name for role in message.author.roles]:
            await message.channel.send("You do not have permission to use this command.")
            return

        _, num_decks = message.content.split()
        max_decks = int(num_decks)

        role = discord.utils.get(message.guild.roles, name="Participant")
        participants = [member for member in message.guild.members if role in member.roles]

        random.shuffle(participants)

        draft_state = {participant.id: [] for participant in participants}
        draft_order = [participant.id for participant in participants]

        await message.channel.send(f"Draft started. Order is: {', '.join([str(client.get_user(user_id)) for user_id in draft_order])}")

    elif message.content.startswith('!pick'):
        if message.author.id not in draft_order:
            await message.channel.send("You are not part of the current draft.")
            return

        if message.author.id != draft_order[0]:
            await message.channel.send("It's not your turn to pick.")
            return

        _, deck = message.content.split()

        draft_state[message.author.id].append(deck)

        if len(draft_state[message.author.id]) >= max_decks:
            draft_order.remove(message.author.id)

        if draft_order:
            await message.channel.send(f"{deck} picked by {message.author.mention}. Next up is {client.get_user(draft_order[0]).mention}")
        else:
            await message.channel.send("Draft complete. Here are the picks:")
            for user_id, decks in draft_state.items():
                await message.channel.send(f"{client.get_user(user_id).mention}: {', '.join(decks)}")

        # Rotate the draft order
        draft_order = draft_order[1:] + draft_order[:1]


client.run(TOKEN)
