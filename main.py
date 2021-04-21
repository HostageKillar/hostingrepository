import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import os

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
    game = discord.Game("Sleeping")
    await app.change_presence(status=discord.Status.online,activity=game)

def setEmbed(Title, Footer, Description, Color, Inline, **kwargs):
    embed = discord.Embed(title = Title, description = Description, color = Color)
    for x in kwargs.keys():
        temp = x.split("_")
        embed.add_field(name=" ".join(temp), value=kwargs[x], inline=Inline)
    embed.set_footer(text=Footer)
    return embed

def returnAddData(filename,directory,num):
    try:
        f = open(directory+filename, "r")
        data = f.read()
        f.close()
        f = open(directory+filename,  "w")
        f.write(str(int(data)+int(num)))
        f.close()
        return int(data)+int(num)
    except FileNotFoundError:
        print("Error : File not found")


def find(filename, directory):
    if os.path.exists(directory+filename):
        return True
    else:
        return False

@app.command(name="DM", pass_context=True)
async def send_dm(ctx, user_name: discord.Member, content):
    channel = await user_name.create_dm()

    await channel.send(content = Content)

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




@app.command(name="추방", pass_context=True)
@commands.has_permissions(administrator=True)
async def _kick(ctx, *, user_name: discord.Member, reason=None):
    print("추방 명령어 작동")
    await user_name.kick(reason=reason)
    await ctx.send(str(user_name) + "님을 추방했습니다.")
@_kick.error
async def _kick_error(ctx, error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("{}님, 당신은 이 명령을 쓸 권한이 없습니다.".format(ctx.message.author))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("유저를 넣어주세요.")
    if isinstance(error,commands.BadArgument):
        await ctx.send("유저의 이름이 유효하지 않습니다.")

@app.command(name="밴", pass_context=True)
@commands.has_any_role("Commander")
async def _ban(ctx, *, user_name: discord.Member):
    print("밴 명령어 작동")
    await user_name.ban()
    await ctx.send(str(user_name) + "님을 영원무궁하도록 추방했습니다.")
@_ban.error
async def _ban_error(ctx,error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("{}님, 당신은 이 명령을 쓸 권한이 없습니다.".format(ctx.message.author))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("유저를 넣어주세요.")
    if isinstance(error,commands.BadArgument):
        await ctx.send("유저의 이름이 유효하지 않습니다.")


@app.command(name="경고", pass_context=True)
@commands.has_permissions(administrator=True)
async def _warn(ctx, counts, user_name: discord.Member=None, reason="없음"):
    print("경고 명령어 작동")
    if user_name == None or ctx.message.author:
        foundfile = find(str(user_name)+".txt", "warnings/")
        if foundfile:
            warnings = returnAddData(str(user_name)+".txt", "warnings/", counts)
            if warnings >= 2:
                await user_name.ban()
                await ctx.send(str(user_name)+"님은 선을 넘어서(경고 2회 받음) 밴 되었습니다.")
            else:
                await ctx.send(str(user_name)+"에게 경고를"+str(counts)+"만큼 부여했습니다.")
        else:
            f = open("warnings/"+str(user_name)+".txt", "w+")
            f.write(str(int(counts)))
            f.close()
            await ctx.send(str(user_name)+"에게 경고를"+str(counts)+"만큼 부여했습니다.")
        
async def _warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("{}님, 당신은 이 명령을 쓸 권한이 없습니다.".format(ctx.message.author))


app.remove_command("help")
access_token = os.environ["BOT_TOKEN"]
app.run(access_token)
