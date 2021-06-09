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
from discord.ext.commands.core import has_permissions
from discord.flags import alias_flag_value
from discord.user import User
from discord.utils import get
from discord.ext.commands.errors import BadArgument, ChannelNotFound, CommandError, CommandInvokeError, CommandNotFound, MissingPermissions, MissingRequiredArgument, NotOwner
from discord.mentions import AllowedMentions

def get_prefix(bot, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix = get_prefix, intents = intents)
bot.remove_command('help')
owner = 298333126143377419
now_utc = datetime.datetime.now(timezone('UTC'))
now_kst = now_utc.astimezone(timezone('Asia/Seoul')).strftime("%#I:%M %p")
time = now_kst

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
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Support to Summer#5555"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="{}개의 서버와 함께해요!".format(len(bot.guilds))))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="{}명의 유저와 함께해요!".format(len(bot.users))))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="&play"))
        await asyncio.sleep(30)

@bot.event
async def on_command_error(ctx: commands.Context, exception: Exception):
    embed = discord.Embed(title='<a:nope_gif:851841522726338580> 오류가 발생했습니다.', description=' ', color=0xFF0000)
    embed.add_field(name='**Error Message**', value=f'```Error occured - {type(exception).__name__} : {exception}```', inline=False)
    embed.set_footer(text=f'{ctx.message.author.name} • Today at {time}', icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed = embed)
    print(f'Error occured - {type(exception).__name__} : {exception}')

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
    firstchannel = discord.utils.get(guild.text_channels, position=0)
    embed = discord.Embed(title='당신의 서버에 저를 추가해주셔서 감사합니다!', description=' ')
    embed.add_field(name='Tae봇의 접두사는 `&`입니다!', value='관리자 권한이 있을 시 changeprefix 명령어를 통해 접두사를 바꿀 수 있습니다.')
    embed.add_field(name='\n봇의 사용법을 보시려면 `&help` 명령어를 사용해보세요!')
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
        embed.set_footer(text=f'{ctx.message.author.name} • Today at {time}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='Commands', value='`&help commands`', inline=True)
        embed.add_field(name='Music', value='`&help music`', inline=True)
        embed.add_field(name='Miscellaneous', value='`&help misc`', inline=True)
        embed.add_field(name='Moderator', value='`&help moderator`', inline=True)
        await ctx.send(embed = embed)
    if args == 'commands':
        # help commands를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Commands', description=' ', color=0xFAFD40)
        embed.set_footer(text=f'{ctx.message.author.name} • Today at {time}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`invite`', value='봇 초대링크를 받을 수 있습니다.', inline=True)
        await ctx.send(embed = embed)
    if args == 'music':
        # help music를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Music', description=' ', color=0xFAFD40)
        embed.set_footer(text=f'{ctx.message.author.name} • Today at {time}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`&join`', value='음성채널에 접속합니다', inline=True)
        embed.add_field(name='`&p <이름 혹은 url>`', value='노래를 재생합니다', inline=True)
        embed.add_field(name='`&q`', value='플레이리스트를 보여줍니다', inline=True)
        embed.add_field(name='`&skip`', value='재생 중인 노래를 건너 뛸 수 있습니다', inline=True)
        embed.add_field(name='`&pause`', value='재생 중인 노래를 일시정지 시킵니다', inline=True)
        embed.add_field(name='`&resume`', value='일시정지시켰던 노래를 다시 재생할 수 있습니다', inline=True)
        embed.add_field(name='`&np`', value='재생중인 음악의 정보를 알려줍니다', inline=True)
        await ctx.send(embed = embed)
    if args == 'misc':
        # help misc를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Misc', description=' ', color=0xFAFD40)
        embed.set_footer(text=f'{ctx.message.author.name} • Today at {time}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`&avatar`', value='프로필 이미지를 얻을 수 있습니다.', inline=True)
        embed.add_field(name='`&userinfo or 내정보`', value='디스코드 계정에 대한 정보를 얻을 수 있습니다. (ex. 계정 생성일, 서버 접속일, 현재 활동, 소유중인 역할 등)', inline=True)
        await ctx.send(embed = embed)
    if args == 'moderator':
        # help moderator를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Moderator', description=' ', color=0xFAFD40)
        embed.set_footer(text=f'{ctx.message.author.name} • Today at {time}', icon_url=ctx.message.author.avatar_url)
        embed.add_field(name='`&공지`', value='&공지 <할 말> 을 통해 서버에 공지를 보낼 수 있습니다. <공지채널 명령어를 통한 채널 설정 필요> \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&공지채널`', value='&공지채널 #채널 을 통해 공지를 보낼 채널을 설정할 수 있습니다. \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&청소`', value='&청소 <청소 할 메세지의 갯수> 를 통해 메세지를 청소할 수 있습니다. \n\n필요한 권한 : Manage Messages', inline=True)
        embed.add_field(name='`&입장`', value='&입장 #채널 을 통해 입장로그를 보낼 채널을 설정 할 수 있습니다. \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&퇴장`', value='&퇴장 #채널 을 통해 퇴장로그를 보낼 채널을 설정 할 수 있습니다. \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&changeprefix`', value='&changeprefix <봇을 사용할 칭호> 를 통해 서버에서 Tae봇을 사용할 때 쓸 칭호를 설정할 수 있습니다. 기본 : & \n\n필요한 권한 : Administrator', inline=True)
        embed.add_field(name='`&slowmode`', value='&slowmode <초> 를 통해 해당 채널에 슬로우모드를 걸 수 있습니다. \n\n필요한 권한 : Manage Channels', inline=True)
        await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def gcreate(ctx, time=None, *, prize=None):
    if time == None:
        return await ctx.send('Please include a time!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    embed = discord.Embed(title='New Giveaway!', description=f'{ctx.author.mention} is giving away **{prize}**!')
    time_convert = {'s':1, 'm':60, 'h':3600, 'd':86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f'Host: {ctx.author} | Ends in {time}')
    await ctx.channel.purge(limit=1)
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction('🎉')
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[1].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    embed2 = discord.Embed(title='Giveaway', description=' ', color=0xFAFD40)
    embed.add_field(name=f'🎁 **{prize}**', value='Host:')
    embed.add_field(name=f':🏅 **Winner**:', value=f'{winner.mention}')

    await ctx.send(embed = embed2)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, time):
    time_convert = {'0':0,'s':1, 'm':60, 'h':3600, 'd':86400}
    time = int(time) * time_convert[time[-1]]
    if time == 0:
        await ctx.send('Slowmode가 꺼졌습니다.')
        await ctx.channel.edit(slowmode_delay = 0)
    elif time > 21600:
        await ctx.send('Slowmode는 6시간을 초과할 수 없습니다!')
        return
    else:
        await ctx.channel.edit(slowmode_delay = time)
        await ctx.send(f'Slowmode가 {time}초로 설정되었습니다.')

@bot.command()
@commands.has_permissions(administrator=True)
# 공지사항 embed 전송 명령어
async def 공지(ctx, *, arg):
    # 공지사항 embed를 전송할 채널 가져오기


    with open('announce.json', 'r', encoding='utf-8') as f:
        announce_dict = json.load(f)

        announce = announce_dict[str(ctx.guild.id)] 

        now = datetime.datetime.now()
        time = f'{str(now.year)}/{str(now.month)}/{str(now.day)}'
        dm_channel = await ctx.message.author.create_dm()
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title='공지', description=' ', color=0xFAFD40)
        embed.add_field(name=(arg), value='** **', inline=False)
        embed.set_footer(text='Sender: 'f'{ctx.message.author} | {time}', icon_url=ctx.author.avatar_url)
        await bot.get_channel(int(announce)).send(embed = embed)
        msg = await ctx.send(f'{ctx.message.author.mention}님에게 이번 공지에 대한 로그가 전송되었습니다.')
        embed2 = discord.Embed(title='Result', description=' ', color=0XFAFD40)
        embed2.add_field(name=f'`{arg}`' + ' 라는 메세지를 설정한 공지채널에 보냈습니다.', value='** **', inline=False)
        embed2.set_footer(text=f'{time} at {ctx.guild}')
        await dm_channel.send(embed = embed2)
        await asyncio.sleep(5)
        await msg.delete()

