##########################################################
## hashBIT Discord Bot                                  ##
##                  [Returns cryptocurrency rates]      ##
##                                                      ##
## by Fuzzy Mannerz (fuzzy#8620) - 2018 | fuzzytek.ml   ##
## https://github.com/fuzzymannerz/hashBIT              ##
##########################################################

version = "0.6.1"

import discord, requests, time
from discord.ext import commands

description = '''Returns cryptocurrency rates in EUR, GBP & USD.'''

cmdPrefix = '#'  # Set the prefix for commands. Default is "#" - hence the name.

bot = commands.Bot(command_prefix=cmdPrefix, description=description)

# Set some variables
genericError = 'There has been an error. 😞 Please try again later or raise an issue on GitHub (fuzzymannerz/hashBIT) for help including the following message:'
rateErrorText = 'There was an error getting the rates. 😞 Please check that you have used a valid coin abbreviation. Try `{}bit help` to view available commands.'.format(cmdPrefix)
embedFooter = 'hashBIT v{} | {}bit help to view commands.'.format(version, cmdPrefix)

# Set links for the info section
botListLink = 'https://discordbots.org/bot/403366799267332097'
githubLink = 'https://github.com/fuzzymannerz/hashBIT'
profileImage = 'https://raw.githubusercontent.com/fuzzymannerz/hashBIT/master/hashbit_profile.png'

# Get the current time
currentTime = time.strftime("%H:%M", time.gmtime())

# Bot uptime stats
startTime = time.time()

def formatTime(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd %dh %dm %ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh %dm %ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm %ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)

def upTime():
    return formatTime(time.time() - startTime)

# Print login information to the server console
@bot.event
async def on_ready():
    print('\nLogged in as: [{}] | User ID: [{}] | Start time: [{}]'.format(bot.user.name, bot.user.id, currentTime))
    print('\n----------------------------------------------------------------------------------------------')
    print('Use this link to invite {} to a server:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=216129'.format(bot.user.id))

    # Set the "playing" text
    await bot.change_presence(game=discord.Game(name='{}bit help'.format(cmdPrefix)))

# Remove default help command
bot.remove_command('help')

# Create the 'bit' command group
@bot.group(pass_context=True)
async def bit(cmd):
    if cmd.invoked_subcommand is None:

        e = discord.Embed(colour=0xff0000)

        e.set_footer(text=embedFooter)
        e.set_author(name='ERROR', icon_url=profileImage)
        e.add_field(name='\u200b', value='That didn\'t work. 😞\nTry `{}bit help` to see available commands.'.format(cmdPrefix))

        await bot.say(embed=e)

# Info command
@bit.command()
async def info():
    try:
        application_info = await bot.application_info()
        serverCount = len(bot.servers)
        uptime = upTime()

        e = discord.Embed(title='Bot Information', colour=0xffd400)

        e.set_footer(text='{} | Rate data provided by cryptocompare.com'.format(embedFooter))

        e.set_thumbnail(url=profileImage)

        e.add_field(name='hashBit Version', value=version)
        e.add_field(name='Discord Version', value=discord.__version__)
        e.add_field(name='hashBIT Bot Username', value=application_info.name)
        e.add_field(name='hashBIT Bot ID', value=application_info.id)
        e.add_field(name='Connected Servers', value=str(serverCount))
        e.add_field(name='hashBIT Uptime', value=uptime)

        e.add_field(name='\u200b', value='\u200b') # Create a blank line

        e.add_field(name='About hashBIT', value='**hashBIT v{} - Created by fuzzy#8620**. {} {}'.format(version, botListLink, githubLink))

        await bot.say(embed=e)

    except Exception as e:
        await bot.say(genericError)
        await bot.say(e)
        return

