import os

from discord import FFmpegOpusAudio, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext.commands import Bot
from discord.ext.commands.errors import CommandInvokeError
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_RADIOBOT_TOKEN")
PREFIX = os.getenv("DISCORD_RADIOBOT_PREFIX") + ' '     
SOURCE = os.getenv("DISCORD_RADIOBOT_SOURCE")      

client = Bot(command_prefix=PREFIX,description="Eu sou um bot para transmitir músicas por streaming <3")

player = None
volume_config = 1.0

@client.event
async def on_ready():
    print('Rádio Boberto pronto!')


@client.command(name="ouvintes")
async def web_listeners(ctx):
    await ctx.send(f"Ouvintes conectados em {SOURCE}")


#muito gambiarra isso. Pela amor de deus! Refatorar assim que possível
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
        await ctx.guild.voice_client.disconnect()
    except Exception as err:
        print(err)
        pass
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.reply('Você não está em um canal de voz.')
    if player:
        try:
            player.play(FFmpegPCMAudio(SOURCE))
            player.source = PCMVolumeTransformer(player.source)
            player.source.volume = 1.0
        except:
            await ctx.guild.voice_client.disconnect()
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
        
@client.command(aliases=['rest', 'rein'])
async def reiniciar(ctx):
    await ctx.reply('Ok... você quer me matar, né?! Tudo bem.')
    await ctx.bot.logout()
    await client.run(TOKEN)


client.run(TOKEN)

