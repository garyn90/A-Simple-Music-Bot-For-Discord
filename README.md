# discord.py-music-bot
A simple music bot for Discord.


This project was made using Python and the discord.py library. It's configured in a way for beginners or those with no coding knowledge to take this code and host it themselves. Those who wish to improve this bot are encouraged to do so - the intent is to provide the most basic (yet customizable) functionality. 

## **To those who have some coding experience, or are intermediate:**

You can freely take this code and improve upon it to your own ends. This music bot assumes you have a small server. So there are no role-based restrictions, nor does it require certain permissions enabled (for private channels, simply allow it to read them). Feel free to add those restrictions yourselves, by looking at the documentation of discord.py: https://discordpy.readthedocs.io/en/stable/. For further instructions on how to customize this, look for the section below titled: "Customization" 

## **To complete beginners:**

If you wish to have a personal music bot, yet don't know code or have no desire to, this bot should contain everything you need. Simply look into the /misc subdirectory, and you will find certain python files (namely: messages.py, wisdom.py, and helptext.py) that you can customize to your heart's content. Discord encourages customization and for each server to feel like a completely different place, so feel free changing the texts within. Just be mindful to not mess with the structure itself - just change everything on the right side of the colon. 

# **Creating a bot with Discord**

2)It's assumed you already have a discord account and are the owner of a server.
  a)Sign into discord.com, and navigate over to here: https://discord.com/developers/docs/intro.
  Read that, and then head over to Applications, to create your bot.
  
  b)Once there, click on the New Application button on the top right. Give it a name and click "Create".
  
  c)Once inside the application's main page, navigate to and click on "Bot" (should be on the left side of the page). Click "Add Bot" on that page, and confirm.
  Keep the settings for "Public Bot" (must be checked) and "Require OAuth2 Code Grant" (keep unchecked).
  
  d)Once the bot has been created, it will have a token (look for "Token" underneath the name of your bot). Copy that and save it somewhere. You will need it in just   a bit. **It is imperative you don't share this with anybody. This is essentially
  the password to your bot, which you will need for this code. Hold onto that somewhere.**
  
  e)This isn't mandatory, but remember to add a photo for your bot. Customizing this bot in tandem with whatever "character" you have in mind is ideal. For mine, it's   a beautiful little pug.

# **Adding your bot to your server**  

1)Navigate to the "OAUTH2" tab. Check "bot" under "Scopes". 

2)Then, another embed titled "Bot Permissions" will show up (underneath the link). 
These are all the permissions you're granting your bot. 
On the left column, check "View Channels". In the middle, check "Send Messages", "Embed Links", and "Add Reactions", and on the final column, check "Connect" and "Speak" are checked.

3)Once 2) is done, copy the url that's generated. Then, paste that url into your browser, select the server you want your bot to show up in, and invite it in. **This assumes you have the "manage server" permission.**

When all steps are done, the bot should have joined your server. Now, onto the code.

**The following steps are best done with a code editor or IDE. Pick any which one you like, though I'd recommend Visual Studio Code.**

# **Customizing Instructions**
If you wish to look at and tinker with the code yourself, a few requirements:
**What you will need:**

1)First and foremost, be sure to install the latest version of python at https://www.python.org/downloads/.
(Windows users: Be sure to allow it to add itself to the PATH). Once installed, navigate to your terminal or command prompt, and type "python3 -V". It will list the current version. 

3)Then, install discord.py, by following the instructions here: https://discordpy.readthedocs.io/en/stable/intro.html. Be sure to follow the "Installing" tab very carefully, and install all those modules using pip.

