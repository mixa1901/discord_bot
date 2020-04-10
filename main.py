import random
import datetime
import discord
from datetime import datetime
from constants import TOKEN, EMOJIS
from discord.ext import commands
from utils import get_messages_by_channel

bot = commands.Bot(command_prefix='!')

class Author:
    def __init__(self, author_id, username):
        self.author_id = author_id
        self.username = username
        self.emoji = EMOJIS.get(self.author_id, '<:shozanonames:536162051232497684>')

    def __eq__(self, other):
        return self.author_id == other.author_id 
    
    def __hash__(self):
        return hash(self.author_id)

class MessageAnalizator:
    def __init__(self, messages):
        self.messages = messages
    
    def get_number_of_messages_by_author(self):
        message_total = 0
        authors = {}
        for message in self.messages:
            username = message["author"]["username"]
            author_id = int(message["author"]["id"])
            print(author_id)
            author = Author(author_id, username)
            if author in authors:
                authors[author] += 1 
            else:
                authors.update({author: 1})
            message_total += 1
        
        return {
            "authors": authors,
            "total": message_total
        }

    def get_number_of_emojis(self):
        emoji_total = 0
        emojis = {
            
        }
        for message in self.messages:
            reactions = message.get("reactions", [])
            for reaction in reactions:
                emo_id = reaction["emoji"]["id"]
                if not emo_id:
                    continue
                emo_name = reaction["emoji"]["name"]
                emo_count = reaction["count"]
                emoji = f"<:{emo_name}:{emo_id}>"
                if emoji in emojis:
                    emojis[emoji] += emo_count
                else:
                    emojis.update({emoji: 1})
                emoji_total += emo_count

        return {
            "emojis": emojis,
            "total": emoji_total
        }


@bot.command(name='messages_stats', help='gets stats')
async def messages_stats(ctx):
    messages = await get_messages_by_channel(ctx.channel.id)
    by_author = MessageAnalizator(messages).get_number_of_messages_by_author()
    for author, amount in by_author["authors"].items():
        await ctx.send(f"{author.emoji} {author.username}: {amount}")
    total = str(by_author["total"])
    await ctx.send(f"TOTAL MESSAGES: {total}")
    
    
@bot.command(name='emojis_stats', help='gets stats')
async def emojis_stats(ctx):
    messages = await get_messages_by_channel(ctx.channel.id)
    stats = MessageAnalizator(messages).get_number_of_emojis()
    for emoji, amount in stats["emojis"].items():
        await ctx.send(f"{emoji}: {amount}")
    total = str(stats["total"])
    await ctx.send(f"TOTAL REACTIONS USED: {total}")

@bot.command(name='server_stats', help='gets stats')
async def server_stats(ctx):
    members = ctx.guild.members
    for member in members:
        await ctx.send(f'{EMOJIS.get(member.id, "<:shozanonames:536162051232497684>")} {member.display_name} приєднався {member.joined_at.strftime("%d/%m/%Y, %H:%M:%S")}')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за пабом"))

bot.run(TOKEN)