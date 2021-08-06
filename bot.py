#!/usr/bin/env python3

# bot.py
import os
import random
import discord
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
from discord.ext import commands
from dotenv import load_dotenv
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
from pyowm import OWM
from yahoo_fin import stock_info as si

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WEATHER = os.getenv('WEATHER_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.presences = True

cr = CurrencyRates()
bc = BtcConverter()

owm = OWM(WEATHER)
mgr = owm.weather_manager()

bot = commands.Bot(intents=intents, command_prefix='$')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    # Set "Watching" status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))

    print(
        f'{bot.user.name}: Successfully connected to {guild.name} (id: {guild.id})\n'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    greetings = [
        f'Hello {message.author.mention}',
        f'Hola {message.author.mention}',
        f'Bonjour {message.author.mention}',
        f'Hallo {message.author.mention}',
        f'Hej {message.author.mention}',
        f'Hei {message.author.mention}',
        f'Hallå {message.author.mention}',
        f'你好 {message.author.mention}',
        f'Здравствуйте {message.author.mention}',
        f'Ciao {message.author.mention}',
        f'Ahoj {message.author.mention}',
        f'Zdravo {message.author.mention}',
        f'γεια {message.author.mention}',
        f'{message.author.mention} مرحبا',
        f'{message.author.mention} שלום',
        f'Aloha {message.author.mention}',
        f'こんにちは {message.author.mention}',
        f'안녕하세요 {message.author.mention}',
        f'Witaj {message.author.mention}',
        f'Olá {message.author.mention}',
        f'Merhaba {message.author.mention}',
        f'Xin chào {message.author.mention}'
    ]

    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        response = random.choice(greetings)
        await message.channel.send(response)

    await bot.process_commands(message)

# error reporting
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.NoPrivateMessage):
        return await ctx.send('Sorry, this command cannot be used in private messages.')
    if isinstance(error, commands.errors.CheckFailure):
        return await ctx.send('You do not have the required role to use this command.')
    if isinstance(error, commands.errors.MissingRequiredArgument):
        return await ctx.send(f'Invalid usage. Use \'$help {ctx.command}\' for more info.')

# currency converter using forex-python
@bot.command(name='cc',
    brief='Converts amount from orig to new currency. Use $help cc for more info.',
    description=('Usage: $cc <amount> <orig_currency> <new_currency>')
)
async def cc(ctx, amt:float, orig_c, new_c):
    upper_orig_c = orig_c.upper()
    upper_new_c = new_c.upper()
    value = cr.convert(upper_orig_c, upper_new_c, amt)
    response = f'{amt:.2f} {upper_orig_c} = {value:.2f} {upper_new_c}'
    await ctx.send(response)

# convert bitcoin to currency using forex-python
@bot.command(name='frombtc',
    brief='Converts amount in BTC to desired currency. Use $help frombtc for more info.',
    description=('Usage: $frombtc <amount> <currency>')
)
async def frombtc(ctx, amt:float, curr):
    upper_curr = curr.upper()
    value = bc.convert_btc_to_cur(amt, upper_curr)
    response = f'{amt} BTC = {value:.2f} {upper_curr}'
    await ctx.send(response)

# convert currency to bitcoin using forex-python
@bot.command(name='tobtc',
    brief='Converts amount in desired currency to BTC. Use $help tobtc for more info.',
    description=('Usage: $tobtc <amount> <currency>')
)
async def tobtc(ctx, amt:float, curr):
    upper_curr = curr.upper()
    value = bc.convert_to_btc(amt, upper_curr)
    response = f'{amt:.2f} {upper_curr} = {value} BTC'
    await ctx.send(response)

def to_celsius(temp):
    return (temp - 32) / 1.8

# obtain weather data with OpenWeatherMap and pyowm
@bot.command(name='weather',
    brief='Get weather data from OpenWeatherMap.',
    description=('Usage: $weather <location>\n'
        'You may include the country after the city name if you wish, separated by a comma. ex "$weather london,uk"')
)
async def weather(ctx, *args):
    location = ' '.join(a.upper() for a in args)
    observation = mgr.weather_at_place(location)
    w = observation.weather

    status = w.detailed_status

    temp = w.temperature(unit='fahrenheit')
    temp_f = temp['temp']
    temp_c = to_celsius(temp_f)
    high_f = temp['temp_max']
    high_c = to_celsius(high_f)
    low_f = temp['temp_min']
    low_c = to_celsius(low_f)
    feels_like_f = temp['feels_like']
    feels_like_c = to_celsius(feels_like_f)

    humidity = w.humidity

    sunrise_utc = w.sunrise_time(timeformat='date')
    sunset_utc = w.sunset_time(timeformat='date')
    offset = w.utc_offset
    sunrise = (sunrise_utc + datetime.timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S")
    sunset = (sunset_utc + datetime.timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S")

    response = (f'Weather data for {location}.\n'
            f'**Status**: {status}\n'
            f'**Temperature**: {temp_f:.2f}F / {temp_c:.2f}C\n'
            f'**High**: {high_f:.2f}F / {high_c:.2f}C\n'
            f'**Low**: {low_f:.2f}F / {low_c:.2f}C\n'
            f'**Feels like**: {feels_like_f:.2f}F / {feels_like_c:.2f}C\n'
            f'**Humidity**: {humidity}%\n'
            f'**Sunrise**: {sunrise} (local time)\n'
            f'**Sunset**: {sunset} (local time)\n')
    await ctx.send(response)

# obtain stocks data from Yahoo finance
@bot.command(name='stocks',
    brief='Get stocks data from Yahoo Finance.',
    description='Usage: $stocks <symbol> <optional: period>\n'
        'Default period is 1mo. Some examples of valid periods: 5d, 1wk, 1mo, 3mo, 1y, 5y')
async def stocks(ctx, symbol, period='1mo'):
    price = si.get_live_price(symbol)
    ticker = yf.Ticker(symbol.upper())
    ticker_df = ticker.history(period=period)

    ticker_df['Close'].plot()
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'{symbol.upper()} Price Data')
    plt.savefig('stocks.png')
    plt.clf()

    title = f'Current price for {symbol.upper()}: ${price:.2f}'
    file = discord.File('stocks.png', filename='stocks.png')
    embed = discord.Embed()
    embed.title = title
    embed.colour = 0x00FF00 # green
    embed.set_image(url='attachment://stocks.png')
    await ctx.send(file=file, embed=embed)

# Kick - Admin only
@bot.command(name='kick',
    brief='Kick a user. Admins only.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} was kicked for reason: {reason}')

# Ban - Admin only
@bot.command(name='ban',
    brief='Ban a user. Admins only.')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} was banned for reason: {reason}')

# Unban - Admin only
@bot.command(name='unban',
    brief='Unban a user. Admins only.')
@commands.has_permissions(administrator=True)
async def unban(ctx, member, *, reason=None):
    ban_list = await ctx.guild.bans()
    name, tag = member.split('#')

    for b in ban_list:
        user = b.user
        if (user.name, user.discriminator) == (name, tag):
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f'{user} was unbanned for reason: {reason}')

