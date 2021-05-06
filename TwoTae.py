import discord
import asyncio
from discord.ext import commands, tasks
import os

intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix='&', intents = intents)
bot.remove_command('help')
idchannel = 837332811831967804

@bot.event
async def on_ready():
    # 프로그램 실행 시 초기 구성
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Do My Best by D.Ark"))  
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def 안녕(ctx):
    await ctx.send('안녕!')

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title='도움말', description=' ', color=0xFAFD40)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
    embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
    embed.add_field(name='Commands', value='`&help command`', inline=False)
    await ctx.send(embed = embed)

@bot.command()
async def help(ctx, arg):
    if arg == 'command':
        # help commands를 사용했을때 출력 될 임베드
        embed = discord.Embed(title='Commands', description='Tae Bot Commands', color=0xFAFD40)
        embed.set_footer(text='Made By 2Tae#0001', icon_url='https://cdn.discordapp.com/attachments/837952773395841024/837952822527393802/rankong.png')
        embed.add_field(name='&도움말', value='`도움말을 확인할 수 있습니다.`', inline=True)
        embed.add_field(name='&DM', value='`이테를 디엠으로 부를 수 있습니다.`', inline=True)
        await ctx.send(embed = embed)

@bot.command()
async def DM(ctx):
    user = await bot.get_user(tae)
    if user.status == discord.Status.offline:
        await ctx.send('2Tae님이 오프라인 상태이기 때문에 DM을 보낼 수 없습니다.')
    else:
        await bot.get_user(tae).send(f'{user.mention}님, {ctx.message.author}님이 DM 명령어를 사용했습니다!')
        await ctx.send('2Tae님이 온라인 상태여서 DM을 전송했습니다.')

@bot.event
async def on_member_join(member):
    # 서버에 멤버가 들어왔을 때 실행 될 이벤트
    await bot.get_channel(idchannel).send(f'{member.mention}님이 서버에 들어오셨어요.') 

@bot.event
async def on_member_remove(member):
        # 서버에서 멤버가 나갔을 때 실행 될 이벤트
    await bot.get_channel(idchannel).send(f'{member.mention}님이 서버에서 나가셨어요.')

access_token = os.environ["BOT_TOKEN"]

bot.run(access_token)
