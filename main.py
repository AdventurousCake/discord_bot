import asyncio
import os
import sys
import logging
from datetime import datetime

import aiohttp
from discord.ext import commands
from sqlalchemy import update


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

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from db_init import Base, async_session, engine
from db_models import User

intents = discord.Intents.default()
intents.members = True
intents.bans = True
bot = commands.Bot(command_prefix='/', intents=intents)

async def db_create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# engine = create_async_engine(f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}/{config.db_name}",
#                              future=True)
# await db_init(engine)
# async_sessionmaker = sessionmaker(
#     engine, expire_on_commit=False, class_=AsyncSession
# )

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

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi **{member.name}**, welcome to the server! Have a great time!')
    logging.info(f"User is joined: {member}")


@bot.event
async def on_member_remove(member):
    logging.info(f"User is leave: {member}")


@bot.event
async def on_member_update(before, after):
    id = after.id
    print(str(after) + f"\n{id}")
    logging.info(f"User upd profile: {after.name}")


@commands.has_permissions(kick_members=True)
@bot.command(name="kick")
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.kick(reason=reason)
    kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await ctx.message.delete()
    await ctx.channel.send(embed=kick)
    await user.send(embed=kick)
    logging.info(f"User kick: {user.display_name}")


@commands.has_permissions(ban_members=True)
@bot.command(name="ban")
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.ban(reason=reason)
    em = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await ctx.message.delete()
    await ctx.channel.send(embed=em)
    await user.send(embed=em)
    logging.info(f"User ban: {user.display_name}")


@commands.has_permissions(ban_members=True)
@bot.command(name="unban")
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.unban(reason=reason)
    logging.info(f"User unban: {user.display_name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    name = message.author.display_name
    message_text_l = message.content.lower()
    message_text_l_split = message_text_l.split()
    message_text_raw_split = message.content.split()

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if message_text_l.startswith('/hello'):
        await message.channel.send('Hello!')

    elif message_text_l.startswith('/help'):
        help = ''' Useful commands:

		'''
        await message.channel.send(help)

    await bot.process_commands(message)
    await save_history(user_id, name)
    await check_level_progress()


async def check_level_progress(id=None):
    data = int("123")
    if data % int(config.PROGRESS_USER_MSG_COUNT) == 0:
        # inc level
        return "SEND"


# async def get_db_data():
#     async with async_sessionmaker() as session:
#         q = select(User.msg_count)
#         result = await session.execute(q)
#         res = result.scalars().all()


async def save_history(id, username, session=async_session):
    async with session() as session:
        new_user = User(id=id, username=username, msg_count=0, date=datetime.now())
        session.add(new_user)
        # await self.db_session.flush()

        if id:
            q = update(User).where(User.id == id)
            q = q.values(msg_count=(User.msg_count + 1))
            await session.execute(q)

        await session.commit()
        logging.debug("db write done")


async def get_all_user_lvl(session=async_session):
    async with session() as session:
        q = await session.execute(select(User, User.lvl).order_by(User.lvl))
        return q.scalars().all()


async def req():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
            if request.status == 200:
                data = await request.json()


def isadmin(uid):
    '''Return True if user is a bot admin, False otherwise.'''
    return True if uid in config.ADMINS_IDS else False


async def main():

    await db_create(engine)
    await bot.start(config.TOKEN)


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
