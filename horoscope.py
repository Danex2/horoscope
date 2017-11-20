from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import discord
import datetime
import schedule

client = discord.Client()

zodiac = ['aries','taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

@client.event
async def on_message(message):
    await client.change_presence(game=discord.Game(name="What's in store for you today?"))
    if message.author == client.user:
        return

    if message.content.startswith('&h'):
        sign = message.content[3::].lower()
        if sign in zodiac:
            req = Request('https://www.astrology.com/horoscope/daily/' +sign+ '.html',
                          headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req)
            content = url.read()
            soup = BeautifulSoup(content, "html.parser")
            o = datetime.datetime.now().strftime('%Y/%m/%d')

            i = soup.findAll('p')[0].next
            schedule.every(24).hours.do(await client.send_message(message.channel, "```"))

            await client.send_message(message.channel, "```{p}\n{s}\n\n {h}```".format(h=i, p=o, s=sign))
        elif sign == "":
            await client.send_message(message.channel, "```Usage: &h <sign>```")
        elif sign not in zodiac:
            await client.send_message(message.channel, "```Invalid sign```")
        if message.content.startswith('&invite'):
                await client.send_message(message.channel, "https://discordapp.com/oauth2/authorize?client_id=324703502880210944&scope=bot")

client.run('')
