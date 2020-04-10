import aiohttp 
from constants import HEADERS, URL, CH_MESSAGES_ENPOINT



async def get_messages_by_channel(channel_id):
    messages = []
    async with aiohttp.ClientSession() as session:
        url = f"{URL}{CH_MESSAGES_ENPOINT.format(str(channel_id))}?limit=100"
        while True:
            async with session.get(url, headers=HEADERS) as resp:
                print(resp.status)
                response = await resp.json()
                if not response or resp.status != 200:
                    break
                messages.extend(response)
                url = url.split("&before=")[0] + "&" + f"before={response[-1]['id']}"
                print(url)
    return messages
