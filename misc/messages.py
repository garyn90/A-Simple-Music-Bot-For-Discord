###############################################################################################
# this is the module where all messages sent to the server are kept.
# take the time to read each one, and change however you see fit, 
# just be mindful not to change the 'keys' (left side of the colon)
###############################################################################################


messages = {
    ###############################################################################################
    # below are the exceptions for musicCog
    ###############################################################################################

    # errors thrown on -play command, subnested 
    'playError': {
        # if user misuses -play command, queries odd request
        'IndexError': 'Something went wrong. If you are trying to queue a playlist, try the "-playlist" command with a link to the playlist.',
        # if YTDL has a DownloadError
        'DownloadError': 'Something went wrong. Try again.',
        # if user is not in a voice channel when called
        'AttributeError': 'Try joining a voice channel first.',
        # if user calls play, but bot is active in another channel
        'ClientException': 'I am in another voice channel.',
        # if user uses -play without a paramter
        'MissingParams': 'You have to pass something in with the -play command.',
    },

    # the one error thrown on leave    
    'leaveError': 'I am not connected to any channel.',

    # sends when nothing is playing
    'noPlay': 'Nothing currently playing.',

    # sends when there is nothing in queue
    'noQueue': 'No songs in the queue', 

    # sends when there are no other songs in the the queue    
    'noSkip': 'No other songs in the queue.',

    # sent when a user clears the entire queue
    'onClear': 'Queue has been cleared.',

    'onEnqueue': 'Enqueuing playlist. Give me a moment.',

    # message sent when user asks to pause the player
    'onPause': 'Paused.', 

    # message sent when it resumes playback
    'onResume': 'Resuming.', 

    # only throws error if asked to pause, and isn't connected
    'pauseError': 'I am not currently connected.',

    # subnested dictionary for all the errors thrown by -playlist
    'playlistError': {
        # when users queues an odd playlist, or not a playlist
        'KeyError': 'Are you sure that is a playlist? Try again.',
        # error when YTDL fails to download query
        'DownloadError': 'Can\'t find that. Are you sure it still exists, and if so, isn\'t private?',
        # error thrown when user queues first entry as playlist, but isn't connected
        'AttributeError': 'Try joining a voice channel first.',
        # if it's missing necessary query 
        'MissingParams': 'You have to pass something in with the command!',
        # when it just goes south for an indiscernible reason
        'IndexError': 'Something went wrong. Cancelling query.',
        'HTTPException': 'Something went wrong. Are you sure you provided a link to your playlist?'    
    },

    # error when queue entry is missing relevant information for the embed
    'embedError': 'I can\'t make an embed. Query is missing important data.',

    # sent when user asks to skip while not being in a call.
    'skipError': 'You\'re not in a call.',

    ###############################################################################################
    # below are the exception messages for errorCog
    ###############################################################################################

    # users will be put on cooldown with commands after command spamming
    'Cooldown': 'Slow your roll. Try again in 3 seconds.',
    
    # user does an unknown command
    'cmdNotFound': 'That is not a command. Please use -help for a list of commands, or have fun with your fingers elsewhere.',

    ###############################################################################################
    # below are the messages for event listening
    # messages sent when a)leaves if everybody leaves, 
    # or b)leaves when left idle
    ###############################################################################################

    'onAllUsersLeave': 'Everybody left. Guess I\'ll be going now...',

    'OnIdleLeave': 'Disconnected after being idle.'

}
