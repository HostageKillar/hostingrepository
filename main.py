import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import os

intents=discord.Intents()
intents.members = True

app = commands.Bot(command_prefix='>>', intents=intents)


if os.path.exists("warnings"):
    print("Warning Dir found, passing")
else:
    os.mkdir("warnings")

@app.event
async def on_ready():
    print("Login as : ")
    print(app.user.name)
    print(app.user.id)
    print(discord.version_info)
    print(discord.__version__)
    print("==========")
    game = discord.Game("Core 1 is working")
    await app.change_presence(status=discord.Status.idle,activity=game)

def setEmbed(Title, Footer, Description, Color, Inline, **kwargs):
    embed = discord.Embed(title = Title, description = Description, color = Color)
    for x in kwargs.keys():
        temp = x.split("_")
        embed.add_field(name=" ".join(temp), value=kwargs[x], inline=Inline)
    embed.set_footer(text=Footer)
    return embed

@app.event
async def on_member_join(member):

    print(f"{member.name} has joined server.")
    RuleEmbed = setEmbed(
        Title= "아잉츄 서버 규칙",
        Footer= "made by Gamma_Dust",
        Description= "서버의 규칙입니다.",
        Color= 0xFA58F4,
        Inline= False,
        규칙_1= "프로필 사진과 닉네임은 건전하게 설정해주세요.",
        규칙_2= "친목은 삼가주세요.",
        규칙_3= "타인에게 불쾌감/피해를 주는 행동은 하지 말아 주세요.",
        규칙_4= "편의 기능은 적당히 사용해주세요.",
        규칙_5= "다른 방송인의 언급(닉네임, 유튜브 링크, 사진)은 하지 말아 주세요.",
        규칙_6= "영어 채팅방에서는 영어만 사용해 주세요."
    )

    await member.send(embed= RuleEmbed)

#app.remove_command("help")
access_token = os.environ["BOT_TOKEN"]
app.run(access_token)
