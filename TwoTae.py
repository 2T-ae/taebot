import discord
import asyncio
import random
import os
import datetime
import shutil
import json
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
from discord.ext.commands.errors import BadArgument, ChannelNotFound, CommandInvokeError, CommandNotFound, MissingPermissions, MissingRequiredArgument
from discord.mentions import AllowedMentions

def get_prefix(bot, message):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix = get_prefix, intents = intents)
bot.remove_command('help')

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
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="&도움말 을 통해 명령어를 사용해보세요!"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Made by 2Tae#0001"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="&play"))
        await asyncio.sleep(30)

@bot.event
async def on_command_error(ctx: commands.Context, exception: Exception):
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

@bot.event
async def on_member_join(member):
    # 서버에 사람이 들어왔을 때 출력될 Welcome 메세지


    with open("welcome.json", "r", encoding='utf-8') as f:
        welcome_dict = json.load(f)

    welcome = welcome_dict[str(member.guild.id)]
    await bot.get_channel(int(welcome)).send(f'{member.mention}님, {member.guild.name} 서버에 오신것을 환영합니다!')

@bot.event
async def on_member_leave(member):
    # 서버에서 사람이 나갔을 때 출력될 Leave 메세지


    with open("leave.json", "r", encoding='utf-8') as f:
        leave_dict = json.load(f)

    leave = leave_dict[str(member.guild.id)]
    await bot.get_channel(int(leave)).send.send(f'{member.name}님이 서버에서 나가셨습니다. 다음에 또 만나길 빌어요.')

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
async def 도움말(ctx):
    embed = discord.Embed(title='도움말', description=' ', color=0xFAFD40)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
    embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
    embed.add_field(name='Commands', value='`&help command`', inline=True)
    embed.add_field(name='Music', value='`&help music`', inline=True)
    embed.add_field(name='Miscellaneous', value='`&help misc`', inline=True)
    embed.add_field(name='Moderator', value='`&help moderator`', inline=True)
    await ctx.send(embed = embed)

@bot.command()
async def help(ctx, arg):
    if arg == 'command':
        # help commands를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Commands', description='Tae Bot Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&도움말', value='`도움말을 확인할 수 있습니다.`', inline=True)
        embed.add_field(name='&노래추천', value='`이테가 선정한 노래를 추천 받을 수 있습니다 [ 아직 미완 ]`', inline=True)
        await ctx.send(embed = embed)
    if arg == 'music':
        # help music를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Music', description='Tae Bot Music Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&join', value='`봇을 통화방에 부를 수 있습니다.`', inline=True)
        embed.add_field(name='&play <이름 혹은 url>', value='`봇을 통해 노래를 재생할 수 있습니다.`', inline=True)
        embed.add_field(name='&queue <이름 혹은 url>', value='`봇을 통해 다음에 추가될 노래를 추가할 수 있습니다.`', inline=True)
        embed.add_field(name='&skip', value='`지금 재생 중인 노래를 건너 뛸 수 있습니다. (검색 추가 구현 예정)`', inline=True)
        embed.add_field(name='&pause', value='`재생 중인 노래를 중단할 수 있습니다.`', inline=True)
        embed.add_field(name='&resume', value='`중단되있던 노래를 다시 재생할 수 있습니다.`', inline=True) 
        await ctx.send(embed = embed)
    if arg == 'misc':
        # help misc를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Misc', description='Tae Bot Misc Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&초대', value='`Tae봇을 초대 할 수 있는 링크를 받을 수 있습니다`', inline=True)
        embed.add_field(name='&avatar', value='`&avatar @유저 혹은 &av @유저 를 통해 프로필 이미지를 얻을 수 있습니다.`', inline=True)
        await ctx.send(embed = embed)
    if arg == 'moderator':
        # help moderator를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Moderator', description='Tae Bot Moderator Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&공지', value='`&공지 <할 말> 을 통해 서버에 공지를 보낼 수 있습니다. \n\n필요한 권한 : 어드민 권한`', inline=True)
        embed.add_field(name='&청소', value='`&청소 <청소 할 메세지의 갯수> 를 통해 메세지를 청소할 수 있습니다. \n\n필요한 권한 : 메세지 관리`', inline=True)
        embed.add_field(name='&입장', value='`&입장 #채널 을 통해 입장로그를 보낼 채널을 설정 할 수 있습니다. \n\n필요한 권한 : 어드민 권한`', inline=True)
        embed.add_field(name='&퇴장', value='`&퇴장 #채널 을 통해 퇴장로그를 보낼 채널을 설정 할 수 있습니다. \n\n필요한 권한 : 어드민 권한`', inline=True)
        embed.add_field(name='&changeprefix', value='`&changeprefix <봇을 사용할 칭호> 를 통해 서버에서 Tae봇을 사용할 때 쓸 칭호를 설정할 수 있습니다. \n\n필요한 권한 : 어드민 권한`', inline=True)
        embed.add_field(name='&slowmode', value='`&slowmode <초> 를 통해 해당 채널에 슬로우모드를 걸 수 있습니다. \n\n필요한 권한 : 채널 관리`', inline=True)
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
async def slowmode(ctx, time:int):
    try:
        if time == 0:
            await ctx.send('Slowmode가 꺼졌습니다.')
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
            await ctx.send('Slowmode는 6시간을 초과할 수 없습니다!')
            return
        else:
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.send(f'Slowmode가 {time}초로 설정되었습니다.')
    except:
        pass

