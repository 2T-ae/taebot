import discord
from discord import message
from discord import colour
from discord import channel
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.flags import alias_flag_value
from discord.utils import get
import asyncio
import random
import os
import youtube_dl
from discord.ext.commands.errors import MissingPermissions

from discord.mentions import AllowedMentions

intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix='&', intents = intents, lavalinkpass = "yourpass", lavalinkport = 6969)
bot.remove_command('help')
idchannel = 844796497157423114
#서예은 방 입퇴장 채널
tae = 298333126143377419

@bot.event
async def on_ready():
    # 프로그램 실행 시 초기 구성  
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="&도움말 을 통해 명령어를 사용해보세요!"))
    await asyncio.sleep(30)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Made by 2Tae#0001"))
    await asyncio.sleep(30)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="&play"))
    await asyncio.sleep(30)

@bot.command()  
async def 도움말(ctx):
    embed = discord.Embed(title='도움말', description=' ', color=0xFAFD40)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
    embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
    embed.add_field(name='Commands', value='`&help command`', inline=True)
    embed.add_field(name='Music', value='`&help music`', inline=True)
    embed.add_field(name='Miscellaneous', value='`&help misc`', inline=True)
    await ctx.send(embed = embed)

@bot.command()
async def help(ctx, arg):
    if arg == 'command':
        # help commands를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Commands', description='Tae Bot Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&도움말', value='`도움말을 확인할 수 있습니다.`', inline=True)
        embed.add_field(name='&DM', value='`이테를 디엠으로 부를 수 있습니다.`', inline=True)
        embed.add_field(name='&모여', value='`&모여 <할 것> 을 통해 서버에 있는 유저들을 호출 할 수 있습니다.`', inline=True)
        embed.add_field(name='&노래추천', value='`이테가 선정한 노래를 추천 받을 수 있다 (매일 바뀐다) [ 아직 미완 ]`', inline=True)
        await ctx.send(embed = embed)
    if arg == 'music':
        # help music를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Music', description='Tae Bot Music Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&j', value='`봇을 통화방에 부를 수 있습니다.`', inline=True)
        embed.add_field(name='&p <노래 이름 혹은 url>', value='`봇을 통해 노래를 재생할 수 있습니다.`', inline=True)
        await ctx.send(embed = embed)
    if arg == 'misc':
        # help misc를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Misc', description='Tae Bot Misc Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&초대', value='`Tae봇을 초대 할 수 있는 링크를 받을 수 있다`', inline=True)
        embed.add_field(name='&청소', value='`&청소 <청소 할 메세지의 갯수> 를 통해 메세지를 청소할 수 있다.`', inline=True)
        embed.add_field(name='&avatar', value='`&avatar @유저 혹은 &av @유저 를 통해 아바타를 얻을 수 있습니다.`', inline=True)
        await ctx.send(embed = embed)

@bot.command()
async def DM(ctx):
    user = await bot.get_user(tae)
    if user.status == discord.Status.offline:
        await ctx.send('2Tae님이 오프라인 상태이기 때문에 DM을 보낼 수 없습니다.')
    else:
        await bot.get_user(tae).send(f'{user.mention}님, {ctx.message.author}님이 DM 명령어를 사용했습니다!')
        await ctx.send('2Tae님이 온라인 상태여서 DM을 전송했습니다.')

@bot.command()
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
@commands.has_permissions(mention_everyone=True)
async def 모여(ctx, *, args=None):
    if args !=None:
        await ctx.channel.send('@everyone ' + args + ' 할 사람 모여라!')
        await ctx.channel.send(f'`{ctx.message.author.name}`님이 모여 명령어를 사용했습니다!')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def 청소(ctx,amount:int):
        await ctx.channel.purge(limit=int(amount+1))
        msg = await ctx.send(f'{amount}개의 메세지를 청소했습니다!')
        await asyncio.sleep(5)
        await msg.delete()

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
    await ctx.send(f'{ctx.message.author.mention} Tae봇의 초대링크입니다. https://discord.com/api/oauth2/authorize?client_id=837332366371979336&permissions=8&scope=bot')


@bot.command(pass_context=True, aliases=['j'])
# 통화방 들어오게 하기 
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f'**Joined `{channel}`**')

@bot.command(pass_context=True, aliases=['l', 'lea'])
# 통화방 나가게 하기
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send('**Successfully disconnected**')
    else:
        embed = discord.Embed(title='저는 통화방에 들어가있지 않아요.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)

@bot.command(pass_context=True, aliases=['p'])
# 노래 재생
async def play(ctx, url: str):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    song_there = os.path.isfile("song.mp3")
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send('ERROR: Music playing')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(''))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.06

    nname = name.rsplit('-', 1)
    await ctx.send(f"Playing: {nname[0]}")

@bot.command(pass_context=True, aliases=['pa','pau'])
# 노래 중단
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        embed = discord.Embed(title='재생중이던 노래가 멈췄습니다.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title='노래가 재생중이지 않습니다.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)

@bot.command(pass_context=True, aliases=['r','res'])
# 노래 다시 재생
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        embed = discord.Embed(title='노래를 다시 재생합니다.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title='노래가 중단되지 않았습니다.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)

@bot.command(pass_context=True, aliases=['s', 'ski'])
async def skip(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        embed = discord.Embed(title='재생중인 노래를 스킵합니다.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title='스킵할 노래가 없습니다.', description=' ', color=0xFAFD40)
        await ctx.send(embed = embed)


@bot.event
async def on_member_join(member):
    # 서버에 멤버가 들어왔을 때 실행 될 이벤트
    await bot.get_channel(idchannel).send(f'{member.mention}님이 서버에 들어오셨어요.') 

@bot.event
async def on_member_remove(member):
        # 서버에서 멤버가 나갔을 때 실행 될 이벤트
    await bot.get_channel(idchannel).send(f'{member.mention}님이 서버에서 나가셨어요.')

@청소.error
async def purge_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')
    if isinstance(error, ValueError):
        await ctx.send('청소 할 메세지의 수를 입력해주세요! (ex:1,2,3...)')

@모여.error
async def send_error(ctx, error):
    if isinstance(error,MissingPermissions):
        await ctx.send(f'{ctx.message.author.mention}님은 이 명령어를 사용할 권한이 없습니다!')

access_token = os.environ["BOT_TOKEN"]

bot.run(access_token)
