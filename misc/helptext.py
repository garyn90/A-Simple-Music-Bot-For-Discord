"""
below is the dictionary containing all the descriptions for each command, to be passed in for the help command
for those wishing to customize this bot, have fun with this. just be sure to not alter the keys (left side of colon);
"""

helpText = {
    # for music related commands

    'clearBrief': 'Purges queue',
    'clearDesc': 'Purges entire queue. Use with caution, you might lose aux cord privileges.',

    'leaveBrief': 'Leaves voice.',
    'leaveDesc': 'If I am in a call, I leave. The queue is cleared.',

    'nowplayingBrief': 'Embed of song',
    'nowplayingDesc': 'Send current song info, including name, requester, and duration.',

    'pauseBrief': 'Pauses song.',
    'pauseDesc': 'Pauses song, if playing. I will leave if idling too long.',

    'playBrief': 'Pass song or query',
    'playDesc': 'You can pass in a link to a single song, or query Youtube for it. If there is a queue, I\'ll add it.',

    'plistBrief': 'Pass in a playlist URL',
    'plistDesc': 'You must provide a link to a (not-private) Youtube playlist.',
    
    'queueBrief': 'Displays queue',
    'queueDesc': 'Displays the queue, and if there\'s a playlist, shows playlist title, and its track count.',
    
    'repeatBrief': 'Repeats current song, once.',
    'repeatDesc': 'Takes the current song and repeats it, once.',

    'repeat3Brief': 'Repeat current song 3x.',
    'repeat3Desc': 'The current song is repeated 3 times. If a playlist, repeats it three times in playlist.',

    'repeat5Brief': 'Repeat current song 5x',
    'repeat5Desc': 'Repeats the current song 5 times. If a playlist, loops current song 5 times.',

    'resumeBrief': 'Resume, if paused.',
    'resumeDesc': 'Resume if paused. Be quick, I might just leave.',

    'skipBrief': 'Skips current song',
    'skipDesc': 'Skips the current song. If a playlist, skips the current song in playlist.',

    # for other commands

    'danceBrief': 'I dance.',
    'danceDesc': 'Sometimes it\'s fun to just shake it.',
    
    'wisdomBrief': 'A nugget of wisdom',
    'wisdomDesc': 'The world is an odd place. A word of advice from your beloved bot.'

}