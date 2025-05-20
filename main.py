import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ydl_opts = {
    'format': 'bestaudio',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'auto'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Musisz być na kanale głosowym.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *, query):
    vc = ctx.voice_client
    if not vc:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            vc = await channel.connect()
        else:
            await ctx.send("Dołącz do kanału głosowego.")
            return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            url = info['url']
            title = info.get('title', 'Nieznany tytuł')
        except Exception as e:
            await ctx.send("Błąd przy pobieraniu: " + str(e))
            return

    vc.stop()
    vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
    await ctx.send(f"▶️ Odtwarzam: {title}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()

bot.run('TWOJ_TOKEN_BOTA')

