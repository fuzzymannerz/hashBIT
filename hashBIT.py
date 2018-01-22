##########################################################
## hashBIT Discord Bot                                  ##
##                  [Returns cryptocurrency rates]      ##
##                                                      ##
## by Fuzzy Mannerz (fuzzy#8620) - 2018 | fuzzytek.ml   ##
## https://github.com/fuzzymannerz/hashBIT              ##
##########################################################
version = "1.0.2"

import discord, os, requests, datetime, requests_cache, time, asyncio, schedule, matplotlib
from discord.ext import commands

matplotlib.use('Agg')  # Stops matplotlib from trying to use a xwindows backend
import matplotlib.pyplot as plt
import pandas as pd

# from PIL import Image
# import numpy as np
# from io import BytesIO

# Enable caching for the API (Default is 5 minutes)
requests_cache.install_cache('coinRateCache', expire_after=300)
requests_cache.clear()

# Set the bot description and prefix
description = '''Returns cryptocurrency rates in EUR, GBP & USD.'''
cmdPrefix = '-'  # Set the prefix for commands. Default is "#" - hence the name.

bot = commands.Bot(command_prefix=cmdPrefix, description=description)

# Set some variables
genericError = 'There has been an error. 😞 Please try again later or raise an issue on GitHub (fuzzymannerz/hashBIT) for help including the following message:'
rateErrorText = 'There was an error getting the rates. 😞 Please check that you have used a valid coin abbreviation. Try `{}bit help` to view available commands.'.format(
    cmdPrefix)
embedFooter = 'hashBIT v{} | {}bit help to view commands.'.format(version, cmdPrefix)

# Set links for the info section
botListLink = 'https://discordbots.org/bot/403366799267332097'
githubLink = 'https://github.com/fuzzymannerz/hashBIT'
profileImage = 'https://raw.githubusercontent.com/fuzzymannerz/hashBIT/master/hashbit_profile.png'

# Set the bot permissions for invite links
perms = "216129"

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
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}'.format(bot.user.id, perms))

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
        e.add_field(name='\u200b',
                    value='That didn\'t work. 😞\nTry `{}bit help` to see available commands.'.format(cmdPrefix))

        await bot.say(embed=e)


# Info command
@bit.command(pass_context=True)
async def info(ctx):
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
        e.add_field(name='Server Owner', value=ctx.message.server.owner)

        e.add_field(name='\u200b', value='\u200b')  # Create a blank line
        e.add_field(name='\u200b', value='\u200b')  # Create a blank line
        e.add_field(name='\u200b', value='\u200b')  # Create a blank line

        e.add_field(name='About hashBIT',
                    value='**hashBIT v{} - Created by fuzzy#8620**. {} {}'.format(version, botListLink, githubLink))

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

        e.add_field(name='Get a coin rate', value='```{}bit rate [btc|eth|ltc|xrp etc...]```'.format(cmdPrefix))
        e.add_field(name='Show a graph of the previous week',
                    value='```{}bit graph [btc|eth|ltc|xrp etc...]```'.format(cmdPrefix))
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
        e = discord.Embed(colour=0xffd400,
                          url='https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}'.format(
                              bot.user.id, perms))
        e.set_footer(text=embedFooter)

        e.set_author(name='hashBIT Invite URL', icon_url=profileImage)
        e.set_thumbnail(url=profileImage)

        e.add_field(name='Invite Link', value='You can invite hashBIT to another server using the following URL:\n \
                                             **https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions={}**'.format(
            bot.user.id, perms))
        await bot.say(embed=e)

    except Exception as e:
        await bot.say(genericError)
        await bot.say(e)
        return


# Get coin information
@bit.command()
async def rate(coin: str):
    try:
        coin = coin.upper()
        priceAPI = requests.get("https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=EUR,GBP,USD".format(coin))
        priceData = priceAPI.json()

        coinDataAPI = requests.get("https://www.cryptocompare.com/api/data/coinlist/")
        coinData = coinDataAPI.json()
        coinName = coinData['Data'][coin]['FullName']

        coinImage = coinData['BaseImageUrl'] + coinData['Data'][coin]['ImageUrl']

        e = discord.Embed(colour=0x00ff5c)
        e.set_footer(text=embedFooter)

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


# Method to get the daily price from API
def dailyPrice(symbol, comparison_symbol, limit=7, aggregate=1):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}' \
        .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df


# Remove the saved graph image cache each day
def removeTempImages():
    dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir("{}/temp".format(dir))

    # Clear the rate cache
    requests_cache.clear()
    # print ("Rate cache was cleared.")

    # Remove temp folder graph images
    for file in files:
        if file.endswith("_graph.png"):
            os.remove("{}/temp/{}".format(dir, file))
            # print ("Temp images were removed.")


# Schedule a time to clean out the temp folder of graph images
schedule.every().day.at("00:00").do(removeTempImages)


async def scheduleTimer():
    schedule.run_pending()