Optional: 4)If you wish to work on this in your local environment you will need FFMPEG. You can download it here, and you can install it wherever (just remember to add it to your PATH). https://www.ffmpeg.org/download.html
You will also need to add FFMPEG to your PATH (if you are on Windows 10). Hit your Windows key, type "Edit system variables", then navigate to the Advanced Tab. Click the "Environment Variables" button.
Under the "User variables for ..." click on Path, then "Edit". A new window should open up. Click "New" on that new window, and add the path to the FFMPEG \bin folder there. It should look something like: ..something\..something\FFMPEG\bin. 
Hit "OK", then "OK", and you should have FFMPEG added to your PATH.

### **Once you have your project set up in an editor (opening the whole folder in an editor is ideal)**

### **Changing the command prefix**

Navigate to bot.py. On line 27 should be:

"bot = commands.Bot(command_prefix='-', intents=intents)"

You can alter the prefix of the commands by changing the value inside the quotes of "command_prefix=' '" into whatever you desire. Be sure to consult the documentation here:
https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=command%20prefix#discord.ext.commands.Bot.command_prefix

### **Changing the bot picture:**

This can be done on the applications page of your discord bot.

### **Changing responses/error messages**:
Inside /misc you will find three files: helpText.py, wisdom.py, and messages.py. 

**helpText.py** is what houses all the text for the -help command, which comes stock with all bots made with discord.py. Changing the contents of those are entirely up to you. Just keep the "keys" of the dictionary intact, and simply change the strings. And mind the commas. Those are important. This data structure is called a dictionary. Please refer to the official Python documentation for an in-depth look.

**wisdom.py**
This is an easter egg of sorts. Think of it like a magic 8-ball offering advice, yet with wisdom.py there is no limit to the randomized result your bot can post.
wisdom.py features a list (see the Python docs for full information). If you wish to alter this entirely, go right ahead! Just keep the list data structure in mind when altering (again: mind the commas).

**messages.py**
These are written for the messages sent into the discord server, either to confirm a command, or notify the user something went wrong. For example, if somebody tries to get the bot to join a call and they're not in a voice channel, it yields an error. The code handles that one, and posts in the server:

"Try joining a voice channel first."

Like the other 2 files, messages.py can be customized, so you can have fun with what messages get sent. Whether it be an insult, or calling somebody specifically out by username, is completely up to you. This data structure is called a dictionary. Please see the official Python documentation for a dive into it.

### **Adding your own commands**

If you wish to add non-music related commands of your own, try housing them within the otherCog.py file. otherCog.py was built specifically for this, to separate the music functionality from other functionality. It's highly recommended to read the documentation, since adding commands will require a primer of sorts. This bot was made with the discord.ext commands framework, but it's not extremely difficult at all to add your own commands. Consult the discord.py documentation to learn how to get started: https://discordpy.readthedocs.io/en/latest/ext/commands/index.html


 ## **How to host**
 
 ### **What you need**
 
 1)You will need that token generated by your bot from the applications page earlier. Hold onto that.
 
 2)Create a heroku account, opting for the free tier.
 
 3)Save these hyperlinks somewhere. You will need these for what heroku calls **buildpacks**:
 
 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
 
 https://github.com/infinitepower18/heroku-buildpack-libopus.git
 
 ### **If the above criteria is met**
 
 1)Navigate to settings, and click "Reveal config vars". Add BOT_TOKEN as KEY, and simply copy-paste your token into the VALUE. Save that. 
 
 2)Then just underneath, click "add buildpack". First, click on "python" ("under officially supported buildpacks"). Once heroku/python appears, add the two buildpacks links from earlier. Make sure the two links from above, and heroku/python are listed in your buildpacks. 
 
 3)Inside your heroku app, navigate to the "Deploy" tab and follow all the instructions for "Deploy using heroku git". This will involve using either your command  prompt or terminal. Be sure to follow those instructions to a T.
 
 4)Once the repo has been pushed onto your heroku app, navigate to the "Resources" tab and under "Dynos" you will see "Free Dynos" which requires you to edit first, and switch the button to on. Be sure to do that.
 
 If you followed the instructions carefully, your bot should come online and be able to start playing music for you! Enjoy.
