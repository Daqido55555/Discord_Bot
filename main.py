import discord
from discord.ext import commands
import asyncio
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Konfiguracja dla yt-dlp
yt_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'noplaylist': True,
    'extract_flat': 'in_playlist'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')


@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Dołączyłem do kanału głosowego.")
    else:
        await ctx.send("Musisz być na kanale głosowym!")


@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Rozłączono.")
    else:
        await ctx.send("Nie jestem na żadnym kanale głosowym.")


@bot.command(name='play')
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        await ctx.invoke(join)

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        url = info['url']

    source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
    ctx.voice_client.stop()
    ctx.voice_client.play(source, after=lambda e: print(f'Odtwarzanie zakończone: {e}'))

    await ctx.send(f"▶️ Odtwarzam: {info.get('title')}")


@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Zatrzymano odtwarzanie.")
    else:
        await ctx.send("Nie odtwarzam niczego.")


# Wklej tutaj swój token bota
bot.run('TWOJ_TOKEN_BOTA')

