import discord
import os
from discord.ext  import commands
from discord.ext.commands import Bot
import asyncio
import json
from datetime import datetime
from datetime import timedelta
import random
from tinydb import TinyDB
from decimal import Decimal
import requests

db = TinyDB('db.json')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.idle, activity = discord.Game(name="Bottering"))
    
@bot.event
async def on_message(message):
    words = message.content.split()
    for word in words:
      if 'cheers' in word:
        await message.add_reaction('🥂')
        json_object = db.get(doc_id=1)
        previous = json_object["cheerscount"]
        db.update({'cheerscount': previous+1}) 
    await bot.process_commands(message)

@bot.command(name='cc')
async def cheerscount(ctx):
    await ctx.channel.send(f'Cheers count: {db.get(doc_id=1)["cheerscount"]}')

@bot.command()
async def vibecheck(ctx):
    author = ctx.message.author
    rand = random.randint(0,100)
    val = round(rand/10)
    values = ["🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛","🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛","🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛","🟥🟥🟥🟥⬛⬛⬛⬛⬛⬛","🟥🟥🟥🟥🟥⬛⬛⬛⬛⬛","🟩🟩🟩🟩🟩🟩⬛⬛⬛⬛","🟩🟩🟩🟩🟩🟩🟩⬛⬛⬛","🟩🟩🟩🟩🟩🟩🟩🟩⬛⬛","🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛","🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩"]
    if(val==0):val=1 #deal with rounding down to 0 exception
    embed=discord.Embed(title='Vibe Check', description='')
    embed.add_field(name=f'{author.display_name}\'s results are in...', value=f'{rand}%', inline=True)
    embed.add_field(name="["+values[val-1]+"]", value='\u200b', inline=True)
    #if(val<=3):
      #embed.set_image(url = "https://media.giphy.com/media/LH6sMoTmJX7RgBFztN/giphy.gif")
    #elif(4<=val<7):
      #embed.set_image(url = "https://m.media-amazon.com/images/I/91HglIWFg9L._SS500_.jpg")
    #else:
      #embed.set_image(url = "https://media.giphy.com/media/dAbwIpLeH9yEeYXnRw/giphy.gif")
    embed.set_footer(icon_url = author.avatar_url, text = f"Requested by {author.name}")
    await ctx.send(embed=embed)   

@bot.command()
async def time(ctx):
    now = datetime.now()
    now_malay = now+timedelta(hours=5)
    now_aus = now_malay+timedelta(hours=2)
    now_cali = now-timedelta(hours=10)
    now_uk = now-timedelta(hours=2)
    now_texas = now-timedelta(hours=8)
    now_can = now-timedelta(hours=7)
    current_time = now.strftime("%I:%M %p")
    current_time_malay = now_malay.strftime("%I:%M %p")
    current_time_aus = now_aus.strftime("%I:%M %p")
    current_time_cali = now_cali.strftime("%I:%M %p")
    current_time_uk = now_uk.strftime("%I:%M %p")
    current_time_texas = now_texas.strftime("%I:%M %p")
    current_time_can = now_can.strftime("%I:%M %p")
    embed=discord.Embed()
    embed.add_field(name="Bahrain: ", value=current_time, inline=True)
    embed.add_field(name="Ontario: ", value=current_time_can, inline=True)
    embed.add_field(name="Malaysia: ", value=current_time_malay, inline=True)
    embed.add_field(name="Australia: ", value=current_time_aus, inline=True)
    embed.add_field(name="Jordan: ", value=current_time, inline=True)
    embed.add_field(name="California: ", value=current_time_cali, inline=True)
    embed.add_field(name="England: ", value=current_time_uk, inline=True)
    embed.add_field(name="Lebanon: ", value=current_time, inline=True)
    embed.add_field(name="Texas: ", value=current_time_texas, inline=True)
    await ctx.send(embed=embed)

@bot.command() #ref https://github.com/aonghena/CoinBot/blob/master/coinbot.py
async def crypto(ctx):
    cost , change = coinBasePrice('BTC')
    all = '```Bitcoin:       $'
    all += str(cost) + '  ' 
    all += str(change) + '%'
    cost , change = coinBasePrice('ETH')
    all += "\nEthereum:      $"
    all += str(cost) + '    ' 
    all += str(change) + '%'
    cost , change = coinBasePrice('LTC')
    #add etc, 
    all += '\nLitecoin:      $'
    all += str(cost) + '    ' 
    all += str(change) + '%'
    cost , change = coinBasePrice('BCH')
    all += '\nBitcoin Cash:  $'
    all += str(cost) + '   ' 
    all += str(change) + '%'
    cost , change = coinBasePrice('ADA')
    all += '\nCardano:       $'
    all += str(cost) + '      ' 
    all += str(change) + '%'
    cost , change = coinBasePrice('USDT')
    all += '\nTetherUS:      $'
    all += str(cost) + '      ' 
    all += str(change) + '%\n\nData retrieved from coinBase API'
    all += '```'
    await ctx.channel.send(all)
  
def coinBasePrice(x):
    TWOPLACES = Decimal(10) ** -2 
    current = float(requests.get('https://api.coinbase.com/v2/prices/' + x + '-USD/spot').json()['data']['amount'])
    per = round(((current/float(requests.get('https://api.pro.coinbase.com/products/' + x + '-USD/stats').json()['open']))-1)*100,2)
    current = Decimal(current).quantize(TWOPLACES)
    per = Decimal(per).quantize(TWOPLACES)
    return str(current), str(per)

f = open("token.txt")
#another comment
TOKEN = f.readline()

bot.run(TOKEN)