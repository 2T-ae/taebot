import discord
import asyncio
import random
import os
import datetime
import shutil
import json
import youtube_dl
import math
import functools
import itertools
import aiohttp
import sys
import requests
from pytz import timezone
from discord import member
from discord import embeds
from discord import activity
from discord import Spotify
from discord.enums import ActivityType
from discord.ext.commands.converter import _get_from_guilds
from async_timeout import timeout
from discord import message
from discord import colour
from discord import channel
from discord import gateway
from discord import user
from discord import client
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands.core import Command, has_permissions
from discord.flags import alias_flag_value
from discord.user import User
from discord.utils import get
from discord.ext.commands.errors import BadArgument, ChannelNotFound, CommandError, CommandInvokeError, CommandNotFound, MissingPermissions, MissingRequiredArgument, NotOwner
from discord.mentions import AllowedMentions
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashCommand
from folder.config import *
from discord.team import TeamMember

def get_prefix(bot, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix = get_prefix, intents = intents)
bot.remove_command('help')
owner = 298333126143377419
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
yes_gif = '<:a:yes_gif:863076896224575488>'
no_gif = '<:a:no_gif:851837941910208553>'

cogs = []
path = "./folder/cogs"

for filename in os.listdir(path):
    if filename.endswith('.py'):
        cogs.append(filename)
        bot.load_extension(f'folder.cogs.{filename[:-3]}')
    if filename == '__pycache__':pass

@bot.event
async def on_ready():
    # 프로그램 실행 시 초기 구성  
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.loop.create_task(status_task())

@bot.event
async def status_task():
   while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="&help를 입력해보세요!"))
        await asyncio.sleep(12)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="{}개의 서버와 함께해요!".format(len(bot.guilds))))
        await asyncio.sleep(12)
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="&play"))
        await asyncio.sleep(12)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="{}명의 유저와 함께해요!".format(len(bot.users))))
        await asyncio.sleep(12)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='Tae 0.1V'))
        await asyncio.sleep(12)

@bot.event
async def on_command_error(ctx: commands.Context, exception: Exception):
    print(f'Command raised an exception: {type(exception).__name__} : {exception}')

@bot.event
async def on_guild_join(guild):
    # 서버에 들어갔을 때 설정될 prefix


    with open("prefixes.json", "r", encoding='utf-8') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "&"

    with open("prefixes.json", "w", encoding='utf-8') as f:
        json.dump(prefixes,f)
    
    #서버에 들어갔을 때 설정될 공지 채널


    with open("announce.json", "r", encoding='utf-8') as f:
        announce = json.load(f)

    announce[str(guild.id)] = None

    with open("announce.json", "w", encoding='utf-8') as f:
        json.dump(announce,f)

    #서버에 들어갔을 때 전송할 메세지
    tae = await bot.get_user(298333126143377419).create_dm()
    joinem = discord.Embed(title='Joined Server', description='', color=0x00ff95)
    joinem.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
    joinem.set_footer(text=f'\u200b')
    joinem.add_field(name=f'Name: {guild.name}', value=f'Owner: {guild.owner}', inline=False)
    await tae.send(embed = joinem)
    print(f'Joined to {guild.name}')
    firstchannel = discord.utils.get(guild.text_channels, position=0)
    embed = discord.Embed(title='초대 완료', description='', color=0x00ff95)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name='Tae를 사용 해주셔서 감사합니다!', value='Tae의 접두사는 `&`입니다!\n자세한 봇의 사용법을 보시려면 `&help` 명령어를 사용해보세요!', inline=False)
    embed.set_footer(text='(C) 2021 Tae, All rights reserved.')
    await firstchannel.send(embed = embed)

@bot.event
async def on_member_join(member):
    # 서버에 사람이 들어왔을 때 출력될 Welcome 메세지


    with open("welcome.json", "r", encoding='utf-8') as f:
        welcome_dict = json.load(f)

    welcome = welcome_dict[str(member.guild.id)]
    await bot.get_channel(int(welcome)).send(f'`{member}({member.id})`님이 서버에 들어왔습니다.')

