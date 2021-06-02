# discord-music-bot

This is a discord bot that plays music in your server

a) Install everything mentioned in the requirements.txt<br>
b) Also install ffmpeg using: <br>

Debian based OS (Ubuntu, Raspberry Pi OS, Debian 10)<br>
```$sudo apt install ffmpeg```<br>

Using Snap<br>
```$sudo snap install ffmpeg```<br>

c)Create a bot/app in the discord developer platform<br>
d)Note your discord bot TOKEN<br>
e)Add the TOKEN variable: ```$export TOKEN=YOUR_TOKEN```<br>
f)Use the OAuth2 link and add the bot to your desired discord bot<br>
g)You can change the docker bot prefix: ```$export PREFIX=PREFIX_CHARACTER```<br>
Example: ```$export PREFIX=!```<br>

Default character is: ```&```

## Execution
```$python3 bot.py```<br>

## Bot commands:

a) ```&join``` => Telling the bot to join the VC (important for playing music)<br>
b) ```&play <Youtube URL>``` => Plays the audio from youtube url<br>
c) ```&pause``` => Pausing the song<br>
d) ```&resume``` => Resume music<br>
e) ```&queue``` => Shows the music queue list<br>
f) ```&skip``` => Skips the music to the next song<br>
g) ```&stop``` => Stops music and clears queue<br>

## Container Usage
https://hub.docker.com/repository/docker/raghavtinker/discordmusicbot<br>
### Limitations:
a) It can only play stuff from youtube<br>
b)Youtube playlists dont work yet<br>
c)Everything else it 'should' play