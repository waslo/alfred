from discord.ext import commands
from discord.ext.commands import Bot
import discord
import random
import json, requests
import praw
import re
import time
from bs4 import BeautifulSoup

bot = Bot(command_prefix="!", description="A bot made by Waslo.")
bot.remove_command('help')

photos_of_arvin = [
    "https://i.imgur.com/QvveBZW.png",
    "https://i.imgur.com/04bXrgr.jpg",
    "https://i.imgur.com/LbGoXwz.jpg",
    "https://i.imgur.com/0CPlwo9.jpg",
    "https://i.imgur.com/bNbDbpZ.png",
    "https://i.imgur.com/PEjLyuA.png"
    "https://i.imgur.com/pSh1aQG.png"
]

photos = [
    "https://i.imgur.com/QOGON8q.jpg",
    "https://i.imgur.com/5pGV1eX.gif",
    "https://i.imgur.com/sR5lJov.jpg",
    "https://i.imgur.com/f0e9nof.png",
]

@bot.event
async def on_ready():
    print('Logged in!')

fn_api_key = ""
with open ('fortnite.txt','r') as myfile:
    fn_api_key = myfile.read()

@bot.command(pass_context=True)
async def help(ctx):
    em = discord.Embed(colour=0x990000)
    em.add_field(name="help", value="Brings up this message.", inline=False)
    em.add_field(name="arvin", value="Sends a random photo of Arvin.", inline=False)
    em.add_field(name="fn", value="Use like so: !fn <platform> <username>, where platforms can be pc/psn/xbl.", inline=False)
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(pass_context=True)
async def arvin(ctx):
    await bot.send_message(ctx.message.channel, random.choice(photos_of_arvin))

@bot.command(pass_context=True)
async def lol(ctx):
    await bot.send_message(ctx.message.channel, random.choice(photos))

@bot.command (pass_context = True)
async def fn(ctx, *args):
    played_name = "Played"
    wins_name = "Wins"
    top_name = "Top 10s/5s/3s"
    top_rate_name = "Top 10/5/3 Rate"
    kd_name = "KDR"
    wr_name = "Win Rate"
    url = "%s%s%s%s" % ("https://api.fortnitetracker.com/v1/profile/", args[0],"/", args[1])
    resp = requests.get(url=url, headers={'trn-api-key': fn_api_key})
    data = json.loads(resp.text)
    #print (data)
    #data_test_value = data["stats"]["curr_p9"]["kd"]["displayValue"]
    #await bot.send_message(ctx.message.channel, data_test_value)
    username = data ["epicUserHandle"]
    profile_url = "%s%s%s%s" % ("https://fortnitetracker.com/profile/", args[0], "/", args[1])
    embed_validation = 0
    d1 = "curr_p2"
    d2 = "curr_p10"
    d3 = "curr_p9"
    #if args[2] == "solo":
        #dataset = "curr_p2"
    #elif args[2] == "duo":
        #dataset = "curr_p10"
    #else:
        #dataset = "curr_p9"

    played = "%s%s%s%s%s" % (data["stats"][d1]["matches"]["displayValue"],"/",data["stats"][d2]["matches"]["displayValue"],"/", data["stats"][d3]["matches"]["displayValue"])
    wins = "%s%s%s%s%s" % (data["stats"][d1]["top1"]["displayValue"],"/",data["stats"][d2]["top1"]["displayValue"],"/", data["stats"][d3]["top1"]["displayValue"])
    kd = "%s%s%s%s%s" % (data["stats"][d1]["kd"]["displayValue"],"/",data["stats"][d2]["kd"]["displayValue"],"/", data["stats"][d3]["kd"]["displayValue"])
    top10 = data["stats"][d1]["top10"]["displayValue"]
    top10rate = int(top10)/int(data["stats"][d1]["matches"]["displayValue"])
    top5 = data["stats"][d2]["top5"]["displayValue"]
    top5rate = int(top5)/int(data["stats"][d2]["matches"]["displayValue"])
    top3 = data["stats"][d3]["top3"]["displayValue"]
    top3rate = int(top3)/int(data["stats"][d3]["matches"]["displayValue"])
    top_rate = "%s%s%s%s%s" %(top10,"/",top5,"/",top3)
    top = "%s%s%s%s%s%s" % (top10,"%/",top5,"%/",top3,"%" )
    wr = "%s%s%s%s%s%s" % (data["stats"][d1]["winRatio"]["displayValue"],"%/",data["stats"][d2]["winRatio"]["displayValue"],"%/", data["stats"][d3]["winRatio"]["displayValue"],"%")
    embed_validation = 1

    em = discord.Embed(title="More Stats", colour=0x42f4eb, url=profile_url)
    em.set_author(name=username)
    em.set_footer(text="Made by Waslo", icon_url="http://i.imgur.com/AKCDVxI.jpg")
    em.add_field(name=played_name, value=played, inline=True)
    em.add_field(name=wins_name, value=wins, inline=True)
    em.add_field(name=top_name, value=top, inline=True)
    em.add_field(name=top_rate_name, value=top_rate, inline=True)
    em.add_field(name=wr_name, value=wr, inline=True)
    em.add_field(name=kd_name, value=kd, inline=True)
    if embed_validation == 1:
        await bot.send_message(ctx.message.channel, embed=em)

with open('secret.txt', 'r') as myfile:
    bot.run(myfile.read())
