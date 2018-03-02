from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import discord
import datetime
import schedule
from datetime import date
import calendar


client = discord.Client()

discordToken = open("token.txt","r").readline()
zodiac = {'aries': 'https://imgur.com/TAgbGIE.png','taurus': 'https://imgur.com/YFDcGHO.png', 'gemini': 'https://imgur.com/YFDcGHO.png', 'cancer': 'https://imgur.com/VkZBJUD.png', 
'leo': 'https://imgur.com/BKjzKhu.png', 'virgo': 'https://imgur.com/YFDcGHO.png', 'libra': 'https://imgur.com/YFDcGHO.png', 'scorpio': 'https://imgur.com/OPvMYU6.png', 
'sagittarius': 'https://imgur.com/Mw5FyG6.png', 'capricorn': 'https://imgur.com/ZCgXIMU.png', 'aquarius': 'https://imgur.com/YiOam4U.png', 'pisces': 'https://imgur.com/YFDcGHO.png'}


weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

@client.event
async def on_message(message):
    await client.change_presence(game=discord.Game(name="What's in store for you today?"))
    if message.author == client.user:
        return

    if message.content.startswith('-h'):
        args = message.content.split(" ")
        sign = args[1]
        sign = sign.lower()
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
            embed.set_thumbnail(url=zodiac[sign])
            embed.add_field(name="sign", value=sign, inline=False)
            embed.add_field(name="horoscope", value=i, inline=False)
            embed.set_footer(text="Date: " + o + " | " + "astrostyle.com")
            """schedule.every(24).hours.do(await client.send_message(message.channel, "```"))"""

            await client.send_message(message.channel, embed=embed)
        elif sign == "":
            await client.send_message(message.channel, "``-h <sign>``")
        elif sign not in zodiac:
            await client.send_message(message.channel, "``Invalid sign``")

client.run(discordToken)