async def graphImageCleaner():
    await bot.wait_until_ready()

    while not bot.is_closed:
        await scheduleTimer()
        await asyncio.sleep(1)


# Method to generate, download and store a coin graph image
def saveGraphImage(coin: str):
    try:
        coin = coin.upper()

        coinDataAPI = requests.get("https://www.cryptocompare.com/api/data/coinlist/")
        coinData = coinDataAPI.json()
        coinName = coinData['Data'][coin]['FullName']

        # TODO:
        # Get the image of the coin to put on the graph
        # coinImage = coinData['BaseImageUrl'] + coinData['Data'][coin]['ImageUrl']
        # response = requests.get(coinImage)
        # coinImage = Image.open(BytesIO(response.content))

        # Graph settings
        coinHistoryEUR = dailyPrice(coin, 'EUR')
        coinHistoryGBP = dailyPrice(coin, 'GBP')
        coinHistoryUSD = dailyPrice(coin, 'USD')

        plt.clf() # Reset plt

        plt.suptitle("{} 7 Day History".format(coinName), fontsize=15, ha='center')
        plt.xticks(rotation=45)
        plt.ylabel("Closing Price", fontsize=14)
        plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=[0, 0.03, 1, 0.95])
        plt.grid(True)

        # Plot the values
        plt.plot(coinHistoryEUR.timestamp, coinHistoryEUR.close, label='Euros')
        plt.plot(coinHistoryGBP.timestamp, coinHistoryGBP.close, label='Pound Sterling')
        plt.plot(coinHistoryUSD.timestamp, coinHistoryUSD.close, label='US Dollars')
        plt.legend()

        # Save the Image to the server and return it to the user
        fileName = "{}_graph".format(coin)
        dir = os.path.dirname(os.path.abspath(__file__))
        plt.savefig('{}/temp/{}.png'.format(dir, fileName), dpi=80)
        os.chmod('{}/temp/{}.png'.format(dir, fileName), 0o777)
        return 1

    except Exception as e:
        return e


# Show graph of the previous 7 days.
@bit.command(pass_context=True)
async def graph(ctx, coin: str):
    coin = coin.upper()
    dir = os.path.dirname(os.path.abspath(__file__))
    try:
        if os.path.isfile("{}/temp/{}_graph.png".format(dir, coin)):
            await bot.send_file(ctx.message.channel, "{}/temp/{}_graph.png".format(dir, coin))
        else:  # If image isn't already there download it for the chosen coin
            try:
                getGraph = saveGraphImage(coin)
                if getGraph:
                    await bot.send_file(ctx.message.channel, "{}/temp/{}_graph.png".format(dir, coin))
                else:
                    raise Exception(getGraph)

            # If the bot couldn't get or create the image for some reason...
            except Exception as e:
                await bot.say("There has been an error. :(")
                print("Graph image error: {}".format(e))

                # If self hosting, feel free to uncomment the following block
                # so you will get notified via PM if something is wrong with the graph system:

                # await bot.send_message(ctx.message.channel,"There was an error with getting the graph image, this is a server configuration issue and the server owner has been notified.")
                # await bot.send_message(ctx.message.server.owner, "Hey! There has been an error with a request for a {} graph image from a user of your server. Please be sure to check the `temp` directory exists in the script root and is readable and writable to the user running the bot script. The error is as follows: ***{}*".format(coin, e))
                # await wbot.send_message(ctx.message.server.owner, "The script automatically generates and downloads images from the temp folder if an image for the chosen coin does not already exist, it then keeps it for 12 hours before removing it from the server.")
                # await bot.send_message(ctx.message.server.owner, "If you are having trouble, feel free to ask for help over on https://github.com/fuzzymannerz/hashBIT or message Discord user **fuzzy#8620**")

    except Exception as e:
        await rateError()
        print(e)
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
        await bot.send_message(message.channel,
                               'Hi {0.mention}, try `{1}bit help` to see my commands.'.format(message.author,
                                                                                              cmdPrefix))

    # If user PMs the bot
    if message.channel.is_private:
        await bot.send_message(message.author,
                               'Hey {}, I don\'t currently accept PMs.\nFor now, please use `{}bit help` in the chat channel for assistance. 🙂'.format(
                                   message.author, cmdPrefix))
        return

    await bot.process_commands(message)


# If there is an error of no argument in "#bit rate [arg]"
@rate.error
async def rate_handler(ctx, error):
    e = discord.Embed(colour=0xff0000)

    e.set_footer(text=embedFooter)
    e.set_author(name='ERROR', icon_url=profileImage)
    e.add_field(name='\u200b',
                value='Rate command format is `{0}bit rate [coin]`\nSee `{0}bit help` for other commands and more information.'.format(
                    cmdPrefix))

    await bot.say(embed=e)


# Run the graph image cleaner in the background
bot.loop.create_task(graphImageCleaner())

# Run the bot using token from Discord developer app page
bot.run('YOUR-APP-TOKEN-HERE)
