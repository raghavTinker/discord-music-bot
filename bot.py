import discord
from discord.ext import commands,tasks
import os
import asyncio
import youtube_dl


token = ""
server_queue = dict()


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

#joining the channel
@bot.command(name="join")
async def join(ctx):
    global queue
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel!")
        return
    else:
        channel = ctx.message.author.voice.channel
        await ctx.send(f'Connected to ``{channel}``')
    await channel.connect()

#Leaving VC
@bot.command(name="leave")  
async def leave(ctx):
    global queue
    voice_client = ctx.message.guild.voice_client
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Bot left!")
        queue[ctx.guild.id] = []
    else:
        await ctx.send("I am not in the VC")

#Play command
@bot.command(name="play") 
async def play(ctx, url):
    print(type(server_queue))
    voice_client = ctx.voice_client
    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            
            if ctx.guild.id in server_queue:
                #already using the bot
                if(len(server_queue[ctx.guild.id]) == 0):
                    server_queue[ctx.guild.id].append(player)
                    await ctx.send("Playing {}".format(player.title))
                    start_playing(ctx.guild.id, voice_client)
                else:
                    server_queue[ctx.guild.id].append(player)
                    await ctx.send("Added to queue {}".format(player.title))
            else:
                server_queue[ctx.guild.id] = [player]
                await ctx.send("Playing {}".format(player.title))
                start_playing(ctx.guild.id, voice_client)
    except Exception as error:
        print(error)
        await ctx.send("Something went wrong, try again later")
                
#Playing music
def start_playing(server_id, voice_client):
    if(len(server_queue[server_id]) != 0):
        player = server_queue[server_id][0]
        try:
            voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else queuePlayer(server_id, voice_client))
        except:
            print("unkown error!")
        #Removing stuff from the list
    else:
        print("queue over")

#Queue management
def queuePlayer(server_id, voice_client):
    if server_id in server_queue:
        server_queue[server_id].pop(0)
    else:
        print("empty")
    start_playing(server_id, voice_client)

#Pause
@bot.command(name="pause")
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client

    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("I am not playing anything")

#Resume
@bot.command(name="resume")
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await ctx.send("Resuming...")
        await voice_client.resume()
    else:
        await ctx.send("I am not playing anything")

#Skip
@bot.command(name="skip")
async def skip(ctx):
    #skip the track
    print("skip")
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()

#Queue
@bot.command(name="queue")
async def queue(ctx):
    message = ""
    for player in server_queue[ctx.guild.id]:
        message = message + player.title + "\n"
    await ctx.send(message)

#Stop music
@bot.command(name="stop")
async def stop(ctx):
    server_queue = {}
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    await ctx.send("Stopped, queue removed")

#Now playing
@bot.command(name="np")
async def np(ctx):
    await ctx.send("Playing {}".format(server_queue[ctx.guild.id][0].title))

#Token input
try:
    print(os.environ['TOKEN'])
    token = str(os.environ['TOKEN'])
    bot.run(token)
except:
    print("Invalid token")