@bot.command()
@commands.is_owner()
# 봇 전체공지 명령어
async def 전체공지(ctx, args=None):
    for i in bot.guilds:
        channel = discord.utils.get(i.text_channels, topic='봇-공지')
        topchannel = discord.utils.get(i.text_channels, position=0)
        embed = discord.Embed(title='TaeBot 공지', description=' ', color=0xFAFD40)
        embed.add_field(name=f'{args}', value=':link:[TaeBot 초대하기](https://discord.com/api/oauth2/authorize?client_id=837332366371979336&permissions=45444182&scope=bot)')
        embed.set_footer(text=f'Sender: {ctx.message.author} - Verified\n다른 채널에 공지를 전송받고 싶다면 채널 주제에 \'봇-공지\'라고 적어주세요.', icon_url=ctx.message.author.avatar_url)
        if channel is None:
            await topchannel.send(embed = embed)
        else:
            await channel.send(embed = embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def 킥(ctx, member: discord.Member=None, *, reasons=None):
    try:
        user = await bot.get_user(member.id).create_dm()
        embed = discord.Embed(title='KICKED', description=f'Server: {ctx.guild.name}')
        embed.add_field(name='사유', value=f'{reasons}')
        embed.set_footer(text=f'처리자: {ctx.message.author} • at {time}', icon_url=ctx.author.avatar_url)
        await user.send(embed = embed)
        await member.kick(reason=reasons)
        embed2 = discord.Embed(title='Result', description='처리 기록')
        embed2.add_field(name=f'{member}가 추방되었습니다.', value=f'사유 : {reasons}')
        embed2.set_footer(text=f'처리자: {ctx.message.author} • at {time}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed = embed2)
    except CommandError:
        return      

@bot.command()
@commands.has_permissions(manage_messages=True)
async def 청소(ctx,amount:int):
    await ctx.channel.purge(limit=int(amount+1))
    msg = await ctx.send(f'{amount}개의 메세지를 청소했습니다!')
    await asyncio.sleep(5)
    await msg.delete()

@bot.command()
async def 옌(ctx, *, arg):
    user = await bot.get_user(382891982382563328).create_dm()
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
        embed2.add_field(name=(arg), value=f'{time}에 발송한 메세지입니다.')
        await dm.send(embed = embed2)
        # 전송될 메세지 Embed
        dm_for_user = await user.send(f'`{ctx.author}` 님에게서 메세지가 도착했습니다. 5초 뒤에 표시됩니다.')
        await asyncio.sleep(1)
        await dm_for_user.edit(content=f'`{ctx.author}` 님에게서 메세지가 도착했습니다. 4초 뒤에 표시됩니다.')
        await asyncio.sleep(1)
        await dm_for_user.edit(content=f'`{ctx.author}` 님에게서 메세지가 도착했습니다. 3초 뒤에 표시됩니다.')
        await asyncio.sleep(1)
        await dm_for_user.edit(content=f'`{ctx.author}` 님에게서 메세지가 도착했습니다. 2초 뒤에 표시됩니다.')
        await asyncio.sleep(1)
        await dm_for_user.edit(content=f'`{ctx.author}` 님에게서 메세지가 도착했습니다. 1초 뒤에 표시됩니다.')
        await asyncio.sleep(1)
        await dm_for_user.edit(content=f'`{ctx.author}` 님에게서 메세지가 도착했습니다. 5초가 지났습니다 메세지를 표시합니다.')
        await asyncio.sleep(0.5)
        embed = discord.Embed(title='Message', description=' ', color=0xFAFD40)
        embed.add_field(name=(arg), value='** **', inline=False)
        await user.send(embed = embed)

@bot.command(name='avatar', aliases=['av'])
async def _avatar(ctx, member : discord.Member=None):
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
        date_format = '%Y/%m/%d %I:%M:%S'
        status = user.status
        if status == discord.Status.online:
            status = 'Online | 온라인'
        elif status == discord.Status.idle:
            status = 'Idle | 자리 비움'
        elif status == discord.Status.dnd:
            status = 'Do Not Disturb | 다른 용무중'
        elif status == discord.Status.offline:
            status = 'Offline | 오프라인'
        
        activ = user.activities
        if activ == ():
            return
        elif len(activ) == 0:
            activ = f'**{user.activity}** 하는 중'
        elif len(activ) == discord.CustomActivity:
            activ == f'**{user.activity}**\n\n**{user.activities[1].name}** 하는 중\nL {user.activities[1].details}\nL {user.activities[1].state}\n**`{user.activities[1].large_image_text}`** | `{user.activities[1].small_image_text}`'
        elif len(activ) == 2:
            activ = f'**{discord.Spotify.title}** 듣는 중\nㄴArtist: {discord.Spotify.artist}\nㄴ Album: {discord.Spotify.album}\nㄴ Duration: {discord.Spotify.duration}'
        print(activ)

        embed = discord.Embed(color=0xdfa3ff, title='USER INFO')
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='현재 상태', value=status)
        embed.add_field(name='계정 생성일', value=user.created_at.strftime(date_format), inline=False)
        embed.add_field(name='서버 접속일', value=user.joined_at.strftime(date_format), inline=False)
        embed.add_field(name='현재 활동', value='{}'.format(activ), inline=False)
        embed.add_field(name='Discord Badge', value=f'Empty Now')

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name='소유중인 역할', value=role_string, inline=False)
        embed.set_footer(text=f'#{members.index(user) + 1} • USER ID : ' + str(user.id))
        return await ctx.send(embed=embed)
        
    else:
        date_format = '%Y/%m/%d %I:%M:%S'
        status = user.status
        if status == discord.Status.online:
            status = 'Online | 온라인'
        elif status == discord.Status.idle:
            status = 'Idle | 자리 비움'
        elif status == discord.Status.dnd:
            status = 'Do Not Disturb | 다른 용무중'
        elif status == discord.Status.offline:
            status = 'Offline | 오프라인'

        activ = user.activities
        if activ == None:
            pass
        elif activ == ActivityType.playing:
            activ = f'**{user.activity}** 하는 중'
        elif activ == discord.Activity:
            activ == f'**{user.activity}**\n\n**{user.activities[1].name}** 하는 중\nL {user.activities[1].details}\nL {user.activities[1].state}\n**`{user.activities[1].large_image_text}`** | `{user.activities[1].small_image_text}`'
        elif activ == discord.CustomActivity:
            activ = f'**{user.activity}**'
        elif activ == activity.Spotify:
            activ = f'{discord.Spotify.artist} - **{discord.Spotify.title}**\nL Album: {discord.Spotify.album}\nL Duration: {discord.Spotify.duration}'

        embed = discord.Embed(color=0xdfa3ff, title='USER INFO')
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='현재 상태', value=status)
        embed.add_field(name='계정 생성일', value=user.created_at.strftime(date_format), inline=False)
        embed.add_field(name='서버 접속일', value=user.joined_at.strftime(date_format), inline=False)
        embed.add_field(name='현재 활동', value=len(activ), inline=False)
        embed.add_field(name='Discord Badge', value=f'Empty Now')

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name='소유중인 역할', value=role_string, inline=False)
        embed.set_footer(text=f'#{members.index(user) + 1} • USER ID : ' + str(user.id))
        return await ctx.send(embed = embed)

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title='TaeBot Invite Link', description='[Invite Link](https://discord.com/api/oauth2/authorize?client_id=837332366371979336&permissions=45444182&scope=bot)', color=0xFAFD40)
    await ctx.send(embed = embed)