@bot.event
async def on_member_remove(member):
    # 서버에서 사람이 나갔을 때 출력될 Leave 메세지
    with open("leave.json", "r", encoding='utf-8') as f:
        leave_dict = json.load(f)

    leave = leave_dict[str(member.guild.id)]
    await bot.get_channel(int(leave)).send(f'`{member}`님이 서버에서 나가셨습니다.')

@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
    # changeprefix 명령어를 통해 prefix 변경

    with open("prefixes.json", "r", encoding='utf-8') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w", encoding='utf-8') as f:
        json.dump(prefixes,f)

    await ctx.send(f'The prefix was changed to `{prefix}`. | Default = `&`')

@bot.command()
@commands.has_permissions(administrator = True)
async def 공지채널(ctx, channel: discord.TextChannel):
    # 공지채널 명령어를 통해 공지를 보낼 채널 변경

    with open("announce.json", "r", encoding='utf-8') as f:
        announce = json.load(f)

    announce[str(ctx.guild.id)] = str(channel.id)

    with open("announce.json", "w", encoding='utf-8') as f:
        json.dump(announce,f)

    await ctx.send(f'{ctx.message.guild.name} 서버의 공지 채널이 `{channel.name}`로 설정되었습니다. | Default = `None`')

@bot.command()
@commands.has_permissions(administrator = True)
async def 입장(ctx, channel: discord.TextChannel):
    # 입장 명령어를 통해 welcome 메세지가 전송될 채널 변경

    with open("welcome.json", "r", encoding='utf-8') as f:
        welcome = json.load(f)

    welcome[str(ctx.guild.id)] = str(channel.id)

    with open("welcome.json", "w", encoding='utf-8') as f:
        json.dump(welcome,f)

    await ctx.send(f'{ctx.message.guild.name} 서버의 입장 로그 채널이 `{channel.name}`로 설정되었습니다. | Default = `None`')

@bot.command()
@commands.has_permissions(administrator = True)
async def 퇴장(ctx, channel: discord.TextChannel):
    # 퇴장 명령어를 통해 leave 메세지가 전송될 채널 변경

    with open("leave.json", "r", encoding='utf-8') as f:
        leave = json.load(f)

    leave[str(ctx.guild.id)] = str(channel.id)

    with open("leave.json", "w", encoding='utf-8') as f:
        json.dump(leave,f)

    await ctx.send(f'{ctx.message.guild.name} 서버의 퇴장 로그 채널이 `{channel.name}`로 설정되었습니다. | Default = `None`')

@bot.event
async def on_message(msg):
    # 멘션만 받게 된다면 해당 서버의 prefix를 출력함

    try:

        if msg.mentions[0] == bot.user:
            
            with open("prefixes.json", "r", encoding='utf-8') as f:
                prefixes = json.load(f)

            pre = prefixes[str(msg.guild.id)]

            await msg.channel.send(f'My prefix for this server is `{pre}`! | Default = `&`')

    except:
        pass

    await bot.process_commands(msg)

