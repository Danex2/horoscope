from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import discord
import datetime
import schedule
from datetime import date, datetime, timedelta
import calendar
import time
from discord.ext import commands
import traceback

description = '''daily horoscopes'''
bot = commands.Bot(command_prefix='++-', description=description)


discordToken = open("token.txt","r").readline()
zodiac = {'aries': 'https://imgur.com/TAgbGIE.png','taurus': 'https://imgur.com/YFDcGHO.png', 'gemini': 'https://imgur.com/YFDcGHO.png', 'cancer': 'https://imgur.com/VkZBJUD.png', 
'leo': 'https://imgur.com/BKjzKhu.png', 'virgo': 'https://imgur.com/YFDcGHO.png', 'libra': 'https://imgur.com/YFDcGHO.png', 'scorpio': 'https://imgur.com/OPvMYU6.png', 
'sagittarius': 'https://imgur.com/Mw5FyG6.png', 'capricorn': 'https://imgur.com/ZCgXIMU.png', 'aquarius': 'https://imgur.com/YiOam4U.png', 'pisces': 'https://imgur.com/YFDcGHO.png'}



@bot.event
async def on_ready():
    print('Online!')
    await bot.change_presence(game=discord.Game(name="owo"))
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
'''@commands.cooldown(1, 5, commands.BucketType.user)'''
async def h(sign: str, y: str = None):
    if sign in zodiac and y is None:
        req = Request('https://www.astrology.com/horoscope/daily/' + sign + '.html',
                            headers={'User-Agent': 'Mozilla/5.0'})
        url = urlopen(req)
        content = url.read()
        embed=discord.Embed(title="", color=0xcc1df1)
        soup = BeautifulSoup(content, "html.parser")
        today = datetime.now().strftime('%Y/%m/%d')
        i = soup.find("div", {"daily-horoscope"}).findAll('p')[0].next


        '''embed.set_thumbnail(url=zodiac[sign])'''
        embed.add_field(name="sign", value=sign, inline=False)
        embed.add_field(name="horoscope", value=i, inline=False)
        embed.set_footer(text="Date: " + today + " | " + "https://www.astrology.com")
        await bot.say(embed=embed)
    elif sign in zodiac and y is not None:
        req = Request('https://www.astrology.com/horoscope/daily/yesterday/' + sign + '.html',
                            headers={'User-Agent': 'Mozilla/5.0'})
        url = urlopen(req)
        content = url.read()
        embed=discord.Embed(title="", color=0xcc1df1)
        soup = BeautifulSoup(content, "html.parser")
        i = soup.find("div", {"daily-horoscope"}).findAll('p')[0].next
        yesterday = datetime.now() - timedelta(days=1)
            
        embed.add_field(name="sign", value=sign, inline=False)
        embed.add_field(name="yesterday's horoscope", value=i, inline=False)
        embed.set_footer(text="Date: " + str(yesterday.strftime('%Y/%m/%d')) + " | " + "https://www.astrology.com")
        await bot.say(embed=embed)
    elif sign == "":
        await bot.say("``-h <sign>``")
    elif sign not in zodiac:
        await bot.say('``Invalid sign``')
    
    

bot.run(discordToken)

