import discord
import time
from discord.ext import commands
import datetime
 
# Intializes bot and it's options.
token = ''
prefix = '*'
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=True)

@bot.event
async def on_ready():
    print(f"clearcord is running.")
    # Delete messages older than 30 days
    before_date = datetime.datetime.today() - datetime.timedelta(days=30)

    await clear_dm(before_date)
    await clear_servers(before_date)
    
    print("\nDone!")

def is_me(m):
    return m.author == bot.user

async def clear_dm(before_date):
    for friend in bot.user.friends:
        message_count = 0
        friend_channel = bot.get_user(int(friend.id))
        async for message in friend_channel.history(limit=None, oldest_first=True):
            if message.author == bot.user:
                if message.created_at < before_date:
                    message_count+=1
                    try:
                        await message.delete()
                        pass
                    except:
                        print(f"didnt delete message {friend.name}:{message.created_at}:{message.content}" + "\n")
                        print()
        print(f'{message_count} messages deleted in {friend.name}\'s channel')

async def clear_servers(before_date):
    for server in bot.guilds:
        print(f"Looking in {server}..")
        for channel in server.text_channels:
            try:
                deleted = await channel.purge(limit=10000, check=is_me, bulk=True, before=before_date)
                if len(deleted) > 0:
                    print(f"{server} - {channel} : {len(deleted)} messages")
                    for m in deleted:
                        print(f"\t{server}@{channel}:{m.created_at}:{m.content}")
            except:
                # print(f"Can't check in {server} - {channel}")
                continue

    
bot.run(token, bot=False)