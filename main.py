import asyncio
import io
import os
import sys
import logging
from datetime import datetime
import aiohttp
from discord.ext import commands
from sqlalchemy import update, insert
import config
import discord

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

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


@bot.event
async def on_ready():
    await db_create(engine)

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

    if message_text_l.startswith('/hello'):
        await message.channel.send('Hello!')

    elif message_text_l.startswith('/help'):
        help = '''Bot commands:
        /listgames
        /kick
        /ban
        /unban
		'''
        await message.channel.send(help)

    elif message_text_l.startswith('/lvl'):
        await message.channel.send(get_all_user_lvl())

    elif message_text_l.startswith('/listgames'):
        await message.channel.send("List of games")
        async with aiohttp.ClientSession() as session:
            async with session.get('https://i.ibb.co/z2nZ57Z/123.jpg') as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'cool_image.png'))

    await bot.process_commands(message)
    await save_history(user_id, name, message=message)


def check_level_progress(id=None, data=None):
    if data % int(config.PROGRESS_USER_MSG_COUNT) == 0:
        return True
    else:
        return False


async def save_history(id, username, session=async_session, message=None):
    async with session() as session:
        q = insert(User).values(id=id, username=username, date=datetime.now()).on_conflict_do_nothing()
        session.execute(q)
        # await self.db_session.flush()

        if id:
            q = update(User).where(User.id == id)
            q = q.values(msg_count=(User.msg_count + 1))
            await session.execute(q)

        q = select(User.msg_count, User.lvl).where(User.id == id)
        result = await session.execute(q)
        result = result.one()

        msg_count = result[0]
        lvl = result[1]

        if check_level_progress(data=msg_count):
            q = update(User).where(User.id == id)
            q = q.values(lvl=(User.lvl + 1))
            await session.execute(q)

            await message.channel.send(f'{username} is reached {lvl} LVL 🎉')

        await session.commit()
        logging.debug("db write done")


def isadmin(uid):
    '''Return True if user is a bot admin, False otherwise.'''
    return True if uid in config.ADMINS_IDS else False


if __name__ == '__main__':
    bot.run(config.TOKEN)