@청소.error
async def purge_error(ctx, error):
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
async def send_error(ctx, error):
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
async def send_error(ctx, error):
    # 명령어 실행자가 봇의 오너가 아닐 경우
    if isinstance(error, NotOwner):
        await ctx.send('{}, 개발자만 사용할 수 있는 명령어입니다!'.format(ctx.message.author.mention))
        return

@옌.error
async def send_error(ctx,error):
    # 인수가 비었을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg = await ctx.send(f'{ctx.message.author.mention}, 보낼 메세지를 제대로 입력해주세요!')
        await asyncio.sleep(5)
        await msg.delete()

@입장.error
async def send_error(ctx, error):
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
async def send_error(ctx, error):
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

@킥.error
async def send_error(ctx, error):
    # kick_members 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 유저를 멘션하지 않았을 경우 출력 될 메세지
    if isinstance(error, BadArgument):
        msg2 = await ctx.send(f'{ctx.message.author.mention}, 명령어의 사용이 잘못되었습니다. 추방시킬 유저를 제대로 멘션해주세요! (ex. 킥 @<user>)')
        await asyncio.sleep(5)
        await msg2.delete()
    
    # 유저를 멘션하지 않았을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg3 = await ctx.send(f'{ctx.message.author.mention}, 명령어의 사용이 잘못되었습니다. 추방시킬 유저를 제대로 멘션해주세요! (ex. 킥 @<user>)')
        await asyncio.sleep(5)
        await msg3.delete()

