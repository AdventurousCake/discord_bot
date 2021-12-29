import os
import sys
import logging
from discord.ext import commands
import config
import discord

# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
# client = discord.Client()

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)


# G ID 925307289433415700


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == 'GUILD':
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # guild = discord.utils.find()

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    pass


@bot.event
async def on_member_update(before, after):
    id = after.id
    print(str(after)+f"\n{id}")

# discord.on_member_remove(member)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if msg.startswith('/hello'):
        await message.channel.send('Hello!')

    elif msg.startswith('/help'):
        await message.channel.send('Hello! Im a bot')

    check_level_progress()


def check_level_progress():
    pass


@bot.command(name='hi')
async def hello(ctx):
    await ctx.send("HI")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.run(config.TOKEN)