@bot.command()
async def help(ctx, *, args=None):
    if args is None:
        embed = discord.Embed(title='TaeBot Help', description=' ', color=0xFAFD40)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='Commands', value='`&help commands`', inline=True)
        embed.add_field(name='Music', value='`&help music`', inline=True)
        embed.add_field(name='Moderator', value='`&help moderator`', inline=True)
        embed.add_field(name='Slash', value='`&help slash`', inline=True)
        await ctx.send(embed = embed)
    if args == 'commands':
        # help commands를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Commands', description=' ', color=0xFAFD40)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`invite`', value='봇 초대링크를 받을 수 있습니다.', inline=True)
        embed.add_field(name='`&avatar`', value='프로필 이미지를 얻을 수 있습니다.', inline=True)
        embed.add_field(name='`&userinfo or &내정보`', value='디스코드 계정에 대한 정보를 얻을 수 있습니다. (ex. 계정 생성일, 서버 접속일, 현재 활동, 소유중인 역할 등)', inline=True)
        embed.add_field(name='`&lyric or &가사`', value='&가사 아티스트 제목 으로 노래 가사를 검색할 수 있습니다.', inline=True)
        embed.add_field(name='`&gcreate`', value='&gcreate <시간> <상품> 으로 Giveaway를 만듭니다. (ex. 5s, 5m, 5h, 5d)', inline=True)
        await ctx.send(embed = embed)
    if args == 'music':
        # help music를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Music', description=' ', color=0xFAFD40)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`&join`', value='음성채널에 접속합니다', inline=True)
        embed.add_field(name='`&p <이름 혹은 url>`', value='노래를 재생합니다', inline=True)
        embed.add_field(name='`&q`', value='플레이리스트를 보여줍니다', inline=True)
        embed.add_field(name='`&skip`', value='재생 중인 노래를 건너 뛸 수 있습니다', inline=True)
        embed.add_field(name='`&pause`', value='재생 중인 노래를 일시정지 시킵니다', inline=True)
        embed.add_field(name='`&resume`', value='일시정지시켰던 노래를 다시 재생할 수 있습니다', inline=True)
        embed.add_field(name='`&np`', value='재생중인 음악의 정보를 알려줍니다', inline=True)
        await ctx.send(embed = embed)
    if args == 'moderator':
        # help moderator를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Moderator', description=' ', color=0xFAFD40)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`&공지`', value='&공지 <할 말> 을 통해 서버에 공지를 보낼 수 있습니다. <공지채널 명령어를 통한 채널 설정 필요> \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&공지채널`', value='&공지채널 #채널 을 통해 공지를 보낼 채널을 설정할 수 있습니다. \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&청소`', value='&청소 <청소 할 메세지의 갯수> 를 통해 메세지를 청소할 수 있습니다. \n\n필요한 권한 : Manage Messages', inline=True)
        embed.add_field(name='`&입장`', value='&입장 #채널 을 통해 입장로그를 보낼 채널을 설정 할 수 있습니다. \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&퇴장`', value='&퇴장 #채널 을 통해 퇴장로그를 보낼 채널을 설정 할 수 있습니다. \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&changeprefix`', value='&changeprefix <봇을 사용할 칭호> 를 통해 서버에서 Tae봇을 사용할 때 쓸 칭호를 설정할 수 있습니다. 기본 : & \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&slowmode`', value='&slowmode <초> 를 통해 해당 채널에 슬로우모드를 걸 수 있습니다. \n\n필요한 권한 : Manage Channels', inline=True)
        embed.add_field(name='`&nuke`', value='해당 명령어를 사용한 채널을 복제 후 삭제시킵니다. \n\n필요한 권한 : Administrator', inline=True)
        await ctx.send(embed = embed)
    if args == 'slash':
        # help slash를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Slash', description=' ', color=0xFAFD40)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`/가사`', value='/가사 아티스트 제목 으로 노래 가사를 검색할 수 있습니다.', inline=True)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def gcreate(ctx, time=None, *, prize=None):
    if time == None:
        return await ctx.send('시간을 올바르게 입력해주세요!')
    elif prize == None:
        return await ctx.send('상품을 올바르게 입력해주세요!')
    embed = discord.Embed(title='New Giveaway!', description=f'{ctx.author.mention} is giving away **{prize}**!')
    time_convert = {'s':1, 'm':60, 'h':3600, 'd':86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f'Host: {ctx.author} | Ends in {time}')
    await ctx.channel.purge(limit=1)
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction('🎉')
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    print(users)
    users.pop(users.index(bot))

    winner = random.choice(users)

    await ctx.send(f'Congratulations {winner.mention}! You won the **{prize}**')

