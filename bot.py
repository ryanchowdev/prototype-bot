#!/usr/bin/env python3

# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.presences = True

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

# basic currency converter
@bot.command(name='cc',
    brief='Converts amount from orig to new currency. Use $help cc for more info.',
    description=('Usage: $cc <amount> <orig_currency> <new_currency>'
        '\nThis bot currently supports the following currencies:'
        '\n\'usd\', \'eur\''
        '\nExample: $cc 50 usd eur'
    )
)
async def cc(ctx, amt:float, orig_c, new_c):
    ratios_dict = {'usd_to_eur': 0.84, 'eur_to_usd': 1.18}

    if orig_c == 'usd' and new_c == 'eur':
        value = round(amt * ratios_dict['usd_to_eur'], 2)
        response = f'${amt} equals {value}€'
        await ctx.send(response)
    if orig_c == 'eur' and new_c == 'usd':
        value = round(amt * ratios_dict['eur_to_usd'], 2)
        response = f'{amt}€ equals ${value}'
        await ctx.send(response)

# bot say - Admin only
@bot.command(name='say',
    brief='Use the bot to say something. Admins only.')
@commands.has_role('Admin')
async def say(ctx, *args):
    guild = ctx.guild
    message = ' '.join(args)

    await ctx.message.delete()
    await ctx.send(message)

# bot announcement - Admin only
@bot.command(name='announce',
    brief='Use the bot to make an announcement. Admins only.')
@commands.has_role('Admin')
async def announce(ctx, *args):
    guild = ctx.guild
    message = ' '.join(args)
    announcement_channel = discord.utils.get(guild.channels, name='announcements')

    await ctx.message.delete()
    await announcement_channel.send(message)

bot.run(TOKEN)
