# bot.py
import os
import random
import aiohttp 
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = "https://discordapp.com/api/v6"
bot = commands.Bot(command_prefix='!')
HEADERS = {"Authorization": f"Bot {TOKEN}"}
CH_MESSAGES_ENPOINT = "/channels/{}/messages"

EMOJIS = {
    280681300979875851: '<:pulaski:592759530413359114>',
    430429972335820830: '<:549:668222219440095232>',
    372409036697632769: '<:honest_svyat:612182073746128899>',
    283961621527789569: '<:inenashl:592759647681642509>',
    433348482380595200: '<:filthy_junior:605808972812910660>',
    314757056290750466: '<:filthy_andrew:600362958840659971>',
    297357551891251202: '<:ljoda:659738402001780766>',
    448774769907859456: '<:mistrustful_mark:615967368199405579>',
    678587319867015189: '<:ljoda:659738402001780766>',
}


class MessageAnalizator:
    def __init__(self, messages):
        self.messages = messages
    
    def get_number_of_messages_by_author(self):
        authors = {}
        for message in self.messages:
            username = message["author"]["username"]
            author_id = int(message["author"]["id"])
            username = f"{EMOJIS.get(author_id, '<:shozanonames:536162051232497684>')} {username}"
            if username not in authors:
                authors.update(
                    {username: 1}
                )
            else:
                authors[username] = authors[username] + 1

        return authors

    def get_number_of_emojis(self):
        authors = {}
        for message in self.messages:
            username = message["author"]["username"]
            author_id = int(message["author"]["id"])
            username = f"{EMOJIS.get(author_id, '<:shozanonames:536162051232497684>')} {username}"
            if username not in authors:
                authors.update(
                    {username: 1}
                )
            else:
                authors[username] = authors[username] + 1

        return authors


@bot.command(name='get_channel_messages', help='gets stats')
async def get_channel_messages(ctx):
    messages = []
    async with aiohttp.ClientSession() as session:
        url = f"{URL}{CH_MESSAGES_ENPOINT.format(str(ctx.channel.id))}?limit=100"
        while True:
            async with session.get(url, headers=HEADERS) as resp:
                print(resp.status)
                response = await resp.json()
                if not response or resp.status != 200:
                    break
                messages.extend(response)
                url = url.split("&before=")[0] + "&" + f"before={response[-1]['id']}"
                print(url)
    by_author = MessageAnalizator(messages).get_number_of_messages_by_author()
    for k, v in by_author.items():
        await ctx.send(f"{k}: {v}")


@bot.command(name='get_channel_stats', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')




bot.run(TOKEN)