@bot.command(aliases=['slowmode'])
@commands.has_permissions(manage_channels=True)
async def 슬로우(ctx, time):
    time = int(time)
    if time == 0:
        await ctx.send(f'🛠{ctx.message.channel.mention} 채널의 슬로우 모드가 `{time}초`로 설정되었습니다.')
        await ctx.channel.edit(slowmode_delay = 0)
    elif time > 21600:
        await ctx.send(f'{ctx.author.mention}, 초는`0(끄기) ~ 21600(6시간)`으로 입력해주세요.')
    else:
        await ctx.channel.edit(slowmode_delay = time)
        await ctx.send(f'🛠{ctx.message.channel.mention} 채널의 슬로우 모드가 `{time}초`로 설정되었습니다.')

@bot.command(aliases=['announcement'])
@commands.has_permissions(administrator=True)
# 공지사항 embed 전송 명령어
async def 공지(ctx, *, arg):
    # 공지사항 embed를 전송할 채널 가져오기


    with open('announce.json', 'r', encoding='utf-8') as f:
        announce_dict = json.load(f)

        announce = announce_dict[str(ctx.guild.id)] 

        dm_channel = await ctx.message.author.create_dm()
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title='공지', description=' ', color=0xFAFD40)
        embed.add_field(name=(arg), value='** **', inline=False)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text='Sender: 'f'{ctx.message.author}', icon_url=ctx.author.avatar_url)
        await bot.get_channel(int(announce)).send(embed = embed)
        msg = await ctx.send(f'{ctx.message.author.mention}님에게 이번 공지에 대한 로그가 전송되었습니다.')
        embed2 = discord.Embed(title='Result', description=' ', color=0XFAFD40)
        embed2.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed2.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed2.add_field(name=f'`{arg}`' + ' 라는 메세지를 설정한 공지채널에 보냈습니다.', value='** **', inline=False)
        await dm_channel.send(embed = embed2)
        await asyncio.sleep(5)
        await msg.delete()

@bot.command(aliases=['봇공지', 'botannounce'])
@commands.is_owner()
# 봇 전체공지 명령어
async def 전체공지(ctx, args=None):
    for i in bot.guilds:
        channel = discord.utils.get(i.text_channels, topic='봇-공지')
        topchannel = discord.utils.get(i.text_channels, position=0)
        embed = discord.Embed(title='TaeBot 공지', description=f'{args}', color=0xFAFD40)
        embed.add_field(name=':link:[TaeBot 초대하기](https://discord.com/api/oauth2/authorize?client_id=837332366371979336&permissions=45444182&scope=bot)', value='** **')
        embed.set_footer(text=f'Sender: {ctx.message.author} - Verified\n다른 채널에 공지를 전송받고 싶다면 채널 주제에 \'봇-공지\'라고 적어주세요.', icon_url=ctx.message.author.avatar_url)
        if channel is None:
            await topchannel.send(embed = embed)
        else:
            await channel.send(embed = embed)

@bot.command()
@commands.is_owner()
# 봇이 들어가있는 서버 목록
async def guildlist(ctx):
    for i in bot.guilds:
        with open("guilds.json", "r", encoding='utf-8') as f:
            guilds = json.load(f)

        guilds["Name: " + str(i.name) + " / Owner: " + str(i.owner) + " / Guild Member Counts: " + str(i.member_count)] = "Guild ID: "+ str(i.id)

        with open("guilds.json", "w", encoding='utf-8') as f:
            json.dump(guilds,f,indent=4)

    try:
        embed = discord.Embed(title='Guild List ', description=f'{guilds}'.replace('{',"\n").replace('}',"\n").replace("',",'\n').replace("'",'').replace(': Guild ID',"\nGuild ID"), color=0xFDFA40)
        embed.set_footer(text=f'Bot in {len(bot.guilds)}')
        tae = await bot.get_user(bot.owner_id).create_dm()
        await tae.send(embed = embed)
        await ctx.message.add_reaction(yes_gif)
    except:
        pass

