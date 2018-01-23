![](https://i.imgur.com/CNfAtAK.png)

[![Discord Bots](https://discordbots.org/api/widget/status/403366799267332097.svg?noavatar=true)](https://discordbots.org/bot/403366799267332097) [![Discord Bots](https://discordbots.org/api/widget/lib/403366799267332097.svg?noavatar=true)](https://discordbots.org/bot/403366799267332097) [![Discord Bots](https://discordbots.org/api/widget/owner/403366799267332097.svg?noavatar=true)](https://discordbots.org/bot/403366799267332097)

# hashBIT
A cryptocurrency rate Discord bot.

## Invite To Server
[https://discordapp.com/oauth2/authorize?client_id=403366799267332097&scope=bot&permissions=216129](https://discordapp.com/oauth2/authorize?client_id=403366799267332097&scope=bot&permissions=216129)

## Commands
The following commands are currently available:    

Show rate of a coin: `#bit rate [btc|eth|ltc|xrp etc...]` eg. `#bit rate btc` or `#bit rate eth`    
Show a graph of closing prices: `#bit graph [btc|eth|ltc|xrp etc...]` eg. `#bit graph btc` or `#bit graph eth`    
Show the help text: `#bit help`    
Show bot invite URL: `#bit invite`
Clean previous hashBIT messages: `#bit clean`  
View information about the bot: `#bit info`    

----------

## Self Hosting

### Requirements    
- Python >= 3.4
- discord.py library [(https://github.com/Rapptz/discord.py)](https://github.com/Rapptz/discord.py)
- requests library [(http://python-requests.org)](http://python-requests.org)
- requests_cache library [(https://pypi.python.org/pypi/requests-cache)](https://pypi.python.org/pypi/requests-cache)
- madplotlib library [(https://matplotlib.org/)](https://matplotlib.org/)
- pandas library [(https://pandas.pydata.org/)](https://pandas.pydata.org/)
- schedule library [(https://pypi.python.org/pypi/schedule)](https://pypi.python.org/pypi/schedule)
- A Discord app & token

Note: Most of the required libraries can be instaled with `pip`. (`python3-pip` package)

### Usage
1. Register an app on the Discord developer page. [https://discordapp.com/developers/applications/me](https://discordapp.com/developers/applications/me)
2. Make the app into a user and copy the token into the end of the code.
3. Create a folder named `temp` in the directory containing the `hashBIT.py` script and give it read and write permissions for the user that runs the script.
4. Save and run it

On Linux you can run the following to open the script as a background process:
```
pnohup python3 hashBIT.py &
disown
```
Or you can use screen:
```
sudo apt install screen
screen -S hashbit
python3 hashBIT.py
```

----------
*Rate data provided by [cryptocompare.com](https://cryptocompare.com)*

----------
## Donate
If you like my work please consider a donation to show your appreciation and support. :)

**[PayPal](https://paypal.me/fuzzymannerz)**       
**BTC:** 1Q1Q4LZK8ghrcX6jxxuPa95bwvu6bVUdsY
