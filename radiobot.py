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
PREFIX = os.getenv("DISCORD_RADIOBOT_PREFIX")       # e.g. "!"
SOURCE = os.getenv("DISCORD_RADIOBOT_SOURCE")       # e.g. "http://nthmost.net:8000/mutiny-studio"
ENCODING = "ogg"                                    # options: ogg, mp3  (default: ogg)

client = Bot(command_prefix="$")

player = None
volume_config = 1.0

@client.event
async def on_ready():
    print('KSTK Player Ready')


@client.command(name="eu")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")


@client.command(name="ouvintes")
async def web_listeners(ctx):
    await ctx.send(f"Ouvintes conectados em {SOURCE}")


async def do_play(ctx):
    global player
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        # user is not in a Voice Channel
        await ctx.send(f"You need to join a Voice Channel for me to know where to play the stream!")
        return

    try:
        player = await channel.connect()
        player.source = PCMVolumeTransformer(player.source, volume=volume_config)
    except CommandInvokeError:
        print("Attempt to play without user in channel")
    except Exception as err:
        print(err)
        pass
    if player:
        if ENCODING == "mp3":
            player.play(FFmpegPCMAudio(SOURCE))
        else:
            player.play(FFmpegOpusAudio(SOURCE))

        #player.source = PCMVolumeTransformer(player.source, volume)
    else:
        print("Could not initialize player.")



@client.command(aliases=['p', 'pla','toc'])
async def play(ctx):
    await do_play(ctx)


@client.command(aliases=['s', 'stp','par'])
async def stop(ctx):
    if player:
        if not ctx.author.voice or not ctx.author.voice.channel:# Muestra un error si estás conectado a un canal de voz.
            return await ctx.reply('Você não está em um canal de voz.')
        player.stop()

@client.command(aliases=['v', 'vol'])
async def volume(ctx, *args):
    if player:
        new_volume = float(args[0])
        if 0 <= new_volume <= 100:
            new_volume = new_volume / 100
            if not ctx.author.voice or not ctx.author.voice.channel:# Muestra un error si estás conectado a un canal de voz.
                return await ctx.reply('Você não está em um canal de voz.')
            
            if not ctx.voice_state.is_playing: # Muestra un error si no se está reproduciendo una música.
                return await ctx.reply('Nenhuma música tocando.')
            
            if ctx.author.voice.channel != ctx.guild.me.voice.channel: # Muestra un error si no está conectado al mismo canal de voz del bot.
                return await ctx.reply('Você não está conectado a um canal de voz.')
        
            ctx.voice_state.current.source.volume = new_volume 
            await ctx.send(f"Volume alterado para {args[0]}")
        else:
            await ctx.send('O volume precisa estar entre 0 e 100')



client.run(TOKEN)

