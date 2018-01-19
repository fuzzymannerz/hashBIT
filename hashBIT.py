'''
    hashBIT Discord Bot
    [Returns cryptocurrency rates]
    by Fuzzy Mannerz (fuzzy#8620) - 2018 | fuzzytek.ml
	https://github.com/fuzzymannerz/hashBIT
'''
version = "0.1 beta"

import discord, requests, json
from discord.ext import commands

description = '''Returns cryptocurrency rates in EUR, GBP & USD.'''
bot = commands.Bot(command_prefix='#', description=description)

# Set some variables
genericError = 'There has been an error. 😞 Please try again later or raise an issue on GitHub (fuzzymannerz/hashBIT) for help including the following message:'
rateError = 'There was an error getting the rates. 😞 Please check that you have used a valid coin abbreviation. Try `#bit help` to view available commands.'

@bot.event
async def on_ready():
    print('Logged in as ', bot.user.name)
    print(bot.user.id)
    print('-------------------------------------------------------------------------------------------------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('-------------------------------------------------------------------------------------------------')

    # Set the "playing" text
    await bot.change_presence(game=discord.Game(name='#bit help'))

# Remove default help command
bot.remove_command('help')

# Create the 'bit' command group
@bot.group(pass_context=True)
async def bit(cmd):
    if cmd.invoked_subcommand is None:
        await bot.say('That didn\'t work. 😞 Try `#bit help` to see available commands.')

# Info command
@bit.command()
async def info():
    try:
        application_info = await bot.application_info()
        serverCount = len(bot.servers)

        await bot.say('\n**Bot Information**\n\
        				\n**hashBIT Version**: {}\
        				\n**Discord Version**: {}\
        				\n**hashBIT Bot Username**: {}\
        				\n**hashBIT Bot ID**: {}\
        				\n**hashBIT Connected Servers**: {}\
        				\
        				\n\n*Cryptocurrency data is retrieved from cryptocompare.com*\
        				\n*Bot created and run by Fuzzy ({})*'.format(version, discord.__version__, application_info.name, application_info.id, serverCount, application_info.owner, ))

    except Exception as e:
        await bot.say(genericError)
        await bot.say(e)
        return

# Help command
@bit.command()
async def help():
    try:
        await bot.say('\n**Help**\n\
        				\nCurrent rate of a coin: `#bit rate [coin abbreviation]` eg. `#bit rate btc` or `#bit rate eth`\
        				\nShow this help text: `#bit help` \
        				\nShow bot invite URL: `#bit invite` \
        				\nView information about this bot: `#bit info`')
    except Exception as e:
        await bot.say(genericError)
        await bot.say(e)
        return

# Invite command
@bit.command()
async def invite():
    try:
        await bot.say('\n**Invite URL**\n\
        				\nInvite the bot to another server with this URL:\
        				\nhttps://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
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

        await bot.say('**1 {}** = €{} / £{} / ${} (USD)'.format(coin, apidata['EUR'], apidata['GBP'], apidata['USD']))

    except (Exception):
        await bot.say(rateError)
        return

# If there is an error of no argument in "#bit rate [arg]"
@rate.error
async def rate_handler(ctx, error): 
    await bot.say("Rate command format is `#bit rate [coin abbreviation]` eg. `#bit rate btc` or `#bit rate eth`. See `#bit help` for other commands.")


# Run the bot using token from Discord developer app page (The token below is invalid and just an example)
bot.run('NDAzMzY2Nzk5MjY3MzMyMDk3.DUGQgg.5aqah8cKs3tC5J8TV7Dv-C_xErc')
