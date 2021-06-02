import discord
from discord.ext import commands,tasks
import os
import asyncio
import youtube_dl


token = ""
queue = []

#Prefix input
prefix = ""
try:
    print(os.environ['PREFIX'])
    prefix = str(os.environ['PREFIX'])
except:
    prefix = '&'
bot = commands.Bot(command_prefix = prefix)


#Youtube stuff. Thanks to stackoverflow
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream or play))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#Discord stuff
@bot.command(name="join")
async def join(ctx):
    global queue
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel!")
        return
    else:
        channel = ctx.message.author.voice.channel
        queue = []
        await ctx.send(f'Connected to ``{channel}``')

    await channel.connect()

@bot.command(name="leave")  
async def leave(ctx):
    global queue
    voice_client = ctx.message.guild.voice_client
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Bot left!")
        queue = []
    else:
        await ctx.send("I am not in the VC")

@bot.command(name="play") 
async def play(ctx, url):
    global queue
    print(len(queue))

    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)

            if len(queue) == 0:
                queue.append(player)
                print(queue)
                start_playing(ctx.voice_client)
                await ctx.send("Playing {}".format(player.title))

            else:  
                queue.append(player)
                await ctx.send("added queue {}".format(player.title))
    except Exception as error:
        print(error)
        await ctx.send("Somenthing went wrong - please try again later!")

def start_playing(voice_client):
    if(len(queue) != 0):
        player = queue[0]
        try:
            voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else queuePlayer(voice_client))
        except:
            print("unkown error!")
        #Removing stuff from the list
    else:
        print("queue over")

def queuePlayer(voice_client):
    global queue
    queue.pop(0)
    start_playing(voice_client)

@bot.command(name="pause")
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client

    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("I am not playing anything")

@bot.command(name="resume")
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await ctx.send("Resuming...")
        await voice_client.resume()
        queuePlayer(ctx.voice_client)
    else:
        await ctx.send("I am not playing anything")

@bot.command(name="skip")
async def skip(ctx):
    #skip the track
    print("skip")
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()

@bot.command(name="queue")
async def queue(ctx):
    global queue
    message = ""
    for player in queue:
        message = message + player.title + "\n"
    await ctx.send(message)

@bot.command(name="stop")
async def stop(ctx):
    global queue
    queue = []

    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    await ctx.send("Stopped, queue removed")

@bot.command(name="np")
async def np(ctx):
    global queue
    await ctx.send("Playing {}".format(queue[0].title))
#Token input
try:
    print(os.environ['TOKEN'])
    token = str(os.environ['TOKEN'])
    bot.run(token)
except:
    print("Invalid token")