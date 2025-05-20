import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="Daq", intents=intents)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
async def help(ctx):
    embed=discord.Embed(title=Commands, description=Prefix: Daq/daq, color=0xf5c211)
    embed.set_author(name=DaqBot)
    embed.add_field(name=ping, value=Look your ping, inline=True)
    embed.add_field(name=help, value=Bot commands, inline=True)
    embed.add_field(name=Play, value=Playing your love music, inline=True)
    embed.set_footer(text=Help command)
    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))

