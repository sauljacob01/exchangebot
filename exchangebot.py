import discord
from discord.ext import commands
from discord.utils import get
import json
import datetime
import sys
import time
import time
import aiofiles
import typing
from discord_slash import SlashCommand, SlashContext
#import asyncpg
from discord.ext import tasks
from discord.ext.commands import Bot, has_permissions, CheckFailure, BadArgument, MissingRequiredArgument
from discord import Member
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord_components import DiscordComponents, Button, ButtonStyle

#INFO
SERVERID = 876134892939923477
WELCOMECHANNELID = 882286388177956956
LEAVECHANNELID = 882286414815965256
UNVERIFIEDMEMBER = 882538440569266206
VERIFIEDID = 882533957382598676
BOTROLEID = 882534217764995123

#ACCOUNT
expoints = 0
trustscore = 50
transactions = 0
extradip = 1
balance = 0

#DISCORD
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="ec.", intents=discord.Intents.all(), case_insensitive=True, owner_id=875422606159912990)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command("help")

#Bot Start and Status
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("ec.help"))
    print('Logged in as {0.user}'.format(bot))

def is_not_pinned(mess):
    return not mess.pinned

# Member Join Event
@bot.event
async def on_member_join(member):
    welcomechannel = discord.utils.get(member.guild.channels, id=WELCOMECHANNELID)
    await welcomechannel.send(f"{member.mention} has joined the server.")
    print(f"{member} has joined the server.")

    if not member.bot:
        role = get(member.guild.roles, id=UNVERIFIEDMEMBER)
        await member.add_roles(role)
        print(f"{member} was given {role}")

    if member.bot:
        role = get(member.guild.roles, id=BOTROLEID)
        await member.add_roles(role)
        print(f"{member} was given {role}")

    #for channel in member.guild.channels:
        #if channel.id == MEMBERCOUNTVCID:
            #await channel.edit(name=f'Member Count: {member.guild.member_count}')

# Member Leave Event
@bot.event
async def on_member_remove(member):
    leavechannel = discord.utils.get(member.guild.channels, id=LEAVECHANNELID)
    await leavechannel.send(f"{str(member)} has left the server.")
    print(f"{str(member)} has left the server")
    #for channel in member.guild.channels:
        #if channel.id == MEMBERCOUNTVCID:
            #await channel.edit(name=f'Member Count: {member.guild.member_count}')

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="List of Commands",
        description="""
        ec.ping or /ping **|** Test your ping speed
        ec.createaccount **|** Create an account
        ec.accountinfo **|** Dm you your account info
        ec.expointsinfo **|** Shows you expoints info
        """, color=0x0075db)
    await ctx.send(embed=embed)

# Verification Command
@bot.command()
@commands.has_role(UNVERIFIEDMEMBER)
async def verify(ctx):
    member = ctx.message.author
    verifiedrole = get(member.guild.roles, id=VERIFIEDID)
    unverifiedrole = get(member.guild.roles, id=UNVERIFIEDMEMBER)

    embed = discord.Embed(title="Welcome to Exchange Center!",
                          description=f"""Hello {member.name},
                                      Thank you for joining our server and verifying.
                                      To get started you can read <#880492417030180955>""", color=0x0075db)

    await member.add_roles(verifiedrole)
    await member.remove_roles(unverifiedrole)
    await member.create_dm()
    await member.dm_channel.send(embed=embed)

@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You are already verified!")

    else:
        await ctx.send("Unknown Error has Occurred. If the issue persists please dm the owner or admin.")


# Clear Command
@bot.command(name="clear") # Still Needs Improvment in message clear number accuracy
@commands.has_permissions(manage_messages=True)
async def clear(ctx, count: int):
    await ctx.channel.purge(limit=count, check=is_not_pinned)
    await ctx.channel.send(f'{count} message(s) has been cleared')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify how much messages you want to clear. Example: ec.clear 5")

    else:
        await ctx.send("Unknown Error has Occurred. If the issue persists please dm the owner or admin.")

# Ban Command
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.create_dm()
    await member.dm_channel.send(f"""You have been banned from Exchange Center by {ctx.author.mention}. Reason: {reason}. 
    If you think that you have been falsely or unfairly banned then fill out this form: https://forms.gle/Qk2Q8k7EZhYBUKTu9""")
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to use this command.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention the member that you want to ban. Example: ec.ban @member [reason]")

    else:
        await ctx.send("Unknown Error has Occurred. If the issue persists please dm the owner or admin.")

# Kick Command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.create_dm()
    await member.dm_channel.send(f"You have been kicked from Exchange Center by {ctx.author.mention}. Reason: {reason}")
    await member.kick(reason=reason)
    await ctx.send(f"{member} was kicked")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to use this command")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention the member that you want to kick. Example: ec.kick @member [reason]")

    else:
        await ctx.send("Unknown Error has Occurred. If the issue persists please dm the owner or admin.")

@bot.command()
async def wanted(ctx, user: discord.Member=None):
    await ctx.send("Command Not Avaliable Now")

@bot.command()
async def expointsinfo(ctx):
    await ctx.send("Command Not Avaliable Now")

@bot.command()
async def createaccount(ctx):
    await ctx.send("Command Not Avaliable Now")

@bot.command()
async def accountinfo(ctx, user: discord.Member=None):
    await ctx.send("Command Not Avaliable Now")


@slash.slash(name="ping", description="Displays the ping speed in milliseconds(ms)")
async def _ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


# Bot Token
bot.run(os.environ['ExchangeToken'])