@bot.command()
# 랜덤 노래추천
async def 노래추천(ctx):
    try:
        dm_channel = await ctx.message.author.create_dm()
        embed = discord.Embed(title='[ENG] [고등래퍼4/최종회] 김우림 - Do My Best (Feat. 제시) @ 파이널 | Mnet 210423 방송', url='https://www.youtube.com/watch?v=kc7t4s78Hok', description='', color=0xFAFD40)
        embed.set_author(name='Mnet Official', icon_url='https://yt3.ggpht.com/ytc/AAUvwngh2Ctucs27ygguTKMB21kuat1zOoyvL41UFBtDxQ=s48-c-k-c0x00ffffff-no-rj')
        embed.set_thumbnail(url='https://musicmeta-phinf.pstatic.net/album/005/691/5691474.jpg?type=r120Fll&v=20210427090509')
        embed.set_image(url='https://i.ytimg.com/vi/kc7t4s78Hok/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBRIS1jpMSzFyyNbH3mkGVycsbzjw')
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        await dm_channel.send(f'{ctx.message.author.mention}님, 오늘의 추천 노래입니다!')
        await dm_channel.send(embed = embed)
        await ctx.send(f'{ctx.message.author.mention} 성공적으로 DM을 전송했습니다!')
    except:
        await ctx.send(f'{ctx.message.author.mention} DM을 전송하는데 실패했습니다. 디스코드 설정에서 `개인정보 보호 및 보안`에 들어가서 `서버 멤버가 보내는 개인 메세지 허용하기`를 켜주신 후에 다시 시도해주세요!')
        return

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
        embed.set_footer(text='작성자: 'f'{ctx.message.author} | {time}', icon_url=ctx.author.avatar_url)
        await bot.get_channel(int(announce)).send(embed = embed)
        msg = await ctx.send(f'{ctx.message.author.mention}님에게 이번 공지에 대한 로그가 전송되었습니다.')
        embed2 = discord.Embed(title='Result', description=' ', color=0XFAFD40)
        embed2.add_field(name=f'`{arg}`' + ' 라는 메세지를 설정한 공지채널에 보냈습니다.', value='** **', inline=False)
        embed2.set_footer(text=f'{time} at {ctx.guild}')
        await dm_channel.send(embed = embed2)
        await asyncio.sleep(5)
        await msg.delete()

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
    now = datetime.datetime.now()
    time = f'{str(now.year)}년|{str(now.month)}월|{str(now.day)}일 {str(now.hour)}시{str(now.minute)}분'
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
        embed = discord.Embed(title='이 명령어의 사용법은 `&avatar or &av @member`입니다', colour=0xFAFD40, timestamp=ctx.message.created_at)
        await ctx.send(embed = embed)
        return
    else:
        embed2 = discord.Embed(title='Avatar', description='')
        embed2.set_image(url=member.avatar_url)
        embed2.set_author(name=f'{member}', icon_url=member.avatar_url)
        await ctx.send(embed = embed2)

@bot.command()
async def 초대(ctx):
    await ctx.send('이 명령어는 개발이 완료된 후 사용할 수 있습니다.')

@bot.event
async def on_member_remove(member):
    # 서버에서 멤버가 나갔을 때 실행 될 이벤트
    await bot.get_channel().send(f'{member.mention}님이 서버에서 나가셨어요.')

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

@slowmode.error
async def send_error(ctx, error):
    # manage_channels 권한이 없을 경우 출력 될 메세지
    if isinstance(error, MissingPermissions):
        msg = await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
        await asyncio.sleep(5)
        await msg.delete()
    # 인수가 숫자가 아닐 경우 출력 될 메세지
    if isinstance(error, BadArgument):
        msg2 = await ctx.send(f'{ctx.message.author.mention}, 숫자를 입력해주세요! (ex. 1,2,3...)')
        await asyncio.sleep(5)
        await msg2.delete()

access_token = os.environ["BOT_TOKEN"]

bot.run(access_token)
