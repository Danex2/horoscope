from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import discord
import datetime
import schedule
from datetime import date
import calendar


client = discord.Client()


zodiac = ['aries','taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

@client.event
async def on_message(message):
    await client.change_presence(game=discord.Game(name="What's in store for you today?"))
    if message.author == client.user:
        return

    if message.content.startswith('-h'):
        sign = message.content[3::].lower()
        if sign in zodiac:
            req = Request('http://astrostyle.com/daily-horoscopes/' + sign + '-daily-horoscope/',
                          headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req)
            content = url.read()
            soup = BeautifulSoup(content, "html.parser")
            o = datetime.datetime.now().strftime('%Y/%m/%d')
            todays_date = date.today()
            td = datetime.date.today().strftime("%A").lower()
            if td in weekdays:
                i = soup.find("div", {"id": td }).findAll('p')[0].next
            else:
                i = "shits broke"


            embed=discord.Embed(title="", color=0x808080)
            """embed.set_thumbnail(url="http://www.pngall.com/wp-content/uploads/2016/05/Scorpio-PNG-HD.png")"""
            embed.add_field(name="sign", value=sign, inline=False)
            embed.add_field(name="horoscope", value=i, inline=False)
            embed.set_footer(text="Date: " + o + " | " + "astrostyle.com")
            """schedule.every(24).hours.do(await client.send_message(message.channel, "```"))"""

            await client.send_message(message.channel, embed=embed)
        elif sign == "":
            await client.send_message(message.channel, "``-h <sign>``")
        elif sign not in zodiac:
            await client.send_message(message.channel, "``Invalid sign``")

client.run('')
