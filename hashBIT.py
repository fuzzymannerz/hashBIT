'''
    hashBIT Discord Bot
    [Returns cryptocurrency rates]
    by Fuzzy Mannerz (fuzzy#8620) - 2018 | fuzzytek.ml
    https://github.com/fuzzymannerz/hashBIT
'''
version = "0.5"

import discord, requests, time
from discord.ext import commands

description = '''Returns cryptocurrency rates in EUR, GBP & USD.'''

cmdPrefix = '#'  # Set the prefix for commands. Default is "#" - hence the name.

# CHANGE THE "-" BELOW TO A "#" WHEN CHANGING TO PRODUCTION SCRIPT
bot = commands.Bot(command_prefix=cmdPrefix, description=description)

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


# Set some variables
genericError = 'There has been an error. 😞 Please try again later or raise an issue on GitHub (fuzzymannerz/hashBIT) for help including the following message:'
rateError = 'There was an error getting the rates. 😞 Please check that you have used a valid coin abbreviation. Try `{}bit help` to view available commands.'.format(cmdPrefix)
embedFooter = 'hashBIT v{}. | {}bit help to view commands.'.format(version, cmdPrefix)

# Set links for the info section
botlistLink = 'https://discordbots.org/bot/403366799267332097s'
githubLink = 'https://github.com/fuzzymannerz/hashBIT'
profileImage = 'https://raw.githubusercontent.com/fuzzymannerz/hashBIT/master/hashbit_profile.png'

# Get the current time
currentTime = time.strftime("%H:%M", time.gmtime())

@bot.event
async def on_ready():
    print('Logged in as ', bot.user.name)
    print(bot.user.id)
    print('-------------------------------------------------------------------------------------------------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('-------------------------------------------------------------------------------------------------')

    # Set the "playing" text
    await bot.change_presence(game=discord.Game(name='{}bit help'.format(cmdPrefix)))

# Remove default help command
bot.remove_command('help')

# Create the 'bit' command group
@bot.group(pass_context=True)
async def bit(cmd):
    if cmd.invoked_subcommand is None:
        await bot.say('That didn\'t work. 😞 Try `{}bit help` to see available commands.'.format(cmdPrefix))

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

        e.add_field(name='About hashBIT', value='**hashBIT v{} - Created by fuzzy#8620**. {} {}'.format(version, botlistLink, githubLink))

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

        e = discord.Embed(colour=0xffd400, url='https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
        e.set_footer(text=embedFooter)

        e.set_author(name='hashBIT Invite URL', icon_url=profileImage)
        e.set_thumbnail(url=profileImage)

        e.add_field(name='Invite Link', value='You can invite hashBIT to another server using the following URL:\n \
                                             **https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8**'.format(bot.user.id))

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
        api = requests.get("https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=EUR,GBP,USD".format(coin))
        apidata = api.json()

        e = discord.Embed(colour=0x00ff5c)
        e.set_footer(text= embedFooter)

        e.set_author(name='hashBIT {} Rate'.format(coin), icon_url=profileImage)

        e.add_field(name='💶 Euros', value='**€{}**'.format(apidata['EUR']))
        e.add_field(name='💷 Pound Sterling', value='**£{}**'.format(apidata['GBP']))
        e.add_field(name='💵 US Dollars', value='**${}**'.format(apidata['USD']))

        await bot.say(embed=e)

    except Exception as ex:
        if api.status_code != "200":
            await bot.say ("**There was an error on the other end that is out of hashBIT's control. Please try again later.**")
            await bot.say("**Returned error:** {}".format(ex))
        else:
            await bot.say(rateError)
        return

# If there is an error of no argument in "#bit rate [arg]"
@rate.error
async def rate_handler():
    await bot.say("Rate command format is `{}bit rate [btc|eth|men|xrp etc...]` See `{}bit help` for other commands.".format(cmdPrefix, cmdPrefix))


# Run the bot using token from Discord developer app page (The token below is invalid and just an example)
bot.run('NDAzMzY2Nzk5MjY3MzMyMDk3.DUGQgg.5aqah8cKs3tC5J8TV7Dv-C_xErc')
