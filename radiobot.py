import os

from discord import FFmpegOpusAudio, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext.commands import Bot
from discord.ext.commands.errors import CommandInvokeError
from dotenv import load_dotenv
load_dotenv()
# A spot to keep these details handy while you're collecting them...
# 
# client id: 
# public key: 
# client secret: 
# bot permissions: 66583360
# TOKEN:
 


TOKEN = os.getenv("DISCORD_RADIOBOT_TOKEN")         # collected from Discord Bot setup process.
PREFIX = os.getenv("DISCORD_RADIOBOT_PREFIX") + ' '      # e.g. "!"
SOURCE = os.getenv("DISCORD_RADIOBOT_SOURCE")       # e.g. "http://nthmost.net:8000/mutiny-studio"                                  # options: ogg, mp3  (default: ogg)

client = Bot(command_prefix=PREFIX,description="Eu sou um bot para transmitir músicas por streaming <3")

player = None
volume_config = 1.0

@client.event
async def on_ready():
    print('Rádio Boberto pronto!')


@client.command(name="ouvintes")
async def web_listeners(ctx):
    await ctx.send(f"Ouvintes conectados em {SOURCE}")

async def do_play(ctx):
    global player

    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        await ctx.send(f"Você precisa entrar em um canal de voz para eu saber onde reproduzir o stream!")
        return 

    try:
        player = await channel.connect()
    except CommandInvokeError:
        print("Tentando tocar sem nenhum usuário no canal.")
    except Exception as err:
        print(err)
        pass
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.reply('Você não está em um canal de voz.')
    if player:
        player.play(FFmpegPCMAudio(SOURCE))
        player.source = PCMVolumeTransformer(player.source)
        player.source.volume = 1.0
    else:
        print("Não foi possível iniciar o player.")



@client.command(aliases=['p', 'pla','toc','r','repr'])
async def play(ctx):
    await do_play(ctx)


@client.command(aliases=['s', 'stp','par'])
async def stop(ctx):
    if player:
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.reply('Você não está em um canal de voz.')
        player.stop()

@client.command(aliases=['v', 'vol'])
async def volume(ctx, *args):
    new_volume = float(args[0])
    if 0 <= new_volume <= 100:

        new_volume = new_volume / 100
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.reply('Você não está em um canal de voz.')
        source = ctx.guild.voice_client.source
        if not isinstance(source, PCMVolumeTransformer):
            return await ctx.send("Erro. Volume não suportado para essa interface de som. Chame o outro boberto.")
        source.volume = new_volume        
        await ctx.send(f"Volume alterado para {args[0]}")
    else:
        await ctx.send('O volume precisa estar entre 0 e 100')

@client.command(aliases=['sai', 'exit'])
async def sair(ctx, *args):
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.reply('Você não está em um canal de voz.')
    await ctx.guild.voice_client.disconnect()
    await ctx.reply('Ok... você me excluiu da fofoca :(')
        



client.run(TOKEN)