@slowmode.error
async def send_error(ctx, error):
    # manage_channels 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 숫자가 아닐 경우 출력 될 메세지
    if isinstance(error, BadArgument):
        msg2 = await ctx.send(f'{ctx.message.author.mention}, 시간을 정확히 입력해주세요! (ex. 10s, 10m, 1h)')
        await asyncio.sleep(5)
        await msg2.delete()
    # 인수가 없을 경우 출력 될 메세지
    if isinstance(error, MissingRequiredArgument):
        msg3 = await ctx.send(f'{ctx.message.author.mention}, 시간을 정확히 입력해주세요! (ex. 10s, 10m, 1h)')
        await asyncio.sleep(5)
        await msg3.delete()
        

# Music Commands
# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=0xFAFD40)
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))
        
        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    self.exists = False
                    return

                self.current.source.volume = self._volume
                self.voice.play(self.current.source, after=self.play_next_song)
                await self.current.source.channel.send(embed=self.current.create_embed())

            elif self.loop == True:
                self.now = discord.FFmpegPCMAudio(self.current.source.stream_url, **YTDLSource.FFMPEG_OPTIONS)
                self.voice.play(self.now, after=self.play_next_song)

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', aliases=['j'], invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect', 'l'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]
        await ctx.message.add_reaction('👋')

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.current.source.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""
        
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send('I\'m currently not playing anything!', delete_after=20)
            return
        elif ctx.voice_client.is_paused():
            return

        ctx.voice_client.pause()
        await ctx.message.add_reaction('⏸')

    @commands.command(name='resume')
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await ctx.send('I am not currently playing anything!', delete_after=20)
            return
        elif not ctx.voice_client.is_paused():
            return

        ctx.voice_client.resume()
        await ctx.message.add_reaction('▶')

    @commands.command(name='stop')
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('🛑')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            await ctx.send('재생중인 노래가 없습니다!')
            return 

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            ctx.voice_state.skip()


        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send(f'Skip vote added, currently at **{total_votes}/3**', delete_after=60)
                await asyncio.sleep(60)
        else:
            await ctx.send('You have already voted to skip this song.', delete_after=15)


    @commands.command(name='queue', aliases=['q'])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('재생목록이 비었습니다.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('재생목록이 비어있어요.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            await ctx.send('재생목록이 비어있어요.', delete_after=15)
            return 

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            await ctx.send('재생중인 노래가 없습니다!')
            return 

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play', aliases=['p'])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
        except YTDLError as e:
            await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
        else:
            if not ctx.voice_state.voice:
                await ctx.invoke(self._join)

            song = Song(source)
            await ctx.voice_state.songs.put(song)
            await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

bot.add_cog(Music(bot))

access_token = os.environ["BOT_TOKEN"]

bot.run(access_token)
