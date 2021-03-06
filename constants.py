import os
from dotenv import load_dotenv

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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URL = "https://discordapp.com/api/v6"
HEADERS = {"Authorization": f"Bot {TOKEN}"}
CH_MESSAGES_ENPOINT = "/channels/{}/messages"