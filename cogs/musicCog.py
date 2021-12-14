###############################################################################################
# cog for music
###############################################################################################

from discord.ext import commands
from discord.errors import *
from discord.ext.commands import cog
from discord.utils import get

from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from youtube_dl.utils import DownloadError 
from embeds.embeds import *

from misc.helptext import helpText
from misc.messages import messages

class MusicCog(commands.Cog, name='Music Commands'):
    # attributes
    def __init__(self, bot: commands.bot):
        self.bot = bot
    # array, containing the dictionaries returned by query functions
        self.queue = []
    # attributes for voice state of bot
        # whether in voice
        self.inVoice = False 
        # needed for error handling     
        self.voiceChannel = False
        # saves initial channel, for event listeners
        self.chatChannel = False
        self.paused = False
    # dict to pass in as options parameter for yt query
        self.ytOptions = {
            'default_search': 'auto',
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]}
    # dict for FFMPEG
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }

    # helper function to search YT and return results in anonymous dictionary
    async def ytQuery(self, ctx):
        # cut out '-play ' from string
        chopIt = ctx.message.content.replace('-play ', '')
        chopIt.strip()
        with YoutubeDL(self.ytOptions) as yt:
               info = yt.extract_info('ytsearch: %s' % (chopIt), download=False)['entries'][0]
        # YTDL returns a rich dict, necessary for bot-side functionality, and sending 
        # user-side information. extract the source for VC functionality, and everything else
        # to include in the embed
        return {'source': info['formats'][0]['url'], 
                'title': info['title'], 
                'channel_url': info['channel_url'], 
                'duration': info['duration'], 
                'thumbnail': info['thumbnail'],
                'webpage_url': info['webpage_url']}

    # function to start indexing the playlist into a subarray in self.queue
    async def plistQuery(self, ctx):
        # cut out '-playlist ' from string
        chopIt = ctx.message.content.replace('-playlist', '')
        with YoutubeDL(self.ytOptions) as yt:
            try:
                playlist = yt.extract_info(chopIt, download=False)['entries']
                return {
                    # 'playlist' is crucial for processing logic
                    'playlist': True,
                    'title': playlist[0]['playlist_title'],
                    'url': chopIt,
                    'songs': [{
                        'source': item['formats'][0]['url'],
                        'duration': item['duration'],
                        'thumbnail': item['thumbnail'],
                        'title': item['title'],
                        'url': item['webpage_url']
                        } for item in playlist                
                    ]
                }
            except:
                raise
            
    # removes first song in queue, then plays the next one - with after param, we can be recursive
    # and if the queue ends, we just pass on exceptions
    # removes first song in queue, then plays the next one - with after param, we can be recursive
    # and if the queue ends, we just pass on exceptions
    def playNext(self, ctx):
        if 'playlist' in self.queue[0]:
            try:
                self.queue[0]['songs'].pop(0)
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.play(FFmpegPCMAudio(self.queue[0]['songs'][0]['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
            except (IndexError, AttributeError, KeyError):
                print('End of playlist.')
                self.queue.pop(0)
                pass
        elif not self.queue:
            print('No entries in queue.')
        # i don't know why this was even here
        #elif not 'playlist' in self.queue[0]:
        #    pass
        else:
            try:
                self.queue.pop(0)
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.play(FFmpegPCMAudio(self.queue[0]['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
            # don't even throw an error, just pass
            # passing exceptions as tuples triggers if any exception in tuple yields true   
            except (AttributeError, IndexError):
                print('End of track.')
                try:
                    self.queue.pop(0)
                except:
                    pass
                pass
        
    # bot state cleaner function to reduce bloat 
    def stateCleanup(self):
        self.inVoice = False
        self.voiceChannel = False
        self.chatChannel = False
        self.paused = False
        self.queue.clear()

    # if user asks for now playing, provide with currently playing song
    @commands.command(brief=helpText['nowplayingBrief'], description=helpText['nowplayingDesc'], aliases=['song'])
    async def nowplaying(self, ctx):
        if self.queue:
            await ctx.send(embed=nowPlayingEmbed(ctx, self.queue[0]))
        else:
            await ctx.send(messages['noPlay'])        

    # skip to next song in queue, if any
    @commands.command(brief=helpText['skipBrief'], description=helpText['skipDesc'], aliases=['next'])
    async def skip(self, ctx):
        # using voice.stop() triggers the playNext recursion, don't use!
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if self.queue and self.voiceChannel:
            # skip track in the playlist, by iterating over the subnested 'songs' list
            try: 
                if 'playlist' in self.queue[0]:
                    voice.pause()
                    await ctx.send(embed=skipEmbed(self.queue, ctx))
                    self.queue[0]['songs'].pop(0)
                    voice.play(FFmpegPCMAudio(self.queue[0]['songs'][0]['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
                elif not 'playlist' in self.queue[0]:
                    voice.pause()
                    await ctx.send(embed=skipEmbed(self.queue, ctx))
                    self.queue.pop(0)
                    if 'playlist' in self.queue[0]:
                        voice.play(FFmpegPCMAudio(self.queue[0]['songs'][0]['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
                    else:
                        voice.play(FFmpegPCMAudio(self.queue[0]['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
            except IndexError:
                pass
        # don't skip at all, there is nothing to skip to
        elif len(self.queue) == 1:
            await ctx.send(messages['noSkip'])
        # self-explanatory
        elif not self.queue:
            await ctx.send(messages['noQueue'])

    # clear the queue
    @commands.command(brief=helpText['clearBrief'], description=helpText['clearDesc'], aliases=['clearqueue'])
    async def clear(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if self.queue:
            if voice.is_playing():
                voice.stop() 
            self.queue.clear()
            await ctx.send(messages['onClear'])
        elif not self.queue:
            await ctx.send(messages['noQueue'])

    # pause current song
    @commands.command(brief=helpText['pauseBrief'], description=helpText['pauseDesc'], )
    async def pause(self, ctx):
        #if self.inVoice:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.pause()
            self.paused = True 
            await ctx.send(messages['onPause'])   
    
    # resume song, if paused
    @commands.command(brief=helpText['resumeBrief'], description=helpText['resumeDesc'], )
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if self.paused:
            voice.resume()
            self.paused = False
            await ctx.send(messages['onResume'])     
        # else:
        #     await ctx.send('Not currently paused.')

    # play
    @commands.command(brief=helpText['playBrief'], description=helpText['playDesc'], )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def play(self, ctx, args):
       # if not connected, hop in and start playing
        if not self.queue and not self.inVoice:
            self.chatChannel = ctx.message.channel.id 
            channel = ctx.author.voice.channel
            await channel.connect()
            self.inVoice = True
            self.voiceChannel = ctx.author.voice.channel
            try:
                link = await self.ytQuery(ctx)
            except:
                raise 
            self.queue.append(link)
            # as of writing, no other alternative with commands ext     
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.play(FFmpegPCMAudio(link['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
            await ctx.send(embed=nowPlayingEmbed(ctx, self.queue[0]))
        # if already in voice and playing, just add it to the queue
        elif len(self.queue) > 0 and self.inVoice: 
            await self.addSongToQueue(ctx)
        # if idle in voice with no songs, just start playing again 
        elif len(self.queue) == 0 and self.inVoice:
           link = await self.ytQuery(ctx)
           self.queue.append(link)
           voice = get(self.bot.voice_clients, guild=ctx.guild)
           voice.play(FFmpegPCMAudio(link['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
           await ctx.send(embed=nowPlayingEmbed(ctx, self.queue[0]))

    # checks if bot is in voice and if there's a queue. if so, adds it to the queue     
    async def addSongToQueue(self, ctx):
            link = await self.ytQuery(ctx)
            await ctx.send('Adding `' + link['title'] + '` to the queue.')
            self.queue.append(link)

    # since we're keeping -playlist and -play separate, mirror the previous function
    async def addPlistToQueue(self, ctx):
        link = await self.playlistQuery(ctx)
        await ctx.send('Adding `' + link['title'] + '` to the queue.')
        self.queue.append(link)

    # leave    
    @commands.command(brief=helpText['leaveBrief'], description=helpText['leaveDesc'], aliases=['git', 'disconnect'])
    async def leave(self, ctx):    
        # try leaving
        if self.inVoice:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            await voice.disconnect()
            await ctx.message.add_reaction('<:white_check_mark:910764702223704085>')
            self.stateCleanup()
        # if it can't, raise the error to be handled
        else:
            raise commands.CommandInvokeError
    
    # queue command, displays content of song queue
    @commands.command(brief=helpText['queueBrief'], description=helpText['queueDesc'], aliases=['list'])
    async def queue(self, ctx):
        await ctx.send(embed=queueEmbed(self.queue))

    # repeat current song, once
    @commands.command(brief=helpText['repeatBrief'], description=helpText['repeatDesc'])
    async def repeat(self, ctx):
        await ctx.send(embed=repeatEmbed(self.queue, ctx))
        if 'playlist' in self.queue[0]:
            copiedSong = self.queue[0]['songs'][0]
            self.queue[0]['songs'].insert(1, copiedSong)    
        else:
            copiedSong = self.queue[0]
            self.queue.insert(1, copiedSong)

    # repeat current song 3 times
    @commands.command(brief=helpText['repeat3Brief'], description=helpText['repeat3Desc'])
    async def repeat3(self, ctx):
        if 'playlist' in self.queue[0]:
            await ctx.send(embed=repeat3Embed(self.queue, ctx))
            loopedSong = self.queue[0]['songs'][0]
            for i in range(1, 4):
                self.queue[0]['songs'].insert(i, loopedSong)
        else:               
            await ctx.send(embed=repeat3Embed(self.queue, ctx))
            loopedSong = self.queue[0]
            for i in range(1, 4):
                self.queue.insert(i, loopedSong)
    
    # and repeat current 5 times
    @commands.command(brief=helpText['repeat5Brief'], description=helpText['repeat5Desc'])
    async def repeat5(self, ctx):
        if 'playlist' in self.queue[0]:
            await ctx.send(embed=repeat5Embed(self.queue, ctx))
            loopedSong = self.queue[0]['songs'][0]
            for i in range(1, 4):
                self.queue[0]['songs'].insert(i, loopedSong)
        else:
            await ctx.send(embed=repeat5Embed(self.queue, ctx))
            loopedSong = self.queue[0]
            for i in range(1, 6):
                self.queue.insert(i, loopedSong)

    # the playlist queuer. users must provide a link to an already existing playlist
    @commands.command(brief=helpText['plistBrief'], description=helpText['plistDesc'])
    async def playlist(self, ctx):
        # joins if not in call
        if not self.queue and not self.inVoice:
            self.chatChannel = ctx.message.channel.id 
            await ctx.author.voice.channel.connect()
            self.inVoice = True
            self.voiceChannel = ctx.author.voice.channel
            await ctx.send(messages['onEnqueue'])
            link = await self.plistQuery(ctx)
            self.queue.append(link)
            # as of writing, no other alternative with commands ext     
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.play(FFmpegPCMAudio(self.queue[0]['songs'][0]['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
            await ctx.send(embed=nowPlayingEmbed(ctx, self.queue[0]))
             
        # if already in voice and playing, just add it to the queue
        elif len(self.queue) > 0 and self.inVoice: 
            await self.addPlistToQueue(ctx)
        # if idle in voice with no songs, just start playing again 
        elif len(self.queue) == 0 and self.inVoice:            
           link = await self.plistQuery(ctx)
           self.queue.append(link)
           voice = get(self.bot.voice_clients, guild=ctx.guild)
           voice.play(FFmpegPCMAudio(link['source'], **self.ffmpeg_options), after=lambda e: self.playNext(ctx))
           await ctx.send(embed=nowPlayingEmbed(ctx, self.queue[0]['songs'][0]))

    ###############################################################################################
    # before_invoke() here. used to take care of stuff without bloating other code
    ###############################################################################################
    
    # checks to see if the bot is not in voice. if it isn't, connect and set states
    @play.before_invoke
    async def confirmQuery(self, ctx):
        if not ctx.args:
            raise commands.MissingRequiredArgument

    # this doesn't seem to work for some reason
    @playlist.before_invoke
    async def confirmPlistQuery(self, ctx):
        if not ctx.args:
            raise commands.MissingRequiredArgument
    
                      
    ###############################################################################################
    # error handling per function. as of writing and given scope of bot, going function by function
    # and tossing the rest to errorCog seems ideal. localize errors per command,
    # then any and all after gets sent up to the errorCog, which functions globally
    ###############################################################################################
            
    # the only time -leave will throw an error if it is not connected. handle it 
    @leave.error 
    async def leaveError(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, TypeError):
                await ctx.send(messages['leaveError'])
        else:
            raise

    # this is actually an embed error. leave for now, see if it works.
    @nowplaying.error 
    async def nowPlayingError(self, ctx, error):
        if isinstance(error, HTTPException):
            await ctx.send(messages['embedError'])
    
    # -play yields a variety of errors out of CommandInvokeError. localize for each 
    @play.error
    async def playError(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # throw if user is trying to use -play to queue a playlist
            if isinstance(error.original, IndexError):
                await ctx.send(messages['playError']['IndexError'])
            # if the query fails
            if isinstance(error.original, (DownloadError)):
                await ctx.send(messages['playError']['DownloadError'])    
            # if the user is not in a channel
            if isinstance(error.original, AttributeError):
                await ctx.send(messages['playError']['AttributeError'])
        # if the user is in another voice channel
        if isinstance(error, ClientException):
            if self.inVoice and (self.voiceChannel != ctx.author.voice.channel):
                await ctx.send(messages['playError']['ClientException'])
        # from pre-invoke; throw if user sends an empty command
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(messages['playError']['MissingParams'])
        else:
            raise

    @pause.error
    async def pauseError(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # if user tries to pause the bot when not paused
            if isinstance(error.original, AttributeError):
                await ctx.send(messages['pauseError'])
        else:
            raise

    @playlist.error
    async def playlistError(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # if user tries to queue a song with the playlist command
            if isinstance(error.original, KeyError):
                await ctx.send(messages['playlistError']['KeyError'])    
            # if user queues a private playlist or a missing one
            if isinstance(error.original, DownloadError):
                await ctx.send(messages['playlistError']['DownloadError'])                
            # on initial join, and user is not in a voice channel
            if isinstance(error.original, AttributeError):
               await ctx.send(messages['playlistError']['AttributeError'])
            # handles if there is no query with the playlist 
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(messages['playlistError']['MissingParams'])
            # makes the wrong query
            if isinstance(error.original, IndexError):
                await ctx.send(messages['playlistError']['IndexError'])
                self.queue.clear()
            # not sure if this works - should throw when HTTPException occurs
            if isinstance(error.original, HTTPException):
                await ctx.send(messages['playlistError']['IndexError'])
                self.queue.clear()
        else:
            raise
    
    @skip.error
    async def skipError(self, ctx, error):
        if isinstance(error, AttributeError):
            if isinstance(error.original, AttributeError):
                await ctx.send(messages['skipError'])
        else:
            raise
             
    ###############################################################################################
    # music cog's event listening. below are event listeners that listen out for voice state 
    # on_voice_state_update() is configured to listen out for:
    # a) the bot being alone in the chat, and disconnecting, resetting its own state
    # b) sitting in the voice call without a song prompted in 30 seconds, which prompts a dc 
    ###############################################################################################

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if all members of voice channel leave, leave as well
        voice = member.guild.voice_client 
        # check to see if the bot is alone
        if voice is not None and len(voice.channel.members) == 1: 
            await voice.disconnect()
            ctxChannel = self.bot.get_channel(self.chatChannel)
            await ctxChannel.send(messages['onAllUsersLeave'])
            self.stateCleanup()

        # disconnect if idle
        if not member.id == self.bot.user.id:
            return
        elif before.channel is None:
            import asyncio
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                # reset if playing and not paused, or reset if paused
                if (voice.is_playing() and not voice.is_paused()) or self.paused:
                    time = 0
                if time == 60:
                    await voice.disconnect()
                    ctxChannel = self.bot.get_channel(self.chatChannel)
                    await ctxChannel.send(messages['onIdleLeave'])
                    self.stateCleanup()
                if not voice.is_connected():
                    break        
     
    # needed to add cog to bot
    def setup(self, bot: commands.Bot):
        bot.add_cog(MusicCog(bot))