@bot.command()
@commands.is_owner()
# 봇이 서버를 나가게 하기
async def guildleave(ctx, *, guild_id):
    try:
        guildid = int(guild_id)
        guild = bot.get_guild(guildid)
        await guild.leave()
        tae = await bot.get_user(bot.owner_id).create_dm()
        await ctx.message.add_reaction('✅')
        embed = discord.Embed(title='Success', description='**Force Leave**', color=0x00ff95)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.add_field(name=f'\nName: {guild.name}\nID: {guild.id}\nGuild Owner: {guild.owner}\nMembers: {guild.member_count}', value='** **', inline=False)
        embed.set_footer(text=f'{ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        await tae.send(embed = embed)
    except CommandInvokeError:
        await ctx.message.add_reaction('❌')
        return

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    await ctx.send('`Nuclear Launch Detected.` 5초 뒤 채널을 터칩니다')
    await asyncio.sleep(1)
    count = await ctx.send('5')
    await asyncio.sleep(1)
    await count.edit(content='4')
    await asyncio.sleep(1)
    await count.edit(content='3')
    await asyncio.sleep(1)
    await count.edit(content='2')
    await asyncio.sleep(1)
    await count.edit(content='1')
    await asyncio.sleep(1)
    await count.edit(content='Execute.')
    await asyncio.sleep(1)
    channel = ctx.channel
    posit = channel.position
    new_channel = await channel.clone()
    await new_channel.edit(position=posit, sync_permissions=True)
    await channel.delete()
    await new_channel.send(f'Success. [{ctx.message.author.mention}]')

@bot.command(aliases=['clear'])
@commands.has_permissions(manage_messages=True)
async def 청소(ctx,amount:int):
    await ctx.channel.purge(limit=int(amount+1))
    msg = await ctx.send(f'{amount}개의 메세지를 청소했습니다!')
    await asyncio.sleep(5)
    await msg.delete()

@bot.command(aliases=['디엠'])
async def DM(ctx, userid, *, arg):
    user = await bot.get_user(int(userid)).create_dm()
    username = bot.get_user(int(userid))
    if arg is None:
            error_msg = await ctx.send('보낼 메세지를 제대로 입력해주세요')
            await asyncio.sleep(5)
            await error_msg.delete
    else:
        # DM을 발송한 사람에게 전송되는 Embed
        dm = await ctx.message.author.create_dm()
        await ctx.channel.purge(limit=1)
        msg = await ctx.send(f'{ctx.author.mention}, 성공적으로 메세지를 전송했습니다.')
        await asyncio.sleep(5)
        await msg.delete()
        embed2 = discord.Embed(title='발송한 메세지 기록', description=' ', color=0xFAFD40)
        embed2.add_field(name=(arg), value=f'Send to {username}', inline=False)
        await dm.send(embed = embed2)
        # 전송될 메세지 Embed
        embed = discord.Embed(title='Message', description=' ', color=0xFAFD40)
        embed.timestamp = datetime.datetime.now(timezone('Asia/Seoul'))
        embed.set_footer(text=f'Sender: {ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name=(arg), value='** **', inline=False)
        await user.send(embed = embed)

@bot.command(aliases=['av'])
async def avatar(ctx, member : discord.Member=None):
    if member is None:
        embed = discord.Embed(title='Avatar', description='')
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed)
        return
    else:
        embed2 = discord.Embed(title='Avatar', description='')
        embed2.set_image(url=member.avatar_url)
        embed2.set_author(name=f'{member}', icon_url=member.avatar_url)
        await ctx.send(embed = embed2)

@bot.command(aliases=['내정보'])
async def userinfo(ctx, *, user: discord.Member = None):
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    if user is None:
        user = ctx.author
        date_format = '%Y/%m/%d %H:%M:%S'
        status = user.status
        if status == discord.Status.online:
            status = 'Online | 온라인'
        elif status == discord.Status.idle:
            status = 'Idle | 자리 비움'
        elif status == discord.Status.dnd:
            status = 'Do Not Disturb | 다른 용무중'
        elif status == discord.Status.offline:
            status = 'Offline | 오프라인'

        info = embed = discord.Embed(color=0xdfa3ff, title='USER INFO')
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='현재 상태', value=status, inline=False)
        embed.add_field(name='계정 생성일', value=user.created_at.strftime(date_format), inline=False)
        embed.add_field(name='서버 접속일', value=user.joined_at.strftime(date_format), inline=False)
        embed.add_field(name='Bot', value=user.bot, inline=False)
        
        activ = user.activities
        if activ == ():
            pass
        elif len(user.activities) == 4:
            # Activity가 네개일때
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[1].type) == "ActivityType.playing":
                if user.activities[1].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\n ㄴ{activ[1].details}\n ㄴ{activ[1].state}\n__**`{activ[1].large_image_text}`**__ | `{activ[1].small_image_text}`')    
            elif str(user.activities[1].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[1].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[1].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[2].type) == "ActivityType.playing":
                if user.activities[2].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\n ㄴ{activ[2].details}\n ㄴ{activ[2].state}\n__**`{activ[2].large_image_text}`**__ | `{activ[2].small_image_text}`')    
            elif str(user.activities[2].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[2].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[2].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[3].type) == "ActivityType.playing":
                if user.activities[3].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 하는 중\n ㄴ{activ[3].details}\n ㄴ{activ[3].state}\n__**`{activ[3].large_image_text}`**__ | `{activ[3].small_image_text}`')    
            elif str(user.activities[3].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[3].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[3].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
        elif len(user.activities) == 3:
            # Activity가 세개일때
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[1].type) == "ActivityType.playing":
                if user.activities[1].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\n ㄴ{activ[1].details}\n ㄴ{activ[1].state}\n__**`{activ[1].large_image_text}`**__ | `{activ[1].small_image_text}`')    
            elif str(user.activities[1].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[1].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[1].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[2].type) == "ActivityType.playing":
                if user.activities[2].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\n ㄴ{activ[2].details}\n ㄴ{activ[2].state}\n__**`{activ[2].large_image_text}`**__ | `{activ[2].small_image_text}`')    
            elif str(user.activities[2].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[2].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[2].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
        elif len(user.activities) == 2:
            # Activity가 두개일때
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[1].type) == "ActivityType.playing":
                if user.activities[1].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\n ㄴ{activ[1].details}\n ㄴ{activ[1].state}\n__**`{activ[1].large_image_text}`**__ | `{activ[1].small_image_text}`')    
            elif str(user.activities[1].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[1].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[1].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            #Activity가 하나일때
        elif len(user.activities) == 1:
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)

        if len(user.roles) > 1:
            info.add_field(name='Highest Role', value=user.top_role.mention, inline=False)

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            print(role_string)
            info.add_field(name='Roles', value=role_string, inline=False)
        info.set_footer(text=f'#{members.index(user) + 1} • USER ID : ' + str(user.id))
        return await ctx.send(embed=embed)

    else:
        date_format = '%Y/%m/%d %H:%M:%S'
        status = user.status
        if status == discord.Status.online:
            status = 'Online | 온라인'
        elif status == discord.Status.idle:
            status = 'Idle | 자리 비움'
        elif status == discord.Status.dnd:
            status = 'Do Not Disturb | 다른 용무중'
        elif status == discord.Status.offline:
            status = 'Offline | 오프라인'

        info = embed = discord.Embed(color=0xdfa3ff, title='USER INFO')
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='현재 상태', value=status, inline=False)
        embed.add_field(name='계정 생성일', value=user.created_at.strftime(date_format), inline=False)
        embed.add_field(name='서버 접속일', value=user.joined_at.strftime(date_format), inline=False)
        embed.add_field(name='Bot', value=user.bot, inline=False)
        
        activ = user.activities
        if activ == ():
            pass
        elif len(user.activities) == 4:
            # Activity가 네개일때
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[1].type) == "ActivityType.playing":
                if user.activities[1].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\n ㄴ{activ[1].details}\n ㄴ{activ[1].state}\n__**`{activ[1].large_image_text}`**__ | `{activ[1].small_image_text}`')    
            elif str(user.activities[1].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[1].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[1].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[2].type) == "ActivityType.playing":
                if user.activities[2].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\n ㄴ{activ[2].details}\n ㄴ{activ[2].state}\n__**`{activ[2].large_image_text}`**__ | `{activ[2].small_image_text}`')    
            elif str(user.activities[2].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[2].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[2].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[3].type) == "ActivityType.playing":
                if user.activities[3].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 하는 중\n ㄴ{activ[3].details}\n ㄴ{activ[3].state}\n__**`{activ[3].large_image_text}`**__ | `{activ[3].small_image_text}`')    
            elif str(user.activities[3].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[3].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[3].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[3].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
        elif len(user.activities) == 3:
            # Activity가 세개일때
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[1].type) == "ActivityType.playing":
                if user.activities[1].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\n ㄴ{activ[1].details}\n ㄴ{activ[1].state}\n__**`{activ[1].large_image_text}`**__ | `{activ[1].small_image_text}`')    
            elif str(user.activities[1].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[1].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[1].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[2].type) == "ActivityType.playing":
                if user.activities[2].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\n ㄴ{activ[2].details}\n ㄴ{activ[2].state}\n__**`{activ[2].large_image_text}`**__ | `{activ[2].small_image_text}`')    
            elif str(user.activities[2].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[2].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[2].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[2].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
        elif len(user.activities) == 2:
            # Activity가 두개일때
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            elif str(user.activities[1].type) == "ActivityType.playing":
                if user.activities[1].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\n ㄴ{activ[1].details}\n ㄴ{activ[1].state}\n__**`{activ[1].large_image_text}`**__ | `{activ[1].small_image_text}`')    
            elif str(user.activities[1].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[1].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[1].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[1].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)
            #Activity가 하나일때
        elif len(user.activities) == 1:
            if str(user.activities[0].type) == "ActivityType.playing":
                if user.activities[0].details is None:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중', inline=False)       
                else:
                    embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\n ㄴ{activ[0].details}\n ㄴ{activ[0].state}\n__**`{activ[0].large_image_text}`**__ | `{activ[0].small_image_text}`')    
            elif str(user.activities[0].type) == "ActivityType.Spotify":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 듣는 중\nㄴ**{Spotify.title}**\nㄴ Artist: {Spotify.artist}\nㄴ Album: {Spotify.album}', inline=False)
            elif str(user.activities[0].type) == "ActivityType.Streaming":
                embed.add_field(name='현재 활동', value=f'**{activ[0].name}** 하는 중\nㄴ Platform: **{discord.Streaming.platform}**\nㄴ {discord.Streaming.name}\nㄴ [Link]({discord.Streaming.url})')
            elif str(user.activities[0].type) == "ActivityType.custom":
                embed.add_field(name='현재 활동', value=f'Custom Status\n**{user.activity}**', inline=False)

        if len(user.roles) > 1:
            info.add_field(name='Highest Role', value=user.top_role.mention, inline=False)

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            print(role_string)
            info.add_field(name='Roles', value=role_string, inline=False)
        info.set_footer(text=f'#{members.index(user) + 1} • USER ID : ' + str(user.id))
        return await ctx.send(embed=embed)

@bot.command(aliases=['초대'])
async def invite(ctx):
    embed = discord.Embed(title='Tae Invite Link', description='[Invite Link](https://discord.com/api/oauth2/authorize?client_id=837332366371979336&permissions=2448944215&scope=bot%20applications.commands)', color=0xFAFD40)
    await ctx.send(embed = embed)

@청소.error
async def error(ctx, error):
    # manage_message 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 비었을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg2 = await ctx.send(f'{ctx.message.author.mention}, 청소 할 메세지의 수를 입력해주세요! (ex:1,2,3...)')
        await asyncio.sleep(5)
        await msg2.delete()
    # 숫자가 아닌 다른것들이 입력되었을 경우 출력 될 메세지 
    if isinstance(error, BadArgument):
        msg3 = await ctx.send(f'{ctx.message.author.mention}, 숫자를 입력해주세요! (ex:1,2,3...)')
        await asyncio.sleep(5)
        await msg3.delete()

@공지.error
async def error(ctx, error):
    # administrator 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 비었을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        error_msg = await ctx.send(f'{ctx.message.author.mention}, 공지 할 메세지를 제대로 입력해주세요!')
        await asyncio.sleep(5)
        await error_msg.delete()
    # 설정된 공지 채널이 없을 경우 출력 될 메세지
    if isinstance(error, CommandInvokeError):
        error_msg2 = await ctx.send(f'{ctx.message.author.mention}, 공지를 보낼 채널이 설정 되어있지 않습니다. 공지채널을 설정 한 이후 다시 시도해주세요.')
        await asyncio.sleep(5)
        await error_msg2.delete()

@전체공지.error
async def error(ctx, error):
    # 명령어 실행자가 봇의 오너가 아닐 경우
    if isinstance(error, NotOwner):
        await ctx.send('{}, 개발자만 사용할 수 있는 명령어입니다!'.format(ctx.message.author.mention))
        return

@DM.error
async def error(ctx,error):
    # 인수가 비었을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg = await ctx.send(f'{ctx.message.author.mention}, 보낼 메세지를 제대로 입력해주세요!')
        await asyncio.sleep(5)
        await msg.delete()

@입장.error
async def error(ctx, error):
    # administrator 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 비었을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg2 = await ctx.send(f'{ctx.message.author.mention}, 입장로그를 전송할 채널을 제대로 선택해주세요! (ex. 입장 #<채널이름>)')
        await asyncio.sleep(5)
        await msg2.delete()
    # 채널이 발견되지 않았을 경우 출력 될 메세지
    if isinstance(error, ChannelNotFound):
        msg3 = await ctx.send(f'{ctx.message.author.mention}, 퇴장로그를 전송할 채널을 제대로 선택해주세요! (ex. 퇴장 #<채널이름>)')
        await asyncio.sleep(5)
        await msg3.delete()

@퇴장.error
async def error(ctx, error):
    # administrator 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 비었을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg2 = await ctx.send(f'{ctx.message.author.mention}, 퇴장로그를 전송할 채널을 제대로 선택해주세요! (ex. 퇴장 #<채널이름>)')
        await asyncio.sleep(5)
        await msg2.delete()
    # 채널이 발견되지 않았을 경우 출력 될 메세지
    if isinstance(error, ChannelNotFound):
        msg3 = await ctx.send(f'{ctx.message.author.mention}, 퇴장로그를 전송할 채널을 제대로 선택해주세요! (ex. 퇴장 #<채널이름>)')
        await asyncio.sleep(5)
        await msg3.delete()

@슬로우.error
async def error(ctx, error):
    # manage_channels 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 숫자가 아닐 경우 출력 될 메세지
    if isinstance(error, BadArgument):
        msg2 = await ctx.send(f'{ctx.author.mention}, 초는`0(끄기) ~ 21600(6시간)`으로 입력해주세요.')
        await asyncio.sleep(5)
        await msg2.delete()
    # 인수가 없을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg3 = await ctx.send(f'{ctx.author.mention}, 초는`0(끄기) ~ 21600(6시간)`으로 입력해주세요.')
        await asyncio.sleep(5)
        await msg3.delete()

@nuke.error
async def error(ctx, error):
    # administrator 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()

@guildlist.error
async def error(ctx, error):
    # 명령어 작동 실패
    if isinstance(error, CommandInvokeError):
        await ctx.message.add_reaction(emoji=no_gif)

access_token = os.environ["BOT_TOKEN"]

bot.run(access_token)