# Make the bot say something - Admin only
@bot.command(name='say',
    brief='Use the bot to say something. Admins only.')
@commands.has_permissions(administrator=True)
async def say(ctx, *args):
    guild = ctx.guild
    message = ' '.join(args)

    await ctx.message.delete()
    await ctx.send(message)

# Make an announcement - Admin only
@bot.command(name='announce',
    brief='Use the bot to make an announcement. Admins only.')
@commands.has_permissions(administrator=True)
async def announce(ctx, *args):
    guild = ctx.guild
    message = ' '.join(args)
    announcement_channel = discord.utils.get(guild.channels, name='announcements')

    await ctx.message.delete()
    await announcement_channel.send(message)

# Change the bot's status - owner only
@bot.command(name='status',
    brief="Change the bot's status. Owner only.")
@commands.is_owner()
async def status(ctx, activity, *name):
    act = activity.upper()
    n = ' '.join(name)

    if (act == 'PLAYING'):
        response = f'Now playing {n}'
        await bot.change_presence(activity=discord.Game(name=n))
    elif (act == 'LISTENING'):
        response = f'Now listening to {n}'
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=n))
    elif (act == 'WATCHING'):
        response = f'Now watching {n}'
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=n))
    else:
        pass

    await ctx.send(response)

bot.run(TOKEN)