# Help command
@bit.command()
async def help():
    try:
        e = discord.Embed(colour=0xffd400)
        e.set_footer(text=embedFooter)

        e.set_author(name='hashBIT Help', icon_url=profileImage)
        e.set_thumbnail(url=profileImage)

        e.add_field(name='Get a coin rate', value='```{}bit rate [btc|eth|men|xrp etc...]```'.format(cmdPrefix))
        e.add_field(name='Show the help text', value='```{}bit help```'.format(cmdPrefix), inline=False)
        e.add_field(name='Show bot invite URL', value='```{}bit invite```'.format(cmdPrefix), inline=False)
        e.add_field(name='View bot information', value='```{}bit info```'.format(cmdPrefix), inline=False)

        await bot.say(embed=e)

    except Exception as e:
        await bot.say(genericError)
        await bot.say(e)
        return

# Invite command
@bit.command()
async def invite():
    try:
        e = discord.Embed(colour=0xffd400, url='https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=216129'.format(bot.user.id))
        e.set_footer(text=embedFooter)

        e.set_author(name='hashBIT Invite URL', icon_url=profileImage)
        e.set_thumbnail(url=profileImage)

        e.add_field(name='Invite Link', value='You can invite hashBIT to another server using the following URL:\n \
                                             **https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=216129**'.format(bot.user.id))
        await bot.say(embed=e)

    except Exception as e:
        await bot.say(genericError)
        await bot.say(e)
        return

# Get coin information
@bit.command()
async def rate(coin : str):
    try:
        coin = coin.upper()
        priceAPI = requests.get("https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=EUR,GBP,USD".format(coin))
        priceData = priceAPI.json()

        coinDataAPI = requests.get("https://www.cryptocompare.com/api/data/coinlist/")
        coinData = coinDataAPI.json()
        coinName = coinData['Data'][coin]['FullName']

        coinImage =  coinData['BaseImageUrl'] + coinData['Data'][coin]['ImageUrl']

        e = discord.Embed(colour=0x00ff5c)
        e.set_footer(text= embedFooter)

        if coinName and coinImage:
            e.set_author(name='{} Rate'.format(coinName), icon_url=coinImage)
        if coinName and not coinImage:
            e.set_author(name='{} Rate'.format(coinName), icon_url=profileImage)
        if coinImage and not coinName:
            e.set_author(name='{} Rate'.format(coin), icon_url=coinImage)
        if not coinName and not coinImage:
            e.set_author(name='{} Rate'.format(coin), icon_url=profileImage)

        e.add_field(name='💶 Euros', value='**€{}**'.format(priceData['EUR']))
        e.add_field(name='💷 Pound Sterling', value='**£{}**'.format(priceData['GBP']))
        e.add_field(name='💵 US Dollars', value='**${}**'.format(priceData['USD']))

        await bot.say(embed=e)

    except (Exception):
        await rateError()
        return

# Rate error embed
async def rateError():
    e = discord.Embed(colour=0xff0000)

    e.set_footer(text=embedFooter)
    e.set_author(name='ERROR', icon_url=profileImage)
    e.add_field(name='\u200b', value=rateErrorText)

    await bot.say(embed=e)

# Deal with mentions and PMs to the bot
@bot.event
async def on_message(message):
    # If user mentions the bot in chat channel
    if message.author.bot:
        return
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        await bot.add_reaction(message, '👍')
        await bot.send_message(message.channel,'Hi {0.mention}, try `{1}bit help` to see my commands.'.format(message.author, cmdPrefix))

    # If user PMs the bot
    if message.channel.is_private:
         await bot.send_message(message.author,'Hey {}, I don\'t currently accept PMs.\nFor now, please use `{}bit help` in the chat channel for assistance. 🙂'.format(message.author, cmdPrefix))
         return

    await bot.process_commands(message)

# If there is an error of no argument in "#bit rate [arg]"
@rate.error
async def rate_handler(ctx, error):

    e = discord.Embed(colour=0xff0000)

    e.set_footer(text= embedFooter)
    e.set_author(name='ERROR', icon_url=profileImage)
    e.add_field(name='\u200b', value='Rate command format is `{0}bit rate [coin]`\nSee `{0}bit help` for other commands and more information.'.format(cmdPrefix))

    await bot.say(embed=e)


# Run the bot using token from Discord developer app page (The token below is invalid and just an example)
bot.run('NDAzMzY2Nzk5MjY3MzMyMDk3.DUGQgg.5aqah8cKs3tC5J8TV7Dv-C_xErc')